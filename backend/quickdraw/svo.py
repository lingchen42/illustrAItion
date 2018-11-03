
#SVO triples
import spacy
#import textacy
from textacy import extract
import random

spacy_nlp = spacy.load('en')

def svo(doc):
    """
    Given a paragraph, it will return a random (subject,verb,object) tuple from 1 sentence in the paragraph
    """
    text = spacy_nlp(doc)
    svos=extract.subject_verb_object_triples(text)
    x=list(svos)
    if len(x)>=1:
        return(random.choice(x))
        #print(random.choice(x))
    else:
        print("sorry, cannot extract svo")

#example
#svo("I eat apple.")
#svo("The rabbit likes carrots. I eat apple.")
#svo("Cat sits on table.")
