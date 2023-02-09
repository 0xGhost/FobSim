blockTime = []
totalBlockTime = 0

def addBlockTime(time):
    global blockTime
    global totalBlockTime
    
    totalBlockTime = totalBlockTime + time
    #totalBlockTime = 3.0
    print("========================= total block time = " + str(totalBlockTime))
    blockTime.append(time)