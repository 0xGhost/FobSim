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

# txPerBlock=(128 256 512 1024 2048 4096 8192)
#txPerBlock=(5 10 15 20 25 30)
#txPerBlock=(2 4)
#txPerBlock=(2 4 8 16 32)
#injectionRate=(256)
#injectionRate=(2 4 8 16 32 64 128 256 512 1024)
#injectionRate=(256 512 1024 2048 4096 8192 16384 32768)
# injectionRate=(16)

#           1   2   3   4   5   6   7   8   9
txPerBlock=(5   10  15  20  25  30  35  40  45)
#txPerBlock=(5   10)

#               1    2    3    4    5    6    7    8    9
injectionRate1=(256  512  704  1088 1280 1408 1792 2176 2176) 
injectionRate3=(288  576  768  1152 1408 1536 1920 2304 2304)
#injectionRate1=(256  576    8    16   32   64   128  256  512) 
#injectionRate2=(16  32   64   128  256  512  1024 2048 4096)
#injectionRate3=(288  640   128  256  512  1024 2048 4096 8192)



runs=10

txPerBlock_length=${#txPerBlock[@]}
for ((i = 0; i < txPerBlock_length; i++))
do
    for j in {1..runs} 
    do
        python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "${injectionRate1[$i]}"
    done

    for j in {1..runs} 
    do
        injectionRateM=$(((${injectionRate1[$i]} + ${injectionRate3[$i]}) / 2))
        python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "$injectionRateM"
    done

    for j in {1..runs} 
    do
        python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "${injectionRate3[$i]}"
    done
done

# for k in "${txPerBlock[@]}" # k: tx per block
# do
#     #for i in {1..10} # runs
#     for j in "${injectionRate[@]}" # j: injection rate
#     do
#         #for j in "${injectionRate[@]}" # j: injection rate
#         for i in {1..10} # runs
#         do
#             # python3 main.py [isBlackGun] [MachineName] [function] [placement] [consensus] [tx per block] [injection rate]
#             python3 main.py 1 [3080ti] 1 2 2 "$k" "$j"
#         done
#     done
# done