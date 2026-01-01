'''
Transformer 모델 구현 (PyTorch)

이 코드는 PyTorch를 사용하여 Transformer 모델을 구현한 것이다.
대부분의 구현은 "Attention is All You Need" 논문의 구조를 참고하였으며, normalization 위치 등 일부는 이후 연구 결과를 반영하여 수정하였다.

코드의 구성은 가장 high-level에서부터 차례대로 다음과 같다.

0. 모델 생성 함수
- build_model(): Transformer 모델 생성 함수

1. 모델의 구성
- Transformer: 전체적인 Transformer 모델 구조 정의

2. Encoder, Decoder 및 Block 정의
- Encoder: Encoder 정의
- EncoderBlock: Encoder를 구성하는 block 정의
- Decoder: Decoder 정의
- DecoderBlock: Decoder를 구성하는 block 정의

3. Encoder, Decoder Block 내부에 들어가는 Layer 정의
- MultiHeadAttentionLayer: Multi-Head Attention Layer
- PositionWiseFeedForwardLayer: Position-wise Feed-Forward Layer
- AddNormLayer: Residual Connection + Layer Normalization

4. Embedding 정의
- TransformerEmbedding: Token Embedding + Positional Encoding
- TokenEmbedding: Token Embedding
- PositionalEncoding: Positional Encoding

'''
import torch
import torch.nn as nn
import math
import copy
import torch.nn.functional as F

# build_model(): Transformer 모델 생성 함수. 모델을 생성할 때는 이 함수만 호출하면 된다.
def build_model(src_vocab_size, tgt_vocab_size, device=torch.device("cpu"), max_len=256, d_embed=512, n_layer=6, d_model=512, h=8, d_ff=2048, dropout_ratio=0.1):
    copy = copy.deepcopy

    # Tokenembedding 및 Positional Encoding
    src_token_embed = TokenEmbedding(d_embed=d_embed, vocab_size=src_vocab_size)
    tgt_token_embed = TokenEmbedding(d_embed=d_embed, vocab_size=tgt_vocab_size)
    pos_embed = PositionalEncoding(d_embed=d_embed, max_len=max_len, device=device)
    src_embed = TransformerEmbedding(token_embed=src_token_embed, pos_embed=copy(pos_embed))
    tgt_embed = TransformerEmbedding(token_embed=tgt_token_embed, pos_embed=copy(pos_embed))

    # Multi-Head Attention
    attention = MultiHeadAttentionLayer(d_model=d_model, h=h, qkv_fc=nn.Linear(d_embed, d_model), out_fc=nn.Linear(d_model, d_embed))

    # PositionWiseFeedForwardLayer
    position_ff = PositionWiseFeedForwardLayer(fc1=nn.Linear(d_embed, d_ff),fc2=nn.Linear(d_ff, d_embed))

    # Encoder and Decoder Block
    encoder_block = EncoderBlock(self_attention=copy(attention), position_ff=copy(position_ff), d_model=d_model, dropout_ratio=dropout_ratio)
    decoder_block = DecoderBlock(self_attention=copy(attention), cross_attention=copy(attention), position_ff=copy(position_ff), d_model=d_model, dropout_ratio=dropout_ratio)

    # Encoder and Decoder
    encoder = Encoder(encoder_block=encoder_block, n_layer=n_layer)
    decoder = Decoder(decoder_block=decoder_block, n_layer=n_layer)

    # Generator
    generator = nn.Linear(d_model, tgt_vocab_size)

    # 전체 모델
    model = Transformer(src_embed=src_embed, tgt_embed=tgt_embed, encoder=encoder, decoder=decoder, generator=generator).to(device)
    
    model.device = device

    return model


# 전체적인 Transformer 모델 구조 정의
class Transformer(nn.Module):
    def __init__(self, src_embed, tgt_embed, encoder, decoder, generator):
        super(Transformer, self).__init__()
        self.src_embed = src_embed  
        self.tgt_embed = tgt_embed
        self.encoder = encoder
        self.decoder = decoder
        self.generator = generator      # 최종 출력 생성

    def encode(self, src, src_mask):
        out = self.encoder(self.src_embed(src), src_mask)
        return out

    def decode(self, tgt, encoder_out, tgt_mask, src_tgt_mask):
        out = self.decoder(self.tgt_embed(tgt), encoder_out, tgt_mask, src_tgt_mask)
        return out
    
    def forward(self, src, tgt, src_mask):    # src: source, tgt:target, src_mask: padding masking 여부
        src_mask = self.make_src_mask(src)
        tgt_mask= self.make_tgt_mask(tgt)
        src_tgt_mask = self.mask_src_tgt_mask(src, tgt)
        encoder_out = self.encode(src, src_mask)
        decoder_out = self.decode(tgt, encoder_out, tgt_mask, src_tgt_mask)
        out = self.generator(decoder_out)
        out = F.log_softmax(out, dim=-1)
        return out, decoder_out
    
    # make_pad_mask(): padding 토큰을 가리는 mask를 직접 처리해 반환.
    def make_pad_mask(self, query, key, pad_idx=1):
        # query: (n_batch, query_seq_len)
        # key: (n_batch, key_seq_len)
        query_seq_len, key_seq_len = query.size(1), key.size(1) 
        
        key_mask = key.ne(pad_idx).unsqueeze(1).unsqueeze(2)    # (n_batch, 1, 1, key_seq_len)
        key_mask = key_mask.repeat(1, 1, query_seq_len, 1)      # (n_batch, 1, query_seq_len, key_seq_len)

        query_mask = query.ne(pad_idx).unsqueeze(1).unsqueeze(3)    # (n_batch, 1, query_seq_len, 1)
        query_mask = key_mask.repeat(1, 1, 1, key_seq_len)      # (n_batch, 1, query_seq_len, key_seq_len)

        mask = key_mask & query_mask
        mask.requires_grad = False
        return mask
    
    # make_subsequent_mask(): 현재 위치 이후의 단어를 가리는 mask만 생성 (decoder에서 사용, query, key를 직접 바꾸지는 않음.)
    def make_subsequent_mask(self, query, key):
        # query: (n_batch, query_seq_len)
        # key: (n_batch, key_seq_len)
        query_seq_len, key_seq_len = query.size(1), key.size(1)

        tril = torch.tril(torch.ones((query_seq_len, key_seq_len)), k=0).astype('uint8')      # lower triangle marix 생성
        mask = torch.tensor(tril, dtype=torch.bool, requires_grad=False, device=query.device)   # 대각선 포함 아래쪽은 True, 나머지는 False
        return mask
    
    # make_src_mask(): source 문장에 대한 masking 생성
    def make_src_mask(self, src):
        pad_mask = self.make_pad_mask(src, src)     # sorce에서는 문장 전체를 다 봐도 되므로 padding 토큰을 가리는 mask만 사용.
        return pad_mask
    
    # make_tgt_mask(): target 문장에 대한 masking 생성 (padding masking + subsequent masking)
    def make_tgt_mask(self, tgt):
        pad_mask = self.make_pad_mask(tgt, tgt)
        seq_mask = self.make_subsequent_mask(tgt, tgt)  # target 문장에서는 이후 토큰은 보면 안됨.
        mask = pad_mask & seq_mask      # 둘 다 True인 부분만 남긴다.
        return mask

    # mask_src_tgt_mask(): Decoder가 Cross-Attention에서 encoder의 출력을 참조할 떼, source의 패딩을 무시하도록 함.
    def mask_src_tgt_mask(self, src, tgt):
        pad_mask = self.make_pad_mask(tgt, src)
        return pad_mask
    

# Encoder 클래스: Encooder block을 모아 encoder 정의
class Encoder(nn.Module):
    def __init__(self, encoder_layer, n_layer):
        super(Encoder, self).__init__()
        self.layers = nn.ModuleList([copy.deepcopy(encoder_layer) for _ in range(n_layer)])    # 정해진 개수만큼 encoder layer 추가
        
    def forward(self, src, src_mask):   # src: source, src_mask: padding masking 여부
        out = src
        for layer in self.layers:
            out = layer(out, src_mask)
        return out

# Encoderblock 클래스: Multi-Head Attention + Add Norm + Position-wise Feed-Forward Layer + Add Norm
class EncoderBlock(nn.Module):
    def __init__(self, self_attention, position_ff, d_model, dropout_ratio=0.1):
        super(EncoderBlock, self).__init__()
        self.self_attention = self_attention    # Multi-Head Attention
        self.position_ff = position_ff          # Position-wise Feed-Forward Layer
        self.residuals = nn.ModuleList([AddNormLayer(d_model, dropout_ratio) for _ in range(2)])  # Add Norm Layer
    
    def forward(self, src, src_mask):       # src: source, src_mask: padding masking 여부
        out = src
        out = self.residuals[0](out, lambda out: self.self_attention(query=out, key=out, value=out, mask=src_mask))     # Multi-Head Attention
        out = self.residuals[1](out, self.position_ff) # Position-wise Feed-Forward Layer     
        return out


# Decoder 클래스: Decooder block을 모아 encoder 정의
class Decoder(nn.Module):
    def __init__(self, decoder_block, n_layer):
        super(Decoder, self).__init__()
        self.n_layer = n_layer
        self.layers = nn.ModuleList([copy.deepcopy(decoder_block) for _ in range(self.n_layer)])
    
    def forward(self, tgt, encoder_out, tgt_mask, src_tgt_mask):
        out = tgt
        for layer in self.layers:
            out = layer(out, encoder_out, tgt_mask, src_tgt_mask)
        return out


# Decoderblock 클래스: Masked Multi-Head Attention + Add Norm + Multi-Head Attention + Add Norm + Position-wise Feed-Forward Layer + Add Norm
class DecoderBlock(nn.Module):
    def __init__(self, self_attention, cross_attention, position_ff, d_model, dropout_ratio=0.1):
        super(DecoderBlock, self).__init__()
        self.self_attention = self_attention
        self.cross_attention = cross_attention
        self.position_ff = position_ff
        self.residuals = nn.ModuleList([AddNormLayer(d_model, dropout_ratio) for _ in range(3)])
    
    def forward(self, tgt, encoder_out, tgt_mask, src_tgt_mask):
        out = tgt
        out = self.residuals[0](out, lambda out: self.self_attention(query=out, key=out, value=out, mask=tgt_mask))
        out = self.residuals[1](out, lambda out: self.cross_attention(query=out, key=encoder_out, value=encoder_out, mask=src_tgt_mask))
        out = self.residuals[2](out, self.position_ff)
        return out


# Multi-Head Attention Layer 클래스
class MultiHeadAttentionLayer(nn.Module):
    def __init__(self, d_model, h, qkv_fc, out_fc):
        super(MultiHeadAttentionLayer, self).__init__()
        self.d_model = d_model
        self.h = h                          # 병렬 처리 단위
        self.q_fc = copy.deepcopy(qkv_fc)   # Q를 만들기 위한 fully connected layer (d_embed, d_model)
        self.k_fc = copy.deepcopy(qkv_fc)   # K를 만들기 위한 fully connected layer (d_embed, d_model)
        self.v_fc = copy.deepcopy(qkv_fc)   # V를 만들기 위한 fully connected layer (d_embed, d_model)
        self.out_fc = out_fc                # (d_model, d_embed)
    
    # Scaled-dot Product Attention
    def calculate_attention(self, query, key, value, mask):
        # query, key, value: (n_batch, h, seq_len, d_k)
        # mask: (n_batch, 1, seq_len, seq_len)
        d_k = key.shape[-1]
        attention_score = torch.matmul(query, key.transpose(-2, -1))  # Q x K^T, (n_batch, h, seq_len, seq_len). transpose(-2, -1)는 마지막 두 차원을 서로 바꾼다.
        attention_score = attention_score / math.sqrt(d_k)
        
        if mask is not None:  # 입력 sequence의 길이를 맞추기 위한 padding mask 적용 여부
            attention_score = attention_score.masked_fill(mask==0, -1e9)

        attention_prob = F.softmax(attention_score, dim=-1) # (n_batch, h, seq_len, seq_len)
        out = torch.matmul(attention_prob, value)   # (n_batch, h, seq_len, d_k)
        return out
    
    def forward(self, *args, query, key, value, mask=None):
        # query, key, value: (n_batch, seq_len, d_embed)
        # mask: (n_batch, seq_len, seq_len)
        # return value: (n_batch, h, seq_len, d_k)
        n_batch = query.size(0)

        # 변환 함수
        def transform(x, fc): # x = (n_batch, seq_len, d_embed)
            out = fc(x)     # 벡터 공간 변환 (n_batch, seq_len, d_model)
            out = out.view(n_batch, -1, self.h, self.d_model // self.h)     # h개의 헤드로 쪼개기 (n_batch, seq_len, h, d_k)
            out = out.transpose(1, 2)       # (n_batch, h, seq_len, d_k)
            return out
        
        query = transform(query, self.q_fc)
        key = transform(key, self.k_fc)
        value = transform(value, self.v_fc)

        out = self.calculate_attention(query, key, value, mask)     # Scaled-Dot Product Attention 계산  (n_batch, h, seq_len, d_k)
        out = out.transpose(1, 2)   # (n_batch, seq_len, h, d_k)
        out = out.contiguous().view(n_batch, -1, self.d_model)  # 계산 결과 concatenation (n_batch, seq_len, d_model)
        out = self.out_fc(out)  # (n_batch, seq_len, d_embed)

        return out


# Position-wise Feed-Forward Layer 클래스
class PositionWiseFeedForwardLayer(nn.Module):
    def __init__(self, fc1, fc2):
        super(PositionWiseFeedForwardLayer, self).__init__()
        self.fc1 = fc1
        self.relu = nn.ReLU()
        self.fc2 = fc2
    
    def forward(self, x):
        out = x
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# AddNormLayer 클래스: Residual Connection + Layer Normalization
class AddNormLayer(nn.Module):
    def __init__(self, d_model, dropout_ratio=0.1):
        super(AddNormLayer, self).__init__()
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout_ratio)
    
    def forward(self, x, sub_layer):
        out = x
        out = sub_layer(out)
        out = self.dropout(out)
        out = self.norm(out + x)        # 원본 논문과는 다르게 Dropout -> Layer Normalization 방식이 안정적
        return out


# TransformerEmbedding 클래스: Token Embedding + Positional Encoding
class TransformerEmbedding(nn.Module):
    def __init__(self, token_embed, pos_embed, dropout_ratio=0.1):
        super(TransformerEmbedding, self).__init__()
        self.embedding = nn.Sequential(token_embed, pos_embed)
        self.dropout = nn.Dropout(dropout_ratio)
    
    def forward(self, x):
        out = self.embedding(x)
        out = self.dropout(out)
        return out
    
# Token Embedding 클래스: token에 대한 word embedding을 생성한다.
class TokenEmbedding(nn.Module):
    def __init__(self, d_embed, vocab_size):
        super(TokenEmbedding, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_embed)
        self.d_embed = d_embed
    
    def forward(self, x):
        out = self.embedding(x) * math.sqrt(self.d_embed)       # 제곱근을 곱해 positional embedding과 스케일 맞춤.
        return out

# Positional Encoding 클래스: positional embedding을 생성한다.
class PositionalEncoding(nn.Module):
    def __init__(self, d_embed, max_len=256, device=torch.device("cpu")):
        super(PositionalEncoding, self).__init__()
        encoding = torch.zeros(max_len, d_embed)
        encoding.requires_grad = False
        position = torch.arange(0, max_len).float().unsqueeze(1)    # 분자 position 인자 미리 계산
        div_term = torch.exp(torch.arange(0, d_embed, 2) * -(math.log(10000.0) / d_embed))  # 분자 미리 계산 (분수를 지수에 -1을 넣는 것으로 대신하고, 
                                                                                            # exp와 ln을 연속적으로 적용하여 컴퓨터 계산에서의 수치적 안정성 확보)
        encoding[:, 0::2] = torch.sin(position * div_term)      # 짝수열은 sin
        encoding[:, 1::2] = torch.cos(position * div_term)      # 홀수열은 cos
        self.encoding = encoding.unsqueeze(0).to(device)
    
    def forward(self, x):
        _, seq_len, _ = x.size()
        pos_embed = self.encoding[:, :seq_len, :]
        out = x + pos_embed
        return out
    