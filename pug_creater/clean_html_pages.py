from bs4 import BeautifulSoup
import os
import shutil

articles_folder = 'output/html/latest/articles'
notes_folder = 'output/html/latest/notes'

def iterdirectories(directory):
    # iterate over files in
    # that directory
    files = []
    for filename in os.listdir(directory):
        dir = os.path.join(directory, filename)
        if os.path.isdir(dir):
            # print(dir)
            for filename0 in os.listdir(dir):
                f = os.path.join(dir, filename0)
                # print(f)
                split_tup = os.path.splitext(f)
                file_extension = split_tup[1]
                # print(file_extension)
                # checking if it is a file
                
                
                if os.path.isfile(f) and '.html' == file_extension and not 'copy' in split_tup[0]:
                    dst = f'{f}_copy'
                    shutil.copyfile(f, dst)
                    files.append(dst)
    return files

def clean_html(files:list):
    for html in files:
        split_tup = os.path.splitext(html)
        # print(split_tup[1][:-5])
        # print(html)
        bad_html = open(html,encoding="utf8")
        try:
            tree = BeautifulSoup(bad_html, 'html.parser')
            good_html = tree.prettify()
            # print(good_html)
            with open(f'{split_tup[0]}{split_tup[1][:-5]}', "w",encoding="utf8") as file1:
                # Writing data to a file
                file1.write(good_html)
            bad_html.close()
            os.remove(html)
        except:
            print(f'File [{html}] doesn\'t exist')
            exit(-1)

article_files = iterdirectories(articles_folder)
clean_html(article_files)
notes_files = iterdirectories(notes_folder)
clean_html(notes_files)
# print(files)


