blockTime = []
totalBlockTime = 0 # totalBlockTime = totalBlockGenerationTime + totalBlockPrepareTime
numOfBlock = 0
failTime = -1.0
queueTooLongTime = -2.0

TXStartTimeSumPerBlock = 0.0
TXNumOfThisBlock = 0
totalTXNum = 0

totalTXPendingTime = 0
totalUploadTime = 0
totalDownloadTime = 0
totalNetworkDelayTime = 0
totalBlockGenerationTime = 0 # totalBlockGenerationTime = totalUploadTime + totalDownloadTime + totalNetworkDelayTime + "Block building time"
totalBlockPrepareTime = 0

def addTransactionsStartTime(txs):
    global TXStartTimeSumPerBlock, TXNumOfThisBlock, totalTXNum
    TXStartTimeSumPerBlock = 0.0
    TXNumOfThisBlock = len(txs)
    totalTXNum += TXNumOfThisBlock
    for tx in txs:
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@ tx[0]: " + str(tx[0]))
        
        TXStartTimeSumPerBlock += float(tx[0])

def addPendingTime(sim_time):
    global totalTXPendingTime
    
    totalTXPendingTime += sim_time * TXNumOfThisBlock - TXStartTimeSumPerBlock

def addBlockTime(time):
    global blockTime
    global totalBlockTime
    
    totalBlockTime = totalBlockTime + time
    blockTime.append(time)