import json

articles_filename = 'json/articles.json'
notes_filename = 'json/notes.json'
try:
    json_file = open(articles_filename)
    articles = json.load(json_file)
    str_articles = json.dumps(articles)
    print(str_articles)
    json_file.close()
except:
    print(f'File [{articles_filename}] doesn\'t exist')
    exit(-1)


try:
    json_file = open(notes_filename)
    notes = json.load(json_file)
    json_file.close()
except:
    print(f'File [{notes_filename}] doesn\'t exist')
    exit(-1)
