import json

lang1 = "eng"
lang2 = "spa"

def tokenize(text):
    type = -1
    start = -1
    answer = []

    for i, c in enumerate(text):
        if c.isalpha():
            if type != 0:
                type = 0
                if start > -1:
                    answer.append((start, i))
                start = i
        elif not c.isspace():
            if type != 1:
                type = 1
                if start > -1:
                    answer.append((start, i))
                start = i
        else:
            if start > -1:
                answer.append((start, i))
            start = -1
            type = -1

    if start > -1:
        answer.append((start, len(text)))
    
    return answer

class Mapping:
    def __init__(self, a, bs):
        self.a = set()
        self.a.update(a)
        self.b = set()
        self.b.update(bs)
    
    def geta(self):
        return self.a
    
    def adda(self, a):
        self.a.add(a)
    
    def getb(self):
        return self.b
    
    def addb(self, b):
        self.b.add(b)
    
    def add(self, mapping):
        self.a.update(mapping.a)
        self.b.update(mapping.b)

    def arange(self):
        return range(min(self.a), max(self.a)+1)

    def brange(self):
        return range(min(self.b), max(self.b)+1)

    def __str__(self):
        return str(self.a) + ' -> ' + str(self.b)

def build_graph(pairs, a, b):
    # Build node connections
    amap = {}
    bmap = {}
    for p in pairs:
        parts = p.split('-')
        x = int(parts[0])
        y = int(parts[1])
        if x >= a or y >= b:
            # ERROR? this does happen, but I don't know why
            continue
        if not x in amap.keys():
            amap[x] = []
        amap[x].append(y)
        if not y in bmap.keys():
            bmap[y] = []
        bmap[y].append(x)

    # Add empty nodes
    for i in range(a):
        if i not in amap.keys():
            amap[i] = []
    for i in range(b):
        if i not in bmap.keys():
            bmap[i] = []

    # Build connected sets for each node
    agroups = [Mapping([i], amap[i]) for i in range(a)]
    bgroups = [Mapping(bmap[i], [i]) for i in range(b)]
    
    # Combine groups based on mapping
    for i in range(a):
        group = agroups[i]
        bs = list(group.getb())
        for j in bs:
            if not bgroups[j] is group:
                group.add(bgroups[j])
                bgroups[j] = group
    for i in range(b):
        group = bgroups[i]
        ags = list(group.geta())
        for j in ags:
            if not agroups[j] is group:
                group.add(agroups[j])
                agroups[j] = group
    
    # Combine groups based on overlap
    for i in range(a):
        group = agroups[i]
        for j in group.arange():
            if not agroups[j] is group:
                group.add(agroups[j])
                agroups[j] = group
    for i in range(b):
        group = bgroups[i]
        for j in group.brange():
            if not bgroups[j] is group:
                group.add(bgroups[j])
                bgroups[j] = group

    # Combine groups based on lack
    for i in range(a):
        group = agroups[i]
        if len(group.getb()) == 0:
            if i>0 and not group is agroups[i-1]:
                group.add(agroups[i-1])
                agroups[i-1] = group
            if i<a-1 and not group is agroups[i+1]:
                group.add(agroups[i+1])
                agroups[i+1] = group
    for i in range(b):
        group = bgroups[i]
        if len(group.geta()) == 0:
            if i>0 and not group is bgroups[i-1]:
                group.add(bgroups[i-1])
                bgroups[i-1] = group
            if i<b-1 and not group is bgroups[i+1]:
                group.add(bgroups[i+1])
                bgroups[i+1] = group
    
    # Combine groups based on mapping again
    for i in range(a):
        group = agroups[i]
        bs = list(group.getb())
        for j in bs:
            if not bgroups[j] is group:
                group.add(bgroups[j])
                bgroups[j] = group
        ags = list(group.geta())
        for j in ags:
            if not agroups[j] is group:
                group.add(agroups[j])
                agroups[j] = group
    for i in range(b):
        group = bgroups[i]
        bs = list(group.getb())
        for j in bs:
            if not bgroups[j] is group:
                group.add(bgroups[j])
                bgroups[j] = group
        ags = list(group.geta())
        for j in ags:
            if not agroups[j] is group:
                group.add(agroups[j])
                agroups[j] = group

    # Unique all sets
    answer = set(agroups)
    answer.update(bgroups)
    answer = list(answer)

    #print([str(g) for g in answer])
    answer = sorted(answer, key= lambda x: min(x.geta()))

    return answer

output = { 'books': [] }
bom = {'id': 'bom', 'books': []}
output['books'].append(bom)

map_id = 0
map_ids = {}

with open(lang1+".txt") as in1, open(lang2 + ".txt") as in2, open(lang1 + "-" + lang2 + "-align.out") as align:
    chapter_obj = None
    book_obj = None
    i = 0
    for a, b in zip(in1.readlines(), in2.readlines()):
        a, b = a.strip(), b.strip()
        if len(a) == 0 and len(b) == 0:
            continue
        elif a == '----------' and b == '----------':
            continue
        elif a.startswith('/study/scriptures/bofm/'):
            book = a[23:]
            if '/' in book:
                book, chapter = book.split('/')
            else:
                chapter = ''
            if book_obj == None or book_obj['id'] != book:
                book_obj = { 'id': book, 'chapters': []}
                bom['books'].append(book_obj)
            chapter_obj = [] # list of verses
            book_obj['chapters'].append(chapter_obj)
            continue
        verses = []
        chapter_obj.append(verses)
        pairs = align.readline().strip().split()
        parts = sorted(pairs)
        # i += 1
        # if i<470:
        #     continue
        at = tokenize(a)
        bt = tokenize(b)
        graph = build_graph(pairs, len(at), len(bt))
        #print(chapter)
        for m in graph:
            ags = m.geta()
            a1, a2 = min(ags), max(ags)
            bgs = m.getb()
            b1, b2 = min(bgs), max(bgs)

            a1, a2 = at[a1][0], at[a2][1]
            b1, b2 = bt[b1][0], bt[b2][1]

            # TODO: remove punctuation? iterate while not alphabetic

            mapping = (a[a1:a2], b[b1:b2])
            if mapping in map_ids.keys():
                current_id = map_ids[mapping]
            else:
                current_id = map_id
                map_ids[mapping] = current_id
                map_id += 1

            verses.append([a1, a2, b1, b2, current_id])

print(map_id)

with open(lang1 + "-" + lang2 + ".json", 'w') as out:
    out.write(json.dumps(output))