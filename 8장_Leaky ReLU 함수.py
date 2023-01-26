def leakyReLU(x, beta = 0.01):
    if x < 0:
        return (beta * x)
    else:
        return x