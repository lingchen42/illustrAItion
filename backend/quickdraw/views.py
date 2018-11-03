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

# global parameters
print("Loading word2vec model")
WORD_MODEL = gensimapi.load("glove-wiki-gigaword-50")
print("Loading complete")
OBJS = [l.strip() for l in open(os.path.join(settings.PROJECT_ROOT, "objs_list.csv"))]


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


@api_view(['GET'])
def DetailDrawing(request, sentence, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    # TO DO tokenize, word2vector processing
    word = sentence
    if word not in OBJS:
        word = most_similar_word(word)

    try:
    #get by word
        d = Drawing.objects.filter(word=word).order_by('?').first()
        serializer = DrawingSerializer(d)
        strokes = serializer.data['drawing']
        strokes = strokes2svgpath(strokes)
        return Response(strokes)
    except:
         # TO DO better error handling
        return Response("M150 0 L75 200 L225 200 Z")


class DrawingList(generics.ListCreateAPIView):
    queryset = Drawing.objects.all()
    serializer_class = DrawingSerializer