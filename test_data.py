blockTime = []
totalBlockTime = 0

def addBlockTime(time):
    global blockTime
    global totalBlockTime
    
    totalBlockTime = totalBlockTime + time
    blockTime.append(time)