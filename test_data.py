blockTime = []
totalBlockTime = 0 # totalBlockTime = totalBlockGenerationTime + totalBlockPrepareTime
numOfBlock = 0
failTime = -1.0
queueTooLongTime = -2.0

totalUploadTime = 0
totalDownloadTime = 0
totalNetworkDelayTime = 0
totalBlockGenerationTime = 0 # totalBlockGenerationTime = totalUploadTime + totalDownloadTime + totalNetworkDelayTime + "Block building time"
totalBlockPrepareTime = 0

def addBlockTime(time):
    global blockTime
    global totalBlockTime
    
    totalBlockTime = totalBlockTime + time
    blockTime.append(time)