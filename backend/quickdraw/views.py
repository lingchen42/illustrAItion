from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from quickdraw.parse_sentence import process_paragraph
from quickdraw.sen2path import locd2path


@api_view(['GET'])
def DetailDrawing(request, sentence, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    mapped_locs_ds = process_paragraph(sentence)
    print(mapped_locs_ds)

    try:
        path = locd2path(mapped_locs_ds)
        return Response([path])
    except:
         # TO DO better error handling
         return Response([''])

#class DrawingList(generics.ListCreateAPIView):
#    queryset = Drawing.objects.all()
#    serializer_class = DrawingSerializer