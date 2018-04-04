import sys
import re
import math

stopWordList2 = ["aaa","i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","can","will","just","don","should","now"]
stopWordList = ["the", "and", "to", "i", "a", "was", "in" ,"of", "we", "for","it", "at","is", "my" ,"that", "this", "had", "with", "were", "on", "they" ,"our","you", "there","t", "have", "be", "as", "when", "hotel", "chicago", "are","me", "s", "an", "night", "which", "what", "their", "us"]
stopWordList1 = ["aaa","a","about","above","across","after","again","against","all","almost","alone","along","already","also","although","always","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","best","better","between","big","both","but","by","c","came","can","cannot","case","cases","certain","certainly","clear","clearly","come","could","d","did","differ","different","differently","do","does","done","down","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","has","have","having","he","her","here","herself","high","high","high","higher","highest","him","himself","his","how","however","i","if","important","in","interest","interested","interesting","interests","into","is","it","its","itself","j","just","k","keep","keeps","kind","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","my","myself","n","necessary","need","needed","needing","needs","never","new","new","newer","newest","next","no","nobody","non","noone","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","our","out","over","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","she","should","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","still","such","sure","t","take","taken","than","that","the","their","them","then","there","therefore","these","they","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","way","ways","we","well","wells","went","were","what","when","where","whether","which","while","who","whole","whose","why","will","with","within","without","work","worked","working","works","would","x","y","year","years","yet","you","young","younger","youngest","your","yours","z"]

corpusSWL = ['hotel', 'the', 'room', 'chicago', 'stay', 't', 'would', 'we', 'staff', 'great', 'service', 'one', 'stayed', 'rooms', 's', 'like', 'night', 'it', 'get', 'location', 'time', 'my', 'desk', 'us', 'even', 'nice', 'could', 'bed', 'this', 'clean', 'also', 'good', 'front', 'back', 'got', 'experience', 'well', 'day', 'place', 'check', 'first', 'bathroom', 'comfortable', 'when', 'hotels', 'next', 'made', 'two', 'they','aaa','a']

totalDict = {}

class Document:
    global totalDict
    tf_label = ''
    pn_label = ''
    data = ''
    _id = ''

    def __init__(self, _id, tf_label, pn_label, data):
        self.tf_label = tf_label
        self.pn_label = pn_label
        self.data = data
        self._id = _id

    def countTerms(self, data):
        wordsDict = {}
        words = data.strip().split(' ')
        for word in words:
            #wordsDict[word] = wordsDict.get(word,0) + 1
            wordsDict[word] = wordsDict.get(word,0) + 1
            totalDict[word] = totalDict.get(word,0) + 1
        return wordsDict

def loadTrainData(filepath):
    with open(filepath) as trainFile:
        data = trainFile.read()
    return data

def removeStopWords(stopWordList, _data):
    res = []    
    data = _data.split(" ")
    data = filter(None, data)
    for word in data:
        if not word in stopWordList:
            res.append(word)
    return " ".join(res)

def prepareData(trainData):
    preData = []
    trainData = re.sub("  ",' ',trainData)
    documents = trainData.strip().split('\n')
    for D in documents:
        elements = D.split(' ', 3)
        _id = elements[0]
        tf_label = elements[1]
        pn_label = elements[2]
        data = elements[3]
        data = re.sub('-',' ',data)
        data = re.sub(r'\.',' ',data)
        data = re.sub(r"'",' ',data)
        data = re.sub(r"\"",' ',data)
        data = re.sub(r'[^a-zA-Z ]', r' ', data)
        #for stopWord in stopWordList:
        #    data = data.replace(stopWord," ")
        data = removeStopWords(stopWordList, data)
        #ata = removeStopWords(corpusSWL, data)
        data = map(lambda x: x.lower().strip(' '), data.split(" "))
        data = filter(None, data)
        data = ' '.join(data)
        data = _id + ';' + tf_label + ';' + pn_label + ';' + data
        preData.append(data)
    return preData

def buildTFStats(Documents, bagOfWords):
    #func to get True Fake Labels' statistics
    trueDict = {}
    fakeDict = {}
    trueCount = 0
    fakeCount = 0
    for w in bagOfWords:
        trueDict[w] = 0
        fakeDict[w] = 0
    for d in Documents:
        if d.tf_label == 'True':
            trueCount += 1
            for k, v in d.countTerms(d.data).iteritems():
                trueDict[k] += v
                totalDict[k] += v
        elif d.tf_label == 'Fake':
            fakeCount += 1
            for k, v in d.countTerms(d.data).iteritems():
                fakeDict[k] += v
                totalDict[k] += v
    return trueCount, trueDict, fakeCount, fakeDict 

def buildPNStats(Documents, bagOfWords):
    #func to get True Fake Labels' statistics
    posDict = {}
    negDict = {}
    posCount = 0
    negCount = 0
    for w in bagOfWords:
        posDict[w] = 0
        negDict[w] = 0
    for d in Documents:
        if d.pn_label == 'Pos':
            posCount += 1
            for k, v in d.countTerms(d.data).iteritems():
                posDict[k] += v
                totalDict[k] += v
        elif d.pn_label == 'Neg':
            negCount += 1
            for k, v in d.countTerms(d.data).iteritems():
                negDict[k] += v
                totalDict[k] += v
    return posCount, posDict, negCount, negDict

def getFreq():
    #sortedDict  = sorted(totalDict.items(), key=operator.itemgetter(1))
    s = [k for k in sorted(totalDict, key=totalDict.get, reverse=True)]
    print(s[1:50])
    text = ''
    #for x in s:
    #    text += x[0]+","+str(x[1])+"\n"
    #with open("dict.txt", "w+") as f:
    #    f.write(text)

def buildModel(preData):
    documents = []
    boW = []
    allWords = ''
    for d in preData:
        elements = d.split(';')
        _id = elements[0]
        tf_label = elements[1]
        pn_label = elements[2]
        data = elements[3]
        allWords = allWords + ' ' + data
        documents.append(Document(_id, tf_label, pn_label, data))
    boW = sorted(list(set(allWords.split(' '))))
    boW = boW[1:]
    #check bow and other integrity
    trueCount, trueDict, fakeCount, fakeDict = buildTFStats(documents,boW)
    posCount, posDict, negCount, negDict = buildPNStats(documents, boW)
    return trueCount, trueDict, fakeCount, fakeDict, posCount, posDict, negCount, negDict, boW, len(documents)

def writeModel(trueCount, trueDict, fakeCount, fakeDict, posCount, posDict, negCount, negDict, boW, N):
    model = []
    maxWordLength = max([len(w) for w in boW])
    cwidths = [maxWordLength+4, 10,10,10,10]
    model.append("P(True)=" + str(math.log(float(trueCount) / N)))
    model.append("\nP(Fake)=" + str(math.log(float(fakeCount) / N)))
    model.append("\nP(Pos)=" + str(math.log(float(posCount) / N)))
    model.append("\nP(Neg)=" + str(math.log(float(negCount) / N)))
    model.append('\nUnsmoothed:')
    formatString = "\n{0:<{w}} {1:<{True}} {2:<{Fake}} {3:<{Pos}} {4:<{Neg}}"
    model.append(formatString.format("Words", "True","Fake", "Pos","Neg",w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
    for word in boW:
        model.append(formatString.format(word, str(trueDict[word]),str(fakeDict[word]),str(posDict[word]),str(negDict[word]),w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
    #Smoothing (Laplacian)
    for w in trueDict.keys():
        trueDict[w] += 1
    for w in fakeDict.keys():
        fakeDict[w] += 1
    for w in posDict.keys():
        posDict[w] += 1
    for w in negDict.keys():
        negDict[w] += 1
    model.append('\nSmoothed:')
    model.append(formatString.format("Words", "True","Fake", "Pos","Neg",w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
    for word in boW:
        model.append(formatString.format(word, str(trueDict[word]),str(fakeDict[word]),str(posDict[word]),str(negDict[word]),w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
    totalTrueWords =  sum(trueDict.values())
    totalFakeWords =  sum(fakeDict.values()) 
    totalPosWords =  sum(posDict.values()) 
    totalNegWords =  sum(negDict.values())
    #rint(totalNegWords,totalPosWords,totalFakeWords,totalTrueWords)   
    model.append(formatString.format("Total", totalTrueWords, totalFakeWords, totalPosWords, totalNegWords, w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
    model.append('\nConditionals:')
    model.append(formatString.format("Words", "True","Fake", "Pos","Neg",w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4])) 
    for word in boW:
        #model.append(formatString.format(word, str(math.log(trueDict[word]/totalTrueWords)),str(math.log(fakeDict[word]/totalFakeWords)),str(math.log(posDict[word]/totalPosWords)),str(math.log(negDict[word]/totalNegWords)),w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))
        model.append(formatString.format(word, str(logProbFrac(trueDict[word],totalTrueWords)),str(logProbFrac(fakeDict[word],totalFakeWords)),str(logProbFrac(posDict[word],totalPosWords)),str(logProbFrac(negDict[word],totalNegWords)),w=cwidths[0],True=cwidths[1],Fake=cwidths[2],Pos=cwidths[3],Neg=cwidths[4]))   
    return model

def logProbFrac(num,den):
    return math.log(num) - math.log(den)

def main():
    trainFilePath = sys.argv[1]
    corpus = loadTrainData(trainFilePath)
    cleanData = prepareData(corpus)
    trueCount, trueDict, fakeCount, fakeDict, posCount, posDict, negCount, negDict, boW, N = buildModel(cleanData)
    model = writeModel(trueCount, trueDict, fakeCount, fakeDict, posCount, posDict, negCount, negDict, boW, N)
    with open("nbmodel.txt", "w+") as f:
        f.write("".join(model))
    #getFreq()

if __name__ == '__main__':
    main()
  


