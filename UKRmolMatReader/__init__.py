import pynumwrap as nw

NUMFIELDCHARS=20

def _checkLineLength(line, linNum, numElements):
    if len(line)!=numElements*NUMFIELDCHARS+1 and len(line)!=numElements*NUMFIELDCHARS+2: #Depending on new line sequence
        raise Exception("Line " + str(linNum) + " bad: " + str(line) + "  Len: " + str(len(line)) + "  Elements: " + str(numElements))

def _readLines(kmats, ene, line, numElements, cElement):
    for i in range(numElements):
        indices = _getIndices(cElement)
        kmats[ene][indices[0],indices[1]] = _num(line[i*20:(i+1)*20])
        cElement += 1
    return cElement

def _getIndices(cElement):
    rows = 1
    cnt = 0
    while cnt < cElement:
        cnt += rows
        rows += 1
    ri = rows-2
    pSum = _aSum(rows-2)
    ci = cElement - pSum - 1
    return (ri, ci)

def _aSum(n):
    return n * (n+1) / 2

def _num(string):
    return float(string.replace("D", "E").replace(" ", ""))

def _flipCopyDiag(kmats):
    for ene in kmats:
        kmat = kmats[ene]
        numChannels = nw.shape(kmat)[0]
        numUniqueElements = _aSum(numChannels) 
        cElement = 1
        for i in range(numUniqueElements):
            indices = _getIndices(cElement)
            cElement += 1
            if indices[0] != indices[1]:
                kmat[indices[1],indices[0]] = kmat[indices[0],indices[1]]

def readkMats(fileName):
    kmats = {}
    with open(fileName, 'rb') as file:
        linNum = 0
        for i in range(0,5):
            linNum += 1
            file.readline()
        ene = None
        numCompleteLinesPerMat = 0
        numRemElements = 0
        oChanDesc = []
        lastNumChannels = 0
        for line in file:
            linNum += 1
            nums = filter(lambda x: x!="", line.split())
            if nums[0].find(".") == -1:
                numChannels = int(nums[0])
                if lastNumChannels != numChannels:
                    lastNumChannels = numChannels
                    if len(oChanDesc) == 0:
                        oChanDesc.append([numChannels,[0,1]])
                    else:
                        newStartInd = oChanDesc[-1][1][1]
                        newEndInd = newStartInd + 1
                        oChanDesc.append([numChannels,[newStartInd,newEndInd]])
                else:
                    oChanDesc[-1][1][1] += 1
                numUniqueElements = _aSum(numChannels)
                numCompleteLinesPerMat = numUniqueElements / 4
                numRemElements = numUniqueElements % 4
                lineI = 0
                ene = _num(nums[3])
                kmats[ene] = nw.sqZeros(numChannels)
                cElement = 1
            else:
                if lineI < numCompleteLinesPerMat:
                    _checkLineLength(line, linNum, 4)
                    cElement = _readLines(kmats, ene, line, 4, cElement)
                elif numRemElements > 0:
                    _checkLineLength(line, linNum, numRemElements)
                    cElement = _readLines(kmats, ene, line, numRemElements, cElement)
                lineI += 1
    _flipCopyDiag(kmats)
    return kmats, oChanDesc
