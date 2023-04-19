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

start=$(date +%s.%N)

# txPerBlock=(128 256 512 1024 2048 4096 8192)
#txPerBlock=(5 10 15 20 25 30)
#txPerBlock=(2 4)
#txPerBlock=(2 4 8 16 32)
#injectionRate=(256)
#injectionRate=(2 4 8 16 32 64 128 256 512 1024)
#injectionRate=(256 512 1024 2048 4096 8192 16384 32768)
# injectionRate=(16)

#           1   2   3   4   5   6   7   8   9
# txPerBlock=(5   10  15  20  25  30  35  40  45)
#txPerBlock=(5   10)
# txPerBlock=(300)
# txPerBlock=(100 200 300 400 500 600 700 800 900)

#           1   2   3   4   5   6   7   8   9  10 11 12 13 14 15 16 17 18 19
txPerBlock=(5   10  15  20  25  30  35  40  45 50 55 60 65 70 75 80 85 90 95)


#               1    2    3    4    5    6    7    8    9
# injectionRate1=(150  340  530  650  800  950  1100 1250 1450) 
# injectionRate3=(250  500  650  850  1050 1300 1600 1700 1900)
# injectionRate1=(100 400 550  850 1100 1350 1600 2000 2400) 
# injectionRate3=(3000 6000 8500 12000 16000 19000 22000 28000 32000)

#                 1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19
injectionRate1=(50   50    50   60   70   80   90  100  100  100  100  100  100  100  100  100  100  100  100) 
injectionRate3=(100  120  160  170  180  200  210  220  220  220  220  250  250  250  250  250  300  300  300)
# injectionRate1=50
# injectionRate3=500

#injectionRate1=(256  576    8    16   32   64   128  256  512) 
#injectionRate2=(16  32   64   128  256  512  1024 2048 4096)
#injectionRate3=(288  640   128  256  512  1024 2048 4096 8192)


#     1 2 3 4 5 6 7 8 9
#  step=5
 step=1
#  step=(2 2 2 2 2 2 2 2 2)

txPerBlock_length=${#txPerBlock[@]}

for ((i = 0; i < txPerBlock_length; i++))
do
    for j in $(seq $injectionRate1 $step $injectionRate3); 
    # for j in $(seq ${injectionRate1[$i]} $step ${injectionRate3[$i]}); 
    # for j in $(seq ${injectionRate1[$i]} ${step[$i]} ${injectionRate3[$i]}); 
    do
        for k in {1..100} # runs
        do
            # python3 main.py [isBlackGun] [MachineName] [function] [placement] [consensus] [tx per block] [injection rate]
            python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "$j"
        done
    done
done

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc)

echo "Runtime: $runtime seconds"

# runs=10

# txPerBlock_length=${#txPerBlock[@]}
# for ((i = 0; i < txPerBlock_length; i++))
# do
#     for j in {1..10} 
#     do
#         python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "${injectionRate1[$i]}"
#     done

#     for j in {1..10} 
#     do
#         injectionRateM=$(((${injectionRate1[$i]} + ${injectionRate3[$i]}) / 2))
#         python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "$injectionRateM"
#     done

#     for j in {1..10} 
#     do
#         python3 main.py 1 [3080ti] 1 2 2 "${txPerBlock[$i]}" "${injectionRate3[$i]}"
#     done
# done

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