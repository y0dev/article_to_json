
import os
import json

def open_json_file(filename:str):
    # Open json file
    try:
        json_file = open(filename,encoding="utf8")
        json_obj = json.load(json_file)
        json_file.close()
    except:
        print(f'File [{filename}] doesn\'t exist')
        return None
    
    return json_obj

def clean_json_list(filename:str, isList=True, checkForArticleID=False, checkForNoteID=False,  keys:list=[]):
    lst = []
    split_fn = os.path.splitext(filename)
    
    json_obj = open_json_file(filename)
    if (json_obj == None):
        print("Object is empty")
        exit(-1)

    # Clean
    if len(keys) != 0:
        # Make sure an array has been passed
        if isList:
            # Search json file for keys
            for ob in json_obj:
                obj = {}
                # Check json for note or article identifier
                if checkForArticleID:
                    if not 'file-id' in ob:
                        obj['file-id'] = 'article'
            
                if checkForNoteID:
                    if not 'file-id' in ob:
                        obj['file-id'] = 'note'
                        
                for key in keys:
                    if key in ob:
                        obj[key] = ob[key]
                lst.append(obj)
    

    # Serializing json
    json_object = json.dumps(lst, indent=4)
    # print(json_object)
    # Writing to _clean.json
    with open(f'{split_fn[0]}_clean.json', "w") as outfile:
        outfile.write(json_object)

    # print(lst)

def add_to_json_list(filename:str, json_object: dict):
    lst = []
    split_fn = os.path.splitext(filename)

    json_obj = open_json_file(filename)
    json_dump = json.dumps(json_obj, indent=4)
    with open(f'{split_fn[0]}_old.json', "w") as outfile:
        outfile.write(json_dump)

    if (json_obj == None):
        print("Object is empty")
        exit(-1)

    found = False
    for ob in json_obj:
        if (ob['title'] == json_object['title']) and (ob['id'] == json_object['id']):
            found = True
        lst.append(ob)
    
    if not found:
        print('Adding new JSON to list')
        lst.append(json_object)
    else:
        print('No update to JSON list')

    # Serializing json
    json_dump = json.dumps(lst, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_dump)

def add_time_to_json_list(filename:str):
    lst = []
    split_fn = os.path.splitext(filename)

    json_obj = open_json_file(filename)
    json_dump = json.dumps(json_obj, indent=4)
    with open(f'{split_fn[0]}_old.json', "w") as outfile:
        outfile.write(json_dump)

    if (json_obj == None):
        print("Object is empty")
        exit(-1)
    
    for ob in json_obj:
        if ('time' in ob):
            continue
        else:
            wordCount = 0
            print(ob['title'])
            for content in ob['content']:
                for paragraph in content['paragraphs']:
                    wordCount += len(paragraph.split(' '))

                if 'lists' in content:
                    for list in content['lists']:
                        for item in list['items']:
                            wordCount += len(item.split(' '))
            
            secs = __words_secs(wordCount)
            #print('seconds',secs)
            timeToRead = __convert_to_preferred_format(secs)
            print(timeToRead)
            
            time_dict = {
                'secs': "%02d" % timeToRead[2],
                'mins': "%02d" % timeToRead[1],
                'hours': "%02d" % timeToRead[0]
            }
            new_obj = {
                'title': ob['title'],
                'description': ob['description'],
                'date': ob['date'],
                'id': ob['id'],
                'time': time_dict,
                'tags': ob['tags'],
                'image': ob['image'],
                'content': ob['content']
            }
        lst.append(new_obj)
    
    # Serializing json
    json_dump = json.dumps(lst, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_dump)

def __convert_to_preferred_format(sec:int):
    # print('seconds',sec)
    sec = sec % (24 * 3600)
    hour = sec // 3600   
    sec %= 3600
    min = sec // 60
    sec %= 60
    # print("seconds value in hours:",hour)
    # print("seconds value in minutes:",min)
    return (hour, min, sec)
    # return "%02d:%02d:%02d" % (hour, min, sec)

def __words_secs(wordCount:int):
    WORDS_PER_MINUTE = 250
    MINUTE = 60
    return (wordCount / WORDS_PER_MINUTE) * MINUTE
