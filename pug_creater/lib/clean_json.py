
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

    for ob in json_obj:
        lst.append(ob)
    
    lst.append(json_object)
    # Serializing json
    json_dump = json.dumps(lst, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_dump)