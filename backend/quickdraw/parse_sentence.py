import spacy

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
        return [[[np, np], 'alone']], set(nps)

    for np in nps:
        if np.root.dep_ != "pobj":
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
                    parent_nouns.append(parent_noun)
                    break

            # if no parent, also document it
            if parent_noun == np.root:
                parent_nouns.append(parent_noun)

            first_level_pair = [[np.root, parent_noun], loc_preposition]
            first_level_pairs.append(first_level_pair)

    return first_level_pairs, set(parent_nouns)


def get_nouns(doc):
    word_locs = {}
    for token in list(doc):
        if token.pos_ == "NOUN":
            word_locs[token.text] = [['', 'alone']]
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
                