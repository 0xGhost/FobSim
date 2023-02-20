blockTime = []
totalBlockTime = 0
numOfBlock = 0
queueTooLongTime = -1.0

def addBlockTime(time):
    global blockTime
    global totalBlockTime
    
    totalBlockTime = totalBlockTime + time
    blockTime.append(time)