from lib.post_gen import Post_Generator
from lib.clean_json import clean_json_list, add_to_json_list, open_json_file, add_time_to_json_list
import os
import json
import glob


PRINT_JSON_FOLDER = False

SINGLE = True
ARTICLES = False
APPEND_NEW_ARTICLE = False
CLEAN_ARTICLES =  APPEND_NEW_ARTICLE

NOTES = False
APPEND_NEW_NOTE = False
CLEAN_NOTES = APPEND_NEW_NOTE

if PRINT_JSON_FOLDER:
    for filename in os.listdir('json'):
        print(filename)

articles_filename = 'json/articles.json'
notes_filename = 'json/notes.json'
keys = ['date','id','image','tags','title']

# add_time_to_json_list(notes_filename)
if APPEND_NEW_ARTICLE:
    list_of_files = glob.glob('F:/Documents/blog_articles/json_outputs/*.json') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    new_obj = open_json_file(latest_file)
    add_to_json_list(articles_filename,new_obj)
    # print(latest_file)

if ARTICLES:
    articles = open_json_file(articles_filename)
    if (articles):
        if CLEAN_ARTICLES:
            clean_json_list(articles_filename, checkForArticleID=True, keys=keys)

        for article in articles:
            pg = Post_Generator(json_obj=article)
            pg.generatePugFile()
# print(json_obj[0])
if NOTES:
    notes = open_json_file(notes_filename)
    if (notes):
        if CLEAN_NOTES:
            clean_json_list(notes_filename, checkForNoteID=True, keys=keys)


        for note in notes:
            pg = Post_Generator(post_type='note',json_obj=note)
            pg.generatePugFile()


if SINGLE:
    
    list_of_files = glob.glob('F:/Documents/blog_articles/json_outputs/*.json') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    json_obj = open_json_file(latest_file)
    if (json_obj):
        pg = Post_Generator(json_obj=json_obj)
        pg.generatePugFile()