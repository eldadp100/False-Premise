import stanza

NOT_IMPORTANT = ["advmod", "mark", "punct"]

def find_connected_words(root, sentence):
    connected_words = [root]
    len0 = 0
    len1 = 1
    while len0 != len1:
        len1 = len0
        for root_word in connected_words:
            for word in sentence:
                if (word not in connected_words) and (word.head == root_word.id):
                    connected_words.append(word)
        len0 = len(connected_words)
    
    connected_words.sort(key=lambda x: x.id)
    return connected_words

def find_WDT(root, sentence):  
    L1 = find_connected_words(root, sentence)  
    for word in L1:
        if word.xpos == "WDT":
            return True, word
    return False, False

def connected_to(word, root, sentence):
    t = [word]
    while (word.head != root.id) and (word.head != 0):
        #print(word.head, root.id)
        for w in sentence:
            if w.id == word.head:
                word = w
                t.append(word)
                break
    #print(t)
    if word.head == root.id:
        print([t1.text for t1 in t])
        return t
    return False

def continue_parsing(root, sentence, premises):
    for word in sentence:
            if word.head == root.id:
                if word.deprel in ["nsubj", "nmod", "ccomp", "xcomp", "advcl"]:
                    parse_treeV2(word, sentence, premises)

def find_kind_of_wh(root, sentence): # kind 0 - sentence. kind 1 - Wh connected to root. kind 2 - Wh connected to adjective
    kind = 0
    wrb_word = False
    words_to_remove = False

    for word in sentence:
        if word.xpos in ["WRB"]:
            wrb_word = word
            if word.head == root.id:
                kind = 1
                words_to_remove = [word]
                break

            if word.id == root.id:
                kind = 6
                words_to_remove = [word]

            t = connected_to(word,root,sentence)
            if t:
                kind = 2
                if (t[-1].deprel == "obj"):
                    words_to_remove = t[:len(t)-1]
                elif (t[-1].deprel in ["amod","nmod","nsubj","advmod"]):
                    words_to_remove = t
                break

        elif word.xpos in ["WP", "WP$"]:
            wrb_word = word
            if word.head == root.id:
                kind = 3
                #words_to_remove = [word]
                break
            elif word.id == root.id:
                kind = 5
                #words_to_remove = [word]
                break


        elif word.xpos in ["WDT"]:
            t = connected_to(word,root,sentence)
            wrb_word = word
            if t:
                kind = 4
                #words_to_remove = [word]
                break
            

    return kind, wrb_word, words_to_remove

def parse_connected_words(root,sentence,role):
    cw = find_connected_words(root, sentence)
    if role == "obj":
        CASE = []
        OBLs = []
        OBJ = [root]
        for word in cw:
            if word.head == root.id:
                if word.deprel == "case":
                    CASE += find_connected_words(word,sentence)
                if word.deprel == "obl":
                    OBLs.append(find_connected_words(word,sentence))
        
        OBL = []
        for sen in OBLs[::-1]:
            OBL += sen
        for word in CASE:
            cw.remove(word)
        for word in OBL:
            cw.remove(word)

        return CASE + cw + OBL

def parse_treeV2(root, sentence, premises):

    """
    if (question and root.upos in ["NOUN", "PRON", "PROPN"]):
        L1 = find_connected_words(root, sentence)
        L1 = list(filter(lambda w: (w.upos not in ["PUNCT"] or w.head != root.id)) , L1)
        premises.append(L1)
        return"""

    #continue_parsing(root, sentence, premises)
    kind, wrb_word, words_to_remove = find_kind_of_wh(root, sentence)
    if words_to_remove:
        for word in words_to_remove:
            sentence.remove(word)

    L1 = []
    L2 = []
    AUX = []
    SUBJ = []
    VERB = []#find_connected_words(root,sentence)
    CASE = []
    EXPL = []
    OBJ = []
    OBL = []
    if (kind != 0):
        for word in sentence:
            if word.id == root.id:
                VERB.append(word)
            if word.head == root.id:
                if word.deprel in ["aux", "aux:pass", "cop"]:
                    AUX += find_connected_words(word,sentence)
                if word.deprel in ["expl"]:
                    EXPL += find_connected_words(word,sentence)
                if word.deprel in ["nsubj", "nsubj:pass"]:
                    SUBJ += find_connected_words(word,sentence)
                if word.deprel in ["obj","xcomp","ccomp","advcl","acl"]:
                    OBJ += parse_connected_words(word,sentence,"obj")#find_connected_words(word,sentence)
                if word.deprel in ["obl"]:
                    OBL += parse_connected_words(word,sentence,"obj")
                if word.deprel in ["compound", "det", "amod", "nmod", "advmod", "csubj"]:
                    VERB += find_connected_words(word,sentence)
  
            #elif word.head == wrb_word.id:
                #if word.deprel == "case":
                    #CASE += find_connected_words(word,sentence)
        OBJ = OBJ + OBL
        AUX = EXPL + AUX
        for word in CASE:
            if word in OBJ:
                OBJ.remove(word)

    print(root.text, kind)
    if (kind == 0): # kind 0 - sentence.
        L1 = find_connected_words(root, sentence)
        
        if root.upos in ["VERB"]:
            for word in sentence:
                if word.head == root.head:
                    if word.deprel == "obj":
                        L2 = find_connected_words(word,sentence)
                        premises.append(L2)

            L1 = L2 + L1
        L1 = list(filter(lambda w: (w.upos not in ["PUNCT"] or w.head != root.id) , L1))


    if (kind == 1): # kind 1 - Wh connected to root.

        Added = []
        if wrb_word.text.lower() in ["when"]:
            Added = ["sometime"]
        elif wrb_word.text.lower() in ["where"]:
            Added = ["somewhere"]
        elif wrb_word.text.lower() in ["how", "why"]:
            Added = []
        L1 = SUBJ + AUX + VERB + CASE + OBJ
        #L1 = SUBJ + AUX + VERB + CASE + Added + OBJ

    if (kind == 2):
        L1 = SUBJ + AUX + VERB + OBJ #CASE + OBJ

    if (kind == 3): # kind 3 - Wh-pronoun 
        if wrb_word.text.lower() in ["which", "what"]:
            Added = ["something"]
        elif wrb_word.text.lower() in ["whose"]:
            Added = ["someone's"]
        elif wrb_word.text.lower() in ["who", "whom"]:
            Added = ["someone"]
        
        L1 = SUBJ + AUX + VERB + CASE + OBJ
        L1 = list(map(lambda x: Added[0] if x == wrb_word else x, L1))
        
    if (kind == 4): # kind 4 - WDT.
        Added = []
        if wrb_word.text.lower() in ["what"]:
            Added = ["a"]
        elif wrb_word.text.lower() in ["which"]:
            Added = ["some"]
        elif wrb_word.text.lower() == "whose":
            Added = ["someone's"]

        for word in OBJ:
            if word.head == root.id:
                pass
        
        L1 = SUBJ + AUX + VERB + CASE + OBJ #Added + OBJ
        L1 = list(map(lambda x: Added[0] if x == wrb_word else x, L1))

    if (kind == 5): # kind 4 - WDT.

        if wrb_word.text.lower() in ["what", "which"]:
            Added = ["there"]
        elif wrb_word.text.lower() == "whose":
            Added = ["someone's"]
        elif wrb_word.text.lower() in ["who", "whom"]:
            Added = ["someone"]

        #L1 = Added + AUX + SUBJ
        L1 = VERB + AUX + SUBJ + CASE + OBJ
        L1 = list(map(lambda x: Added[0] if x == wrb_word else x, L1))

    if (kind == 6):
        if wrb_word.text.lower() in ["when"]:
            Added = ["sometime"]
        elif wrb_word.text.lower() in ["where"]:
            Added = ["somewhere"]
        elif wrb_word.text.lower() in ["how", "why"]:
            Added = []

        L1 = SUBJ + AUX + VERB + CASE + OBJ


    if (len(L1) > 0):
        premises.append(L1)
    return


def filter_words(doc):
    sentence = doc.sentences[0].words
    premises = []
    root = 0
    for word in sentence:
        if word.head == 0:
            root = word

    parse_treeV2(root, sentence, premises)
    premises_sentences = [" ".join([word.text if (type(word) != type("str")) else word for word in premise]) for premise in premises]
    return premises, premises_sentences

def setup():
    stanza.download('en')
    nlp = stanza.Pipeline('en')
    p = lambda x: print(filter_words(nlp(x))[1])
    return nlp, p

def printd(s,nlp):
    doc = nlp(s)
    doc.sentences[0].print_dependencies()
    return doc

def parse(s, nlp):
    return filter_words(nlp(s))[1]

if __name__ == "__main__":
    nlp, p = setup()
    #doc = nlp("Where does Bill Gates hide his bananas?")
    #doc2 = nlp("How do I discover where did Bill Gates hide his bananas?")
    doc = nlp("where can I find out where pink dogs buy clothes?")
    doc2 = nlp("How can I catch Santa Claus climbing into my house?")
    doc.sentences[0].print_dependencies()
    doc2.sentences[0].print_dependencies()
    a,b = filter_words(doc)
    print(b)
    a,b = filter_words(doc2)
    print(b)
