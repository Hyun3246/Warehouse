'''
Transformer Decoder 모델 구현 (PyTorch)

이 코드는 PyTorch를 사용하여 Transformer Decoder 모델을 구현한 것이다.
대부분의 구현은 "Generating wikipedia by summarizing long sequences." 논문의 구조를 참고하였다.

코드의 구성은 가장 high-level에서부터 차례대로 다음과 같다.

0. 모델 생성 함수
- build_dmca_model(): Transformer DMCA 모델 생성 함수

1. 모델의 구성
- TransformerDMCA: 전체적인 Transformer DMCA 모델 구조 정의

2. Decoder 및 Block 정의
- DMCADecoder: Decoder 정의
- DMCADecoderBlock: Decoder를 구성하는 block 정의

3. Decoder Block 내부에 들어가는 Layer 정의
- DMCAMultiHeadAttentionLayer: Multi-Head Attention Layer
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
def build_dmca_model(vocab_size, device=torch.device("cpu"), max_len=4096, d_embed=512, d_model=512, h=8, d_ff=2048, dropout_ratio=0.1):
    copy = copy.deepcopy

    # 1. Embedding (Source/Target 구분 없이 하나로 통합)
    token_embed = TokenEmbedding(d_embed=d_embed, vocab_size=vocab_size)
    pos_embed = PositionalEncoding(d_embed=d_embed, max_len=max_len, device=device)
    total_embed = TransformerEmbedding(token_embed=token_embed, pos_embed=copy(pos_embed))

    # 2. Feed Forward
    position_ff = PositionWiseFeedForwardLayer(fc1=nn.Linear(d_embed, d_ff), fc2=nn.Linear(d_ff, d_embed))

    # 3. Layer 구성 (논문과 동일한 L, M, L, M, L)
    layers = nn.ModuleList()
    modes = ['local', 'memory_compressed', 'local', 'memory_compressed', 'local']

    for mode in modes:
        attn_layer = DMCAMultiHeadAttentionLayer(
            d_model=d_model,
            h=h,
            qkv_fc=nn.Linear(d_embed, d_model),
            out_fc=nn.Linear(d_model, d_embed),
            mode=mode,
            block_size=256,
            kernel_size=3,
            stride=3
        )

        block = DMCADecoderBlock(
            self_attention=attn_layer,
            position_ff=copy(position_ff),
            d_model=d_model,
            dropout_ratio=dropout_ratio
        )
        layers.append(block)
    
    # 4. Generator
    generator = nn.Linear(d_model, vocab_size)

    # 5. 모델 조립
    model = TransformerDMCA(token_embed=total_embed, layers=layers, generator=generator)
    model.device = device
    return model


# 전체적인 TransformerDMCA 모델 구조 정의
class TransformerDMCA(nn.Module):
    def __init__(self, token_embed, layers, generator):
        super(TransformerDMCA, self).__init__()
        self.token_embed = token_embed
        self.layers = layers
        self.generator = generator      # 최종 출력 생성
    
    def forward(self, x): 
        out = self.token_embed(x)

        for layer in self.layers:
            out = layer(out)
        
        out = self.generator(out)
        out = F.log_softmax(out, dim=-1)
        return out


# DMCADecoderblock 클래스: (Local or Compressed) Self-Attention + Add Norm + Position-wise Feed-Forward Layer + Add Norm
class DMCADecoderBlock(nn.Module):
    def __init__(self, self_attention, position_ff, d_model, dropout_ratio=0.1):
        super(DMCADecoderBlock, self).__init__()
        self.self_attention = self_attention
        self.position_ff = position_ff
        self.residuals = nn.ModuleList([AddNormLayer(d_model, dropout_ratio) for _ in range(2)])
    
    def forward(self, x):
        out = x
        out = self.residuals[0](out, lambda out: self.self_attention(x=out))
        out = self.residuals[1](out, self.position_ff)
        return out


# DMCA Multi-Head Attention Layer 클래스
class DMCAMultiHeadAttentionLayer(nn.Module):
    def __init__(self, d_model, h, qkv_fc, out_fc, mode="local", block_size=256, kernel_size=3, stride=3):
        super(DMCAMultiHeadAttentionLayer, self).__init__()
        self.d_model = d_model
        self.h = h                          # 병렬 처리 단위
        self.mode = mode                    # Local attention or Memory-compressed attention
        self.block_size = block_size
        self.kernel_size = kernel_size
        self.stride = stride

        self.q_fc = copy.deepcopy(qkv_fc)   # Q를 만들기 위한 fully connected layer (d_embed, d_model)
        self.k_fc = copy.deepcopy(qkv_fc)   # K를 만들기 위한 fully connected layer (d_embed, d_model)
        self.v_fc = copy.deepcopy(qkv_fc)   # V를 만들기 위한 fully connected layer (d_embed, d_model)
        self.out_fc = out_fc                # (d_model, d_embed)

        # Memory-compressed attention인 경우 Conv layer를 추가로 정의.
        if self.mode == "memory_compressed":    
            self.compress_conv = nn.Conv1d(
                in_channels=d_model,
                out_channels=d_model,
                kernel_size=self.kernel_size,
                stride=self.stride,
                padding=kernel_size//2
            )
    
    # Scaled-dot Product Attention
    def calculate_attention(self, query, key, value, mask):
        # query: (n_batch, h, q_len, d_k)
        # key, value: (n_batch, h, k_len, d_k)
        d_k = key.shape[-1]

        # Score 계산: Q x K^T, (n_batch, h, seq_len, seq_len). 
        attention_score = torch.matmul(query, key.transpose(-2, -1))  # transpose(-2, -1)는 마지막 두 차원을 서로 바꾼다.
        attention_score = attention_score / math.sqrt(d_k)
        
        # Masking
        # Local mode 일 때: (block_size, block_size) -> 블록 안에서만 미래 정보를 가리면 됨. (정사각형)
        # Compressed mode 일 때: (q_len, k_len) -> 압축된 길이까지 고려해야함. (직사각형)
        if mask is not None:  # 입력 sequence의 길이를 맞추기 위한 padding mask 적용 여부
            attention_score = attention_score.masked_fill(mask==0, -1e9)

        attention_prob = F.softmax(attention_score, dim=-1) 
        out = torch.matmul(attention_prob, value)   
        return out
    
    def forward(self, x, mask=None):
        # x: (n_batch, seq_len, d_embed) -> Decoder only이므로 Q=K=V=x
        n_batch, seq_len, d_embed = x.size()

        if self.mode == 'local':
            # Padding: 만약 block의 크기보다 작을 경우에 사용
            pad_len = (self.block_size - (seq_len % self.block_size)) % self.block_size
            if pad_len > 0:     # padding이 필요한 경우
                x = F.pad(x, (0, 0, 0, pad_len))
            
            # Reshape: (B, Num_Blocks, Block_Size, d_embed) -> (B * Num_Blocks, Block_Size, d_embed)
            # 배치 차원을 늘려서 블록들을 독립적인 배치처럼 처리
            x_reshaped = x.view(n_batch, -1, self.block_size, d_embed)
            num_blocks = x_reshaped.size(1)
            x_local = x_reshaped.view(-1, self.block_size, d_embed)

            # Projection
            query = self.transform(x_local, self.q_fc)
            key = self.transform(x_local, self.k_fc)
            value = self.transform(x_local, self.v_fc)

            # Local Causal Mask
            local_mask = torch.tril(torch.ones((self.block_size, self.block_size), device=x.device)).bool()

            # Attention
            out = self.calculate_attention(query, key, value, local_mask)

            # 원래 형태로 복구
            out = out.transpose(1, 2).contiguous().view(-1, self.block_size, self.d_model)
            out = out.view(n_batch, -1, self.d_model)

            if pad_len > 0:
                out = out[:, :seq_len, :]
            
            return self.out_fc(out)
        
        elif self.mode == 'memory_compressed':
            query = self.transform(x, self.q_fc)    # query는 원본 유지

            x_t = x.transpose(1, 2)     # Key, Value 압축을 위해 차원 변경
            
            # Conv1d 수행
            k_compressed = self.compress_conv(x_t).transpose(1, 2)
            v_compressed = self.compress_conv(x_t).transpose(1, 2)

            # Projection
            key = self.transform(k_compressed, self.k_fc)
            value = self.transform(v_compressed, self.v_fc)

            mca_mask = None
            out = self.calculate_attention(query, key, value, mca_mask)

            out = out.transpose(1, 2).contiguous().view(n_batch, -1, self.d_model)
            return self.out_fc(out)

    # 변환 함수
    def transform(self, x, fc): 
        n_batch = x.size(0)     # Local Mode일 경우, n_batch는 실제 배치가 아니라 (Batch * Num_Blocks)가 됨.
        out = fc(x)     # 벡터 공간 변환 (n_batch, len, d_model)
        out = out.view(n_batch, -1, self.h, self.d_model // self.h)     # h개의 헤드로 쪼개기 (n_batch, len, h, d_k)
        out = out.transpose(1, 2)       # (n_batch, h, len, d_k)
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
    
