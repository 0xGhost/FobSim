#!/bin/bash


# [function]
# Please choose the function of the Blockchain network:
# (1) Data Management
# (2) Computational services
# (3) Payment
# (4) Identity Management

# [placement]
# Please choose the placement of the Blockchain network:
# (1) Fog Layer
# (2) End-User layer

# [consensus]
# Please choose the Consensus algorithm to be used in the simulation:
# 1: Proof of Work (PoW)
# 2: Proof of Stake (PoS)
# 3: Proof of Authority (PoA)
# 4: Proof of Elapsed Time (PoET)
# 5: Delegated Proof of Stake (DPoS)
# 6: Example New CA

txPerBlock=(2 4)
#txPerBlock=(2 4 8 16 32)
injectionRate=(2 4 8 16 32 64 128 256 512 1024)
#injectionRate=(2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384)

for k in "${txPerBlock[@]}" # k: tx per block
do
    for j in "${injectionRate[@]}" # j: injection rate
    do
        for i in {1..5} # runs
        do
            # python3 main.py [isBlackGun] [MachineName] [function] [placement] [consensus] [tx per block] [injection rate]
            python3 main.py 1 [3070ti] 1 2 2 "$k" "$j"
        done
    done
done