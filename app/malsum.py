import regex
import math
from collections import Counter
from mlmorph import Analyser

sw = "കാണാന് | നിന്ന് | കുറഞ്ഞ | മുഴുവന് | കൂടാതെ | ആദ്യം | ഈ | കൂടുതല് | താങ്കള് | എന്നാല് | അതിനു | ശേഷം " \
     "| ചെയ്യുന്നു | ഇവിടത്തെ | വേണ്ടി | ഏറ്റവും | ഇതില് | വേണ്ടിയും | ആണ് | സ്ഥിതിചെയ്യുന്നു | സ്ഥിതി" \
     " | സ്ഥിതിചെയ്യുന്ന | ചെയ്യണം | നമ്മുടെ | ഇപ്പോള് | ഒരു | തന്റെ | ചെയ്യുന്ന | എന്ന | ചെയ്യുന്നത് |" \
     " ഉണ്ട് | മുന്പ് | മുമ്പ് | കൂടെ | ചേര്ത്തു | ഇപ്രകാരം | എന്നിവയുടെ | " \
     "കഴിയും | എന്നീ | ഇതാണ് | വളരെ | കാരണം | ഇവിടത്തെ | എപ്പോഴും | കൊണ്ട് | നല്ല | ധാരാളം |" \
     " എപ്പോഴും | ഇവ | കാരണം | ഇതു | മാത്രമല്ല | മറ്റു | എന്നിവ | കൂടിയാണ് | ഇടയില് | ഇല്ല | എന്നാണ് | എന്നു | കുറച്ച് " \
     "| അതായത് | എന്തെന്നാല് | എന്നറിയപ്പെടുന്നു | കിടക്കുന്ന | പോയാല് | ഇത് | എല്ലാ | വേണ്ടി | ഇവിടെ | വരുന്നു " \
     "| പോലുള്ള  | വലിയ | പറഞ്ഞ് | ഇതിനെ | കൊടുത്തിട്ടും | എന്ന് | വേണം | ഒരുപോലെ |" \
     " ഒരു പോലെ | കാര്യമാണ് | കഴിയുന്നു | വളരെ | അധികം | വളരെ അധികം | വളരെയധികം | പോയി |" \
     " ഉണ്ടാകുന്നുണ്ട് | പക്ഷേ | അതേ | കൊണ്ട് | ഏത് | നിന്നും | എത്താന് | അടുത്ത് | ആയി " \
     "| എന്നു പറയുന്നു | ഇപ്പോൾ | ഏകദേശം | എന്നുപറയുന്നു | കാണാൻ | ആ | വിവിധ | ഇതിന്റെ | നിന്നു | ഇതിന് " \
     "| അടുത്ത | അടുത്തുള്ള | പല | പ്രധാന | നിലനിൽക്കുന്ന | നിലനിൽക്കുന്നത് | മുതലായവ | മുതലായവക്ക് " \
     "| വേണ്ട | പ്രാധാന്യം"


def lev_sim(x, y):
    m = max(x, y)
    return round(abs(x - y) / m, 2)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    word = regex.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)


def get_result(content_a, content_b):
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result


analyser = Analyser()


def split_sentence(text):
    text = text.strip()
    words = regex.split(r'(\s+)', text)
    temp = []
    delim = ",.!?/&-:;@'..."
    for word in words:
        strip_num = regex.sub('[0-9]+\S+', '', word)
        strip_whitespace = regex.sub('\s+', '', strip_num)
        temp.append(strip_whitespace)
    words = temp
    words = [x for x in words if x not in delim]  # strip delim
    fin = []
    for i in words:
        # remove stop words
        morpheme = None
        if i not in sw:
            morpheme = analyser.analyse(i)  # split word into morpheme
        if morpheme:
            # take only the first morpheme and also remove metadata
            y = regex.match(r'(.*?)<', morpheme[0][0]).group(1)
            fin.append(y)

    return fin


def split_text(text):
    # remove unnecessary unicode chars
    text = text.replace('\u200d', '')
    text = text.replace('\u200c', '')
    # TODO: find a way to detect abbreviations
    text = text.split('.')[:-1]
    words = Counter()
    counter = 1
    sentences = {}
    length = 0
    for i in text:
        s = split_sentence(i)
        length += len(s)
        sentences.update({counter: [s, i]})
        words.update(s)
        counter = counter + 1
    ret = [sentences, words, length]
    return ret


def affinity(dictionary, counter, length):
    aff = {}
    for i in dictionary:
        x = 0
        words = dictionary[i][0]
        for j in words:
            x += counter[j] / length
        aff.update({i: round(x, 3) / 10})
    return aff


article = """"""


def summarize(text, limit):
    dictionary, counter, length = split_text(text)
    aff = affinity(dictionary, counter, length)
    aff = {k: v for k, v in sorted(aff.items(), key=lambda item: item[1])}
    final = {}
    count = 0
    for i in reversed(list(aff.keys())):
        if count == limit+5:
            break
        else:
            final.update({i: dictionary[i]})
        count += 1
    ret = []
    for i in sorted(list(final.keys())):
        ret.append([i, final[i][1].strip()])

    summary = [ret[0]]
    for i in range(1, len(ret)):
        for j in summary:
            if get_result(ret[i][1], j[1]) > 0.66:
                break
            elif ret[i] not in summary:
                summary.append(ret[i])
    # for i in range(len(summary)):
    #     print(summary[i][0], summary[i][1].strip())

    return summary[:limit]

