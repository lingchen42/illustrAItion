import os
import numpy as np
from django.conf import settings
import spacy
from translate import Translator
from langdetect import detect
import gensim.downloader as gensimapi
from nltk import Tree
from pattern.en import singularize

# global parameters
print("Loading word2vec model")
WORD_MODEL = gensimapi.load("glove-wiki-gigaword-50")
print("Loading complete")
try:
    OBJS = [l.strip() for l in open(os.path.join(settings.PROJECT_ROOT, "objs_list.csv"))]
except:
    OBJS = [l.strip() for l in open(os.path.join("../project/", "objs_list.csv"))]
SPECIAL_WORDS = ['hack', 'hacker', 'vandy', 'vanderbilt', 'hackthon']
NLP = spacy.load('en')
HUMAN_LIST = ['i', 'you', 'he', 'she', 'girl', 'boy', 'lady', 'guy', 'person', 
               'we', 'us', 'man', 'woman', 'human']

LOC_LIST = {"on" : ["up"], 
            "above":["up"],
            "alone": ['on'],
            "under" : ["down"],
            "below":["down"],
            "beneath":["down"],
            "beside":["right","left"],
            "by":["left","right"],
            "against":["right","left"],
            "before":["left","right"],
            "after":["left","right"],
            "over":["up"],
            "alone":["alone"],
            "in":["up"], 
            "at":["right", "left"], 
            'near':['right', 'left'], 
            'behind':['right']}

OBJ_D = { 'animal migration':['migration'],
          'hockey stick': ['hockey', 'stick'],
          'The Great Wall of China': ['china', 'wall'],
          'tennis racquet':['tennis', 'racquet'],
          'teddy-bear':['teddy', 'bear', 'doll'],
          'light bulb':['light', 'bulb'],
          'wine bottle':['wine', 'bottle'],
          'power outlet':['power'],
          'picture frame':['picture', 'frame'],
          'diving board':['diving', 'board'],
          'flip flops':['flip-flop'],
          'hot air balloon':['ballon'],
          'alarm clock':['alarm', 'clock'],
          'washing machine':['washer'],
          'traffic light':['traffic'],
          'string bean':['bean'],
          'smiley face':['smiling', 'smile'],
          'palm tree':['palm'],
          'pickup truck':['pickup', 'truck'],
          'flying saucer':['ufo'],
          'sleeping bag':['sleep'],
          'frying pan':['pan', 'frying'],
          'cruise ship':['cruise', 'ship'],
          'sea turtle':['turtle'],
          'swing set':['swing'],
          'fire hydrant':['hydrant'],
          'bottlecap': ['cap'],
          'soccer ball':['soccer', 'ball'],
          'school bus':['bus'],
          'cell phone':['cellphone'],
          'paper clip':['clip'],
          'house plant':['plant'],
          'garden hose':['hose'],
          'ice cream':['icecream'],
          'birthday cake':['cake'],
          'The Eiffel Tower':['paris', 'tower', 'eiffel'],
          'stop sign':['stop', 'sign'],
          'hockey puck':['puck'],
          'coffee cup':['coffee', 'cup'],
          'golf club':['golf'],
           'The Mona Lisa':['painting'],
           'wine glass':['glass'],
           'paint can':['paint'],
           'ceiling fan':['fan'],
           'hot tub':['bathtub', 'tub'],
           'see saw':['seesaw'],
           'baseball bat':['bat'],
           'police car':['police'],
           'roller coaster':['roller', 'coaster'],
           'remote control':['control', 'controller'],
           'floor lamp':['lamp'],
           'hot dog':['hotdog']
          }

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_


def get_first_level_pairs(doc):
    '''
    Returns 
    list of [[children_noun, parent_noun], loc_preposition]
    parent nouns
    '''
    first_level_pairs = []
    parent_nouns = []
    nps = list(doc.noun_chunks)

    if len(nps) == 1:
        np = nps[0]
        return [[[np.root, np.root], 'alone']], set([nps[0].root])

    for np in nps:
        if np.root.dep_ == 'nsubj':
            nsubj = np.root
            continue
        elif np.root.dep_ != "pobj":
            continue
        else:
            token = np.root
            loc_preposition = np.root.head.text
            obj = token.text
            parent_noun = np.root
            while token.head != token:  #  token is not root
                token = token.head
                if token.pos_ == 'NOUN':
                    parent_noun = token
                    break

            # if no parent, also document it
            if parent_noun == np.root:
                try:
                    parent_noun = nsubj
                except:
                    pass
            
            if loc_preposition not in LOC_LIST:
                if loc_preposition == 'of':
                    print("of detected, setting parent noun back to , setting loc back to alone", np.root)
                    parent_noun = np.root
                    loc_preposition = 'alone'
            
            parent_nouns.append(parent_noun)
            first_level_pair = [[np.root, parent_noun], loc_preposition]
            first_level_pairs.append(first_level_pair)

    return first_level_pairs, set(parent_nouns)


def get_nouns(doc):
    word_locs = {}
    nps = [ n.root for n in list(doc.noun_chunks)]
    for token in nps:
        if token.pos_ == "NOUN":
            if token.text in (OBJS + SPECIAL_WORDS):
                print(token)
                word_locs[token.text] = [['', 'alone']]
            else:
                print("find similar ", token)
                word_locs[most_similar_word(token.text)] = [['', 'alone']]
    return word_locs


def sentence_to_loc(doc):
    '''
    Only works for noun dependence tree with depth of 2
    '''
    first_level_pairs, parent_nouns = get_first_level_pairs(doc)
    second_level_pairs = {}

    for parent_noun in parent_nouns:
        second_level_pairs[parent_noun.text] = []
        for pair in first_level_pairs:
            pair_child = pair[0][0]
            pair_parent = pair[0][1]
            if pair_parent == parent_noun:
                # if parent == child, replace the child as ''
                if pair_child == pair_parent:
                    entry = ['', pair[1]]
                else:
                    entry = [pair_child.text, pair[1]]
                second_level_pairs[parent_noun.text].append(entry)
    
    return second_level_pairs


def most_similar_word(word):
    if word.lower() in (OBJS + SPECIAL_WORDS):
        return word

    most_sim_word = (np.inf, '')
    for obj in OBJS:
        if obj in OBJ_D.keys():
            tmp_objs = OBJ_D[obj]
            tmp_min_dist = np.inf
            for tmp_obj in tmp_objs:
                tmp_dist = WORD_MODEL.distance(word, tmp_obj)
                if tmp_dist < tmp_min_dist:
                    tmp_min_dist = tmp_dist
            dist = tmp_min_dist

        else:
            dist = WORD_MODEL.distance(word, obj)

        if dist < most_sim_word[0]:
            most_sim_word = (dist, obj)

    return most_sim_word[1]


def translate(sentence):
    if detect(sentence) == 'zh-cn':
        print("Translating Chinese")
        # try translatin chinese
        sentence = Translator(from_lang='zh',to_lang="en").translate(sentence).lower()
    return sentence


def manual_processing(sentence):
    doc = NLP(sentence)
    new_doc = []
    for x in doc:
        if (x.pos_ == "NOUN") and (x.text != 'grass'):
            x_text = singularize(x.text)
        else:
            x_text = x.text

        if x_text in HUMAN_LIST:
            new_doc.append('face')
        elif x_text == 'sky':
            new_doc.append('cloud')
        # elif x.pos_ == "VERB":  # don't know how to handle verb yet
        #     continue
        else:
            new_doc.append(x_text)
    return ' '.join(new_doc)


def process_sentence(sentence):
    sentence = sentence.lower()
    sentence = translate(sentence)
    sentence = manual_processing(sentence)
    print("Processed sentence:", sentence)

    # Handle octocat
    if sentence == 'octocat':
        return ''

    doc = NLP(sentence)
    locs_d = sentence_to_loc(doc)
    mapped_locs_d = {}
    for key, items in locs_d.items():
        key = most_similar_word(key)
        mapped_items = []
        for item in items:
            if item[0]:
                mapped_items.append([most_similar_word(item[0]), item[1]])
            else:
               mapped_items.append([item[0], item[1]]) 
        mapped_locs_d[key] = mapped_items

    if not mapped_locs_d:
        mapped_locs_d = get_nouns(NLP(sentence))

    return mapped_locs_d


def process_paragraph(paragraph):
    paragraph = paragraph.replace(",", ".")
    doc = NLP(paragraph)
    sentences = [sent.string.strip() for sent in doc.sents]
    mapped_locs_ds = []
    for sentence in sentences:
        mapped_locs_ds.append(process_sentence(sentence))
    return mapped_locs_ds