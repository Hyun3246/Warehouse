## Cyclical Learning Rate

1. LR=0.35 vs CLR=0.1-3 <br/>
    test accuracy with respect to iteration
    (Figure 5a)

<br/>

## Weight Decay

1. 0.001 vs 0.0001 vs 0.00001 vs 0.000001 <br/>
    test accuracy with respect to iteration
    (Figure 5b)

2. 1e-3 vs 3.2e-3 vs 1e-2 vs 1.8e-3 <br/>
     test accuracy, test loss with respect to iterations
    - LR=0.005
    - mom=0.95
    (Figure 9)

<br/>

## Momentum

1. Mom 0.9 vs 0.7 vs 0.99 <br/>
    test loss with respect to learning rate
    - CLR=0.002-0.02
    - WD=4e-3
    - TBS=548
    - iteration=10k
    (Figure 7a)

2. Increasing Momentum(0.7-1) <br/>
    test accuracy, test loss with respect to momentum
    - LR=0.01
    - WD=4e-3
    - TBS=548
    - iteration=10k
    (Figure 7b)

3. Mom=0.9 vs CM=0.8-1 vs CM=0.95-0.8 vs CM=0.97-0.7 <br/>
    test loss with respect to learning rate
    - CLR=0.002-0.02
    - WD=4e-3
    - TBS=548
    - iteration=10k
    (Figure 7c)

3. Mom=0.9(LR=0.007) vs CM=0.97-0.7(CLR=0.001-0.007) <br/>
    test loss & test accuracy with respect to iterations
    - WD=4e-3
    - TBS=536
    (Figure 7d)