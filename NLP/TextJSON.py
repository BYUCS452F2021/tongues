import json

lang = "eng"

output = { 'books': [] }
bom = {'id': 'bom', 'name': 'bom', 'books': []}
output['books'].append(bom)

with open(lang+".txt") as in1:
    chapter_obj = None
    book_obj = None
    i = 0
    for a in in1.readlines():
        a = a.strip()
        if len(a) == 0:
            continue
        elif a == '----------':
            continue
        elif a.startswith('/study/scriptures/bofm/'):
            book = a[23:]
            if '/' in book:
                book, chapter = book.split('/')
            else:
                chapter = ''
            if book_obj == None or book_obj['id'] != book:
                book_obj = { 'id': book, 'name': book, 'chapters': []}
                bom['books'].append(book_obj)
            chapter_obj = [] # list of verses
            book_obj['chapters'].append(chapter_obj)
            continue
        chapter_obj.append(a)

with open(lang + ".json", 'wb') as out:
    out.write(json.dumps(output, ensure_ascii=False).encode('utf8'))