import os
from django.conf import settings
import ast
import json
import numpy as np
from quickdraw.models import Drawing
from quickdraw.serializers import DrawingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
import gensim.downloader as gensimapi
from quickdraw.parse_sentence import *

# global parameters
print("Loading word2vec model")
WORD_MODEL = gensimapi.load("glove-wiki-gigaword-50")
print("Loading complete")
OBJS = [l.strip() for l in open(os.path.join(settings.PROJECT_ROOT, "objs_list.csv"))]
NLP = spacy.load('en')


def most_similar_word(word):
    most_sim_word = (np.inf, '')
    for obj in OBJS:
        dist = WORD_MODEL.wmdistance(word, obj)
        if dist < most_sim_word[0]:
            most_sim_word = (dist, obj)
    return most_sim_word[1]


def strokes2svgpath(strokes):
    if isinstance(strokes, str):
        strokes = ast.literal_eval(strokes)

    svg_path = []
    for stroke in strokes:
        for ith, pos in enumerate(zip(stroke[0], stroke[1])):
            if ith == 0:
                p = "M%s %s"%(pos[0], pos[1])
            else:
                p = "L%s %s"%(pos[0], pos[1])
            svg_path.append(p)

    return " ".join(svg_path)


def process_sentence(sentence):
    doc = NLP(sentence)
    locs_d = sentence_to_loc(doc)
    mapped_locs_d = {}
    for key, item in locs_d.items():
        key = most_similar_word(key)
        mapped_locs_d[key] = item
    return mapped_locs_d

def word2Strokes(word):
    d = Drawing.objects.filter(word=word).order_by('?').first()
    serializer = DrawingSerializer(d)
    strokes = serializer.data['drawing']
    return strokes

def locationDict(preposition): # maps prepositions to directions
    dict = {"on" : ["up"], "above":["up"],"under" : ["down"], "beneath":["down"],"beside":["right","left"]}
    try:
        return random.choice(dict[preposition])
    except:
        return "right"

def phrase2Strokes(object,loc): #object = dict key, loc= value
    strokes = word2Strokes(object)
    print(strokes)


@api_view(['GET'])
def DetailDrawing(request, sentence, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    # TO DO tokenize, word2vector processing
    mapped_locs_d = process_sentence(sentence)
#    return Response(mapped_locs_d)

    try:
        # TEMP USE
        word = list(mapped_locs_d.keys())[0]
        #get by word
        strokes = word2Strokes(word)
        path = strokes2svgpath(strokes)
        return Response(path)
    except:
         # TO DO better error handling
        return Response("M150 0 L75 200 L225 200 Z")


class DrawingList(generics.ListCreateAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer
