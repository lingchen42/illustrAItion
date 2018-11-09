import ast
import random
from quickdraw.models import Drawing
from quickdraw.serializers import DrawingSerializer

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


def word2Strokes(word):
    print("Query:", word)
    d = Drawing.objects.filter(word=word).order_by('?').first()
    serializer = DrawingSerializer(d)
    strokes = serializer.data['drawing']
    try:
        strokes = ast.literal_eval(strokes)
    except:
        strokes = ""
    return strokes


def locationDict(preposition): # maps prepositions to directions
    dict = {"on" : ["up"], 
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
    print("In phrase2strokes:", object1, object2, "loc: ", loc)
    location = locationDict(loc)
    rm_inds = [0,0]
    print("generate strokes for ", object1, object2, location)
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


def locd2path(mapped_locs_ds):
    drawn = []
    root_strokes = []
    for mapped_locs_d in mapped_locs_ds:
        for word1 in mapped_locs_d.keys():
            strokes = []
            print("Draw:", drawn)
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

    return path