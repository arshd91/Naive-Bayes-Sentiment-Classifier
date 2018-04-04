import re
import sys

stopWordList2 = ["aaa","i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","can","will","just","don","should","now"]
stopWordList = ["the", "and", "to", "i", "a", "was", "in" ,"of", "we", "for","it", "at","is", "my" ,"that", "this", "had", "with", "were", "on", "they" ,"our","you", "there","t", "have", "be", "as", "when", "hotel", "chicago", "are","me", "s", "an", "night", "which", "what", "their", "us"]
stopWordList1 = ["aaa","a","about","above","across","after","again","against","all","almost","alone","along","already","also","although","always","among","an","and","another","any","anybody","anyone","anything","anywhere","are","area","areas","around","as","ask","asked","asking","asks","at","away","b","back","backed","backing","backs","be","became","because","become","becomes","been","before","began","behind","being","beings","best","better","between","big","both","but","by","c","came","can","cannot","case","cases","certain","certainly","clear","clearly","come","could","d","did","differ","different","differently","do","does","done","down","down","downed","downing","downs","during","e","each","early","either","end","ended","ending","ends","enough","even","evenly","ever","every","everybody","everyone","everything","everywhere","f","face","faces","fact","facts","far","felt","few","find","finds","first","for","four","from","full","fully","further","furthered","furthering","furthers","g","gave","general","generally","get","gets","give","given","gives","go","going","good","goods","got","great","greater","greatest","group","grouped","grouping","groups","h","had","has","have","having","he","her","here","herself","high","high","high","higher","highest","him","himself","his","how","however","i","if","important","in","interest","interested","interesting","interests","into","is","it","its","itself","j","just","k","keep","keeps","kind","knew","know","known","knows","l","large","largely","last","later","latest","least","less","let","lets","like","likely","long","longer","longest","m","made","make","making","man","many","may","me","member","members","men","might","more","most","mostly","mr","mrs","much","must","my","myself","n","necessary","need","needed","needing","needs","never","new","new","newer","newest","next","no","nobody","non","noone","not","nothing","now","nowhere","number","numbers","o","of","off","often","old","older","oldest","on","once","one","only","open","opened","opening","opens","or","order","ordered","ordering","orders","other","others","our","out","over","p","part","parted","parting","parts","per","perhaps","place","places","point","pointed","pointing","points","possible","present","presented","presenting","presents","problem","problems","put","puts","q","quite","r","rather","really","right","right","room","rooms","s","said","same","saw","say","says","second","seconds","see","seem","seemed","seeming","seems","sees","several","shall","she","should","show","showed","showing","shows","side","sides","since","small","smaller","smallest","so","some","somebody","someone","something","somewhere","state","states","still","still","such","sure","t","take","taken","than","that","the","their","them","then","there","therefore","these","they","thing","things","think","thinks","this","those","though","thought","thoughts","three","through","thus","to","today","together","too","took","toward","turn","turned","turning","turns","two","u","under","until","up","upon","us","use","used","uses","v","very","w","want","wanted","wanting","wants","was","way","ways","we","well","wells","went","were","what","when","where","whether","which","while","who","whole","whose","why","will","with","within","without","work","worked","working","works","would","x","y","year","years","yet","you","young","younger","youngest","your","yours","z"]

corpusSWL = ['hotel', 'the', 'room', 'chicago', 'stay', 't', 'would', 'we', 'staff', 'great', 'service', 'one', 'stayed', 'rooms', 's', 'like', 'night', 'it', 'get', 'location', 'time', 'my', 'desk', 'us', 'even', 'nice', 'could', 'bed', 'this', 'clean', 'also', 'good', 'front', 'back', 'got', 'experience', 'well', 'day', 'place', 'check', 'first', 'bathroom', 'comfortable', 'when', 'hotels', 'next', 'made', 'two', 'they','aaa','a']

def removeStopWords(stopWordList, _data):
    res = []    
    data = _data.split(" ")
    data = filter(None, data)
    for word in data:
        if not word in stopWordList:
            res.append(word)
    return " ".join(res)

def loadModel(path):
    trueDict = {}
    fakeDict = {}
    posDict = {}
    negDict = {}
    with open(path,'r') as f:
        modelText = filter(None,f.read().strip().split('\n'))
        prioris = [float(x.strip().split('=')[1]) for x in modelText[:4]]
        index = modelText.index("Conditionals:")
        for d in modelText[index+2:]:
            dataRow = filter(None,d.strip().split(' '))
            trueDict[dataRow[0]] = dataRow[1]
            fakeDict[dataRow[0]] = dataRow[2]
            posDict[dataRow[0]] = dataRow[3]
            negDict[dataRow[0]] = dataRow[4]
    return trueDict,fakeDict, posDict, negDict, prioris

def prepareData(testData):
    preData = []
    testData = re.sub("  ",' ',testData)
    documents = testData.strip().split('\n')
    for D in documents:
        elements = D.split(' ',1)
        _id = elements[0]
        data = elements[1]
        data = re.sub('-',' ',data)
        data = re.sub(r'\.',' ',data)
        data = re.sub(r"'",' ',data)
        data = re.sub(r"\"",' ',data)
        data = re.sub(r'[^a-zA-Z ]', r' ', data)
        #for stopWord in stopWordList:
        #    data = data.replace(stopWord," ")
        data = removeStopWords(stopWordList, data)
        #data = removeStopWords(corpusSWL, data)
        data = map(lambda x: x.lower().strip(' '), data.split(" "))
        data = filter(None, data)
        data = ' '.join(data)
        data = _id + ';' + data
        preData.append(data)
    return preData

def classify(trueDict,fakeDict, posDict, negDict, prioris, testCorpus):
    output = ''
    for d in testCorpus:
        #print(d)
        trueP, fakeP, posP, negP = 0.0, 0.0, 0.0, 0.0
        elements = d.split(';')
        _id = elements[0]
        data = elements[1].strip().split(" ")
        for word in data:
            if word in trueDict.keys():
                trueP += float(trueDict[word])
            if word in fakeDict.keys():
                fakeP += float(fakeDict[word])
            if word in posDict.keys():
                posP += float(posDict[word])
            if word in negDict.keys():
                negP += float(negDict[word])
        trueP += prioris[0]
        fakeP += prioris[1]
        posP += prioris[2]
        negP += prioris[3]
        prediction = vote(trueP,fakeP, posP, negP)
        output += str(_id + ' ' + prediction +'\n')
    return output


def vote(p1, p2, p3, p4):
    ans = ''
    if p1>p2:
        ans = 'True '
    else:
        ans = 'Fake '
    if p3>p4:
        ans += 'Pos'
    else:
        ans += 'Neg'
    return ans

def loadFile(filepath):
    with open(filepath) as testFile:
        data = testFile.read()
    return data

def main():
    trueDict,fakeDict, posDict, negDict, prioris = loadModel("nbmodel.txt")
    testFile = loadFile(sys.argv[1])
    testCorpus = prepareData(testFile)
    #print(testCorpus)
    result = classify(trueDict,fakeDict, posDict, negDict, prioris, testCorpus)
    with open("nboutput.txt", "w+") as f:
        f.write(result)

if __name__ == '__main__':
    main()