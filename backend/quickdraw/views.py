import os
from django.conf import settings
import ast
import json
import numpy as np
import random
from quickdraw.models import Drawing
from quickdraw.serializers import DrawingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
import gensim.downloader as gensimapi
from quickdraw.parse_sentence import *
from translate import Translator
from langdetect import detect

# global parameters
print("Loading word2vec model")
WORD_MODEL = gensimapi.load("glove-wiki-gigaword-50")
print("Loading complete")
OBJS = [l.strip() for l in open(os.path.join(settings.PROJECT_ROOT, "objs_list.csv"))]
OBJS.extend(['hack', 'vandy', 'vanderbilt', 'hackthon'])
NLP = spacy.load('en')
HUMAN_LIST = ['i', 'you', 'he', 'she', 'girl', 'boy', 'lady', 'guy', 'person', 
               'we', 'us']


def strokes2svgpath(strokes):
    svg_path = []
    for stroke in strokes:
        for ith, pos in enumerate(zip(stroke[0], stroke[1])):
            if ith == 0:
                p = "M%s %s"%(pos[0], pos[1])
            else:
                p = "L%s %s"%(pos[0], pos[1])
            svg_path.append(p)

    return " ".join(svg_path)


def most_similar_word(word):
   if word.lower() in OBJS:
       return word

   most_sim_word = (np.inf, '')
   for obj in OBJS:
       dist = WORD_MODEL.wmdistance(word, obj)
       if dist < most_sim_word[0]:
           most_sim_word = (dist, obj)

#    if not most_sim_word[1]:
   return most_sim_word[1]


def process_sentence(sentence):
    doc = NLP(sentence)
    # detect human words
    new_doc = ' '.join(['face' if (x.text in HUMAN_LIST) else x.text for x in doc])
    new_doc = NLP(new_doc)
    # remove verbs
    new_doc = ' '.join([x.text for x in new_doc if x.pos_ != "VERB"])

    doc = NLP(new_doc)
    locs_d = sentence_to_loc(doc)
    mapped_locs_d = {}
    for key, items in locs_d.items():
        key = most_similar_word(key)
        mapped_items = []
        for item in items:
            mapped_items.append([most_similar_word(item[0]), item[1]])
        mapped_locs_d[key] = mapped_items
    print(mapped_locs_d)
    return mapped_locs_d


def word2Strokes(word):
    d = Drawing.objects.filter(word=word).order_by('?').first()
    serializer = DrawingSerializer(d)
    strokes = serializer.data['drawing']
    try:
        strokes = ast.literal_eval(strokes)
    except:
        strokes = ""
    return strokes


def locationDict(preposition): # maps prepositions to directions
    dict = {"on" : ["up"], "above":["up"],"under" : ["down"],"below":["down"],
        "beneath":["down"],"beside":["right","left"],"by":["left","right"],
        "against":["right","left"],"before":["left","right"],"after":["left","right"],
        "over":["up"],"alone":["alone"], "in":["up"], 
        "at":["right", "left"], 'near':['right', 'left'], 'behind':['right']}
    try:
        return random.choice(dict[preposition])
    except:
        return "alone"


def getMaxBound(strokes, coord):
    mx = 0
    if coord == "x":
        mx = max([max(stroke[0]) for stroke in strokes])
    else:
        mx = max([max(stroke[1]) for stroke in strokes])
    return mx


def adjustStrokes(strokes, amount, coord):
    strokes = strokes.copy()
    if coord == "x":
        for stroke in strokes:
            stroke[0] = [x+amount for x in stroke[0]]
    else:
        for stroke in strokes:
            stroke[1] = [y+amount for y in stroke[1]]
    return strokes


def phrase2Strokes(strokes,object1,object2,loc,drawn): #object = dict key, loc= value
    location = locationDict(loc)
    rm_inds = [0,0]
    print(object1, object2, location)
    if location == "up":
        if drawn == "obj1":
            rm_inds[0] = len(strokes)
        strokes.extend(word2Strokes(object1))
        if drawn == "obj1":
            rm_inds[1] = len(strokes)
        elif drawn == "obj2":
            rm_inds[0] = len(strokes)
        strokes.extend(adjustStrokes(word2Strokes(object2),getMaxBound(strokes,"y"),"y"))
        if drawn == "obj2":
            rm_inds[1] = len(strokes)
    elif location == "down":
        if drawn == "obj2":
            rm_inds[0] = len(strokes)
        strokes.extend(word2Strokes(object2))
        if drawn == "obj1":
            rm_inds[0] = len(strokes)
        elif drawn == "obj2":
            rm_inds[1] = len(strokes)
        strokes.extend(adjustStrokes(word2Strokes(object1),getMaxBound(strokes,"y"),"y"))
        if drawn == "obj1":
            rm_inds[1] = len(strokes)
    elif location == "right":
        if drawn == "obj2":
            rm_inds[0] = len(strokes)
        strokes.extend(word2Strokes(object2))
        if drawn == "obj1":
            rm_inds[0] = len(strokes)
        elif drawn == "obj2":
            rm_inds[1] = len(strokes)
        strokes.extend(adjustStrokes(word2Strokes(object1),getMaxBound(strokes,"x"),"x"))
        if drawn == "obj1":
            rm_inds[1] = len(strokes)
    elif location == "left":
        if drawn == "obj1":
            rm_inds[0] = len(strokes)
        strokes.extend(word2Strokes(object1))
        if drawn == "obj1":
            rm_inds[1] = len(strokes)
        elif drawn == "obj2":
                rm_inds[0] = len(strokes)
        strokes.extend(adjustStrokes(word2Strokes(object2),getMaxBound(strokes,"x"),"x"))
        if drawn == "obj2":
            rm_inds[1] = len(strokes)
    else:
        strokes.extend(word2Strokes(object1))
        if drawn == "obj1":
            rm_inds = [0,len(strokes)]
    if drawn != "none": #if object1 or object2 was drawn in a previous call, remove strokes
        if rm_inds[0] == 0:
            del strokes[:rm_inds[1]]
        else:
            del strokes[rm_inds[0]:rm_inds[1]]
    return strokes


@api_view(['GET'])
def DetailDrawing(request, sentence, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    # TO DO tokenize, word2vector processing
    sentence = sentence.lower()
    if detect(sentence) == 'zh-cn':
        print("Translating Chinese")
        # try translatin chinese
        sentence = Translator(from_lang='zh',to_lang="en").translate(sentence).lower()

    print(sentence)

    # Handle octocat
    if "octo" in sentence:
        return Response([''])
    
    # manual correct map some words
    sentence = sentence.replace('sky', 'cloud')

    mapped_locs_d = process_sentence(sentence)
    print(mapped_locs_d)
    if not mapped_locs_d:
        mapped_locs_d = get_nouns(NLP(sentence))

    try:
        drawn = []
        root_strokes = []
        for word1 in mapped_locs_d.keys():
            strokes = []
            print(drawn)
            if word1 not in drawn:
                print(mapped_locs_d[word1])
                for pair in mapped_locs_d[word1]:
                    if pair[0] not in drawn and (word1 not in drawn):
                        drawn.append(pair[0])
                        drawn.append(word1)
                        strokes= phrase2Strokes(strokes,word1,pair[0],pair[1],"none")
                    elif pair[0] not in drawn and (word1 in drawn):
                        drawn.append(pair[0])
                        strokes= phrase2Strokes(strokes,word1,pair[0],pair[1],"obj1")
                    elif pair[0] in drawn and (word1 not in drawn):
                        drawn.append(word1)
                        strokes= phrase2Strokes(strokes,word1,pair[0],pair[1],"obj2")
                # update root strokes
                root_strokes.append(strokes.copy())

        # use margin between noun chunks
        margin = 20
        if len(root_strokes) == 1:
            path = strokes2svgpath(strokes)
        else:
            for idx, strokes_pair in enumerate(zip(root_strokes, root_strokes[1:])):
                strokes1, strokes2 = strokes_pair
                if idx == 0:
                    final_strokes = strokes1.copy()
                mx = getMaxBound(final_strokes, "x") + margin
                final_strokes.extend(adjustStrokes(strokes2.copy(), mx, "x"))
            path = strokes2svgpath(final_strokes) 
            print(path)

        return Response([path])
    except:
         # TO DO better error handling
        return Response([strokes2svgpath(word2Strokes('hack'))])


class DrawingList(generics.ListCreateAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer