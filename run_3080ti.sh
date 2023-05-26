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

#                 1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19
# up100 down200
# injectionRate1=(50   50    50   60   70   80   90  100  100  100  100  100  100  100  100  100  100  100  100) 
# injectionRate3=(100  120  160  170  180  200  210  220  220  220  220  250  250  250  250  250  300  300  300)
# up200 down400
# injectionRate1=(100  125  150  180  190  195  200  200  200  200  200  200  200  200  200  200  200  200  200) 
# injectionRate3=(175  215  235  250  260  270  280  300  300  300  300  300  300  300  300  300  300  300  300)
# up300 down600
# injectionRate1=(150  210  230  250  280  300  300  310  310  310  310  320  320  320  320  320  320  320  320) 
# injectionRate3=(250  310  330  350  380  400  400  410  410  410  410  420  420  420  420  420  420  420  420)
# up400 down800
# injectionRate1=(220  310  330  360  380  390  400  410  410  410  410  420  420  420  420  420  420  420  420) 
# injectionRate3=(310  410  430  460  480  490  500  510  510  510  510  520  520  520  520  520  520  520  520)
# up500 down1000
# injectionRate1=(300  350  400  430  460  470  480  500  510  520  525  530  530  530  530  530  530  530  530) 
# injectionRate3=(400  450  500  530  560  570  580  600  610  620  625  630  630  630  630  630  630  630  630)
# up600 down1200
# injectionRate1=(300  350  400  470  500  530  570  600  610  620  630  640  640  640  640  640  640  640  640) 
# injectionRate3=(500  550  600  630  660  670  700  700  740  750  760  770  770  770  770  770  770  770  770)
# up700 down1400
# injectionRate1=(300  400  500  570  600  630  670  700  710  720  730  740  750  750  750  750  750  750  750)
# injectionRate3=(500  600  690  770  800  830  870  900  910  920  930  940  950  950  950  950  950  950  950)
# up800 down1600
# injectionRate1=(400  500  600  670  700  730  770  800  810  820  830  840  860  860  860  860  860  860  860)
# injectionRate3=(600  700  790  870  900  930  970  1000 1010 1020 1030 1040 1060 1060 1060 1060 1060 1060 1060)

#                 1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19

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
    # for j in $(seq $injectionRate1 $step $injectionRate3); 
    # for j in $(seq $((${injectionRate1[$i]}+50)) $step $((${injectionRate3[$i]}+150))); 
    for j in $(seq ${injectionRate1[$i]} $step ${injectionRate3[$i]}); 
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