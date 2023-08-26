import sys
from lib.post_gen import Post_Generator
from lib.clean_json import clean_json_list, add_to_json_list, open_json_file, add_time_to_json_list
import os
import json
import glob
import argparse


PRINT_JSON_FOLDER = False

SINGLE = True
ARTICLES = False
APPEND_NEW_ARTICLE = False
CLEAN_ARTICLES =  APPEND_NEW_ARTICLE

NOTES = False
APPEND_NEW_NOTE = False
CLEAN_NOTES = APPEND_NEW_NOTE

def print_json_dir():
    for filename in os.listdir('json'):
        print(filename)

articles_filename = 'json/articles.json'
notes_filename = 'json/notes.json'
keys = ['date','id','image','tags','title']

# add_time_to_json_list(notes_filename)
def append_new_article():
    list_of_files = glob.glob('F:/Documents/blog_articles/json_outputs/*.json') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    new_obj = open_json_file(latest_file)
    add_to_json_list(articles_filename,new_obj)
    # print(latest_file)

def process_articles(clean):
    articles = open_json_file(articles_filename)
    if (articles):
        if clean:
            clean_json_list(articles_filename, checkForArticleID=True, keys=keys)

        for article in articles:
            pg = Post_Generator(json_obj=article)
            pg.generatePugFile()
# print(json_obj[0])

def process_notes(clean):
    notes = open_json_file(notes_filename)
    if (notes):
        if clean:
            clean_json_list(notes_filename, checkForNoteID=True, keys=keys)


        for note in notes:
            pg = Post_Generator(post_type='note',json_obj=note)
            pg.generatePugFile()




def process_single_json(operating_system):
    file_path = ''
    if operating_system == 'pc':
        file_path = 'F:/Documents/blog_articles/json_outputs/*.json'
    elif operating_system == 'mac':
        file_path = 'json/docker.json'

    list_of_files = glob.glob(file_path) # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    json_obj = open_json_file(latest_file)
    if (json_obj):
        print(latest_file)
        pg = Post_Generator(json_obj=json_obj)
        pg.generatePugFile()
        print(pg.pm.filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python script to create an HTML file from JSON file")
    parser.add_argument("--os", choices=["mac", "pc"], required=True, help="Choose an Operating System")
    parser.add_argument("--action", choices=["single", "articles", "notes", "print" ], help="Choose an action to perform")
    parser.add_argument("--clean", action="store_true", help="Use clean option for specific actions")
    parser.add_argument("--append", action="store_true", help="Use append option for specific actions")


    args = parser.parse_args()

    if args.action == "single":
        process_single_json(args.os)
    elif args.action == "articles":
        if args.append:
            append_new_article()
        else:
            process_articles(args.clean)
    elif args.action == "notes":
        process_notes(args.clean)
    elif args.action == "print":
        print_json_dir()
    else:
        print("Invalid action")
        sys.exit(1)  # Exit with an error status code