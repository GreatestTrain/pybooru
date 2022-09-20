POS_TAGS = '+{}'
NEG_TAGS = '+-{}'
FUZZY_TAGS = '+{}~'
END_TAGS = '+*{}'

def ttags(tags = [], string = ''):
    sss = ''
    for i in tags:
        sss += string.format(i)
    return sss

_pos_tags = lambda tags: ttags(tags, POS_TAGS)
_neg_tags = lambda tags: ttags(tags, NEG_TAGS)
# _fuz_tags = lambda tags: ttags(tags, FUZZY_TAGS)
# _end_tags = lambda tags: ttags(tags, END_TAGS)

def add_tags(pos_tags=[], neg_tags=[]): #fuz_tags=[], end_tags=[]):
    return '{}{}'.format(_pos_tags(pos_tags), _neg_tags(neg_tags)) #, _fuz_tags(fuz_tags), _end_tags(end_tags))