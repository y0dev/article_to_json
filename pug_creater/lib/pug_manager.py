from pathlib import Path 

# Add debug prints

def indent(num=1):
    val = ''
    for _ in range(num):
        val += '\t'
    return val

# first_level_body_idn = pmObj.indent(2)
# second_level_body_idn = pmObj.indent(3)
# third_level_body_idn = pmObj.indent(4)
# fourth_level_body_idn = pmObj.indent(5)
# fifth_level_body_idn = pmObj.indent(6)
# sixth_level_body_idn = pmObj.indent(7)
# seventh_level_body_idn = pmObj.indent(8)
# eighth_level_body_idn = pmObj.indent(9)
# ninth_level_body_idn = pmObj.indent(10)
def indentList() -> list:
    indent_list = []
    for idx in range(10):
        indent_list.append( indent( idx + 2 ) )
    return indent_list

class Pug_Manager:

    def __init__(self,output_path='output/', filename='main') -> None:
        print(f'Generating {filename}')
        self.filename = f'{output_path}/{filename}/index.pug'
        filepath = Path(f'{output_path}/{filename}')
        filepath.mkdir(parents=True, exist_ok=True)  
        
        # Create a pug file with the name given
        lines = ['doctype html\n', 'html(lang=\'en\')\n','\thead\n','\t\tmeta(charset="UTF-8")\n',
                '\t\tmeta(name="viewport" content="width=device-width, initial-scale=1.0")\n', 
                '\tbody\n']
        self.elements = {'head': 2, 'body': 0}
        with open(self.filename, 'w') as f:
            f.writelines(lines)
    
    def __appendNewLineChar(self,lines):
        new_lines = []
        for line in lines:
            new_lines.append(f'{line}\n')
        return new_lines

    def __updateListIndex(self,list, num):
        indention = indent(num)
        new_list = []
        for item in list:
            new_list.append(f'{indention}{item}')
        return new_list
    
    """
        Definition: Finds head or body in pug file
        param:
            after
    """
    def __findLocationInFile(self,location,lines,after=0):
        new_lines = []
        skip_list = []
        with open(self.filename, 'r+') as f:
            filelines = f.readlines()
            for idx, line in enumerate(filelines):
                if location in line:
                    new_lines.append(f"\t{location}\n")
                    
                    # Check number of elements in section
                    if self.elements[location] > 0:
                        for j_idx in range(self.elements[location]):
                            if j_idx == after:
                                # print(f'Breaking at {j_idx}')
                                break
                            start_from = 1
                            # print(filelines[idx + (j_idx + start_from)])
                            new_lines.append(filelines[idx + (j_idx + start_from)])
                            skip_list.append(idx + (j_idx + start_from))
                    # print(f'New Lines Count: {len(lines)}')
                    for nline in lines:
                        # print(f'Element Count: {self.elements[location]} {nline}')
                        new_lines.append(nline)
                        self.elements[location] += 1
                else:
                    # print(f'Skip List {skip_list}')
                    if idx not in skip_list:
                        # print(f'Not in list {line}')
                        new_lines.append(line)
                
        return new_lines
    
# 'meta': {
# 				'author': 'Devontae Reid',
# 				'og:title': 'Devontae Reid',
# 				'twitter:title': 'Devontae Reid',

# 				'og:image': 'https://i.ibb.co/HY4dx9s/headshot.jpg',
# 				'twitter:image': 'https://i.ibb.co/HY4dx9s/headshot.jpg',

# 				'description': 'Backend & Frontend Developer, Engineer, & Theologian',
# 				'og:description': 'Backend & Frontend Developer, Engineer, & Theologian',
# 				'twitter:description': 'Backend & Frontend Developer, Engineer, & Theologian',

# 				'twitter:card': 'summary_large_image',
# 				'twitter:site': '@_yodev_',

# 				'og:url': 'https://www.devontaereid.com',
# 				'og:type': 'website'
# 				// 'theme-color': '#4285f4'
# 				// Will generate: <meta name="theme-color" content="#4285f4">
# 			}

    def addTitle(self,title:str):
        # print('Adding Title')
        lines = [f'title {title}\n',
                 f'meta(name="title" property="og:title" content="{title}")\n',
                 f'meta(name="title" property="twitter:title" content="{title}")\n']
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)
    
    def addDescription(self,description:str):
        # print('Adding Description')
        lines = [f'meta(name="description" property="og:description" content="{description}")\n',
                 f'meta(name="description" property="twitter:description" content="{description}")\n']
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def addImage(self,image:str):
        # print('Adding Image')
        lines = [f'meta(name="image" property="og:image" content="{image}")\n',
                 f'meta(name="image" property="twitter:image" content="{image}")\n']
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)
            
    def addMeta(self,meta_tags:dict):
        # print('Adding Meta')
        lines = []
        for key in meta_tags:
            lines.append(f'meta(property="{key}" content="{meta_tags[key]}")\n')
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def addPrismCode(self,languages:[str]):
        # print('Adding Meta')
        lines = []
        # lines.append(f'link(rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/themes/prism.min.css")\n')
        lines.append(f'script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/prism.min.js")\n')
        lines.append(f'script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/plugins/normalize-whitespace/prism-normalize-whitespace.min.js")\n')
        for language in languages:
            lines.append(f'script(src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/components/prism-{language}.min.js")\n')
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def addIcon(self,logo_filename='logo.png'):
        lines = [f'link(rel="icon" type="image/x-icon" href="{logo_filename}")\n']
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines)
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def addCSS(self,parent:bool=False,css_filename='style.css'):
        # print('Adding Style Sheet')
        lines = []
        if parent:
            lines.append(f'link(rel="stylesheet" href="../{css_filename}")\n')
        else:
            lines.append(f'link(rel="stylesheet" href="/{css_filename}")\n')
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines,after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)
    
    def addJavascriptFile(self,parent:bool=False,js_filename='main.js'):
        # print('Adding Javascript File')
        lines = []
        if parent:
            lines.append(f'script(type="text/javascript" src="../{js_filename}")\n')
        else:
            lines.append(f'script(type="text/javascript" src="/{js_filename}")\n')
        
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('body',lines,after=self.elements['body'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)
    
    def addBibleJavascriptFile(self):
        # print('Adding Javascript File')
        lines = [f'script(type="text/javascript" src="https://static.esvmedia.org/crossref/crossref.min.js")\n']
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('body',lines,after=self.elements['body'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def appendToHeader(self, lines:list):
        lines = self.__updateListIndex(lines,2)
        new_lines = self.__findLocationInFile('head',lines)
        # Rewrite lines to file
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)
    

    def appendToBody(self, lines:list):
        lines = self.__appendNewLineChar(lines)
        new_lines = self.__findLocationInFile('body',lines)
        # Rewrite lines to file
        # print(lines)
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.writelines(new_lines)
