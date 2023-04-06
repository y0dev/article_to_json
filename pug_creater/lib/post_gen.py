from .pug_manager import Pug_Manager, indentList
import re


"""
    This is for 
"""

class Post_Generator:
    def __init__(self, title: str = 'Sample', description: str = 'Sample Description', post_type: str = 'article', json_obj: dict = {}) -> None:
        if len(json_obj) == 0:
            post_page_filename = 'main.pug'
        else:
            post_page_filename = json_obj['id']

        self.post_type = post_type
        if self.post_type.lower() == 'article':
            self.pm = Pug_Manager(
                output_path='output/pug/articles', filename=f'{post_page_filename}')
        else:
            self.pm = Pug_Manager(
                output_path='output/pug/notes', filename=f'{post_page_filename}')

        self.lines = []
        self.tags = []
        self.id_list = indentList()
        self.title = title
        self.description = description
        self.embedded = False
        self.code_script_added = False
        self.headshot = 'https://i.ibb.co/HY4dx9s/headshot.jpg'  # 'headshot.png'
        self.logo = '/images/logo.png'  # 'images/logo192.png'
        self.__getPostDetails(json_obj)
        self.__setupInitHead()

        self.__setupBody()

    def __getPostDetails(self, json_obj: dict):
        if len(json_obj) == 0:
            self.post_time = 'Thursday, October 6, 2022'
            self.post_info = {'date': 'Thursday, October 6, 2022'}
        else:
            from datetime import datetime
            self.post_info = json_obj
            self.title = self.post_info['title']
            # Add description
            if self.post_type.lower() == 'article':
                self.description = f'Blog post about {self.post_info["description"]}.'
            else:
                self.description = f'Note about {self.post_info["description"]}.'

            self.tags = self.post_info['tags']
            # Convert from js timestamp
            py_timestamp = int(self.post_info['date'])/1000.0
            # print(py_timestamp)
            self.post_info['date'] = datetime.fromtimestamp(
                py_timestamp).strftime("%A, %B %d, %Y")

    # Helper

    def __setupInitHead(self):
        meta_links = { 'twitter:card': 'summary_large_image', 'twitter:site': '@_yodev_',
                      'og:url': 'https://www.devontaereid.com', 'og:type': 'website'}
        self.pm.addTitle(self.title)
        self.pm.addDescription(self.description)
        self.pm.addIcon(logo_filename='/images/logo.png')
        self.pm.addImage(
            f'https://www.devontaereid.com/{self.post_info["image"]["name"]}')
        self.pm.addMeta(meta_links)
        self.pm.addCSS()

    def __addNavBar(self):
        self.lines.append(
            f'{self.id_list[0]}div#nav-bar.navbar.header-content--mini')
        self.lines.append(f'{self.id_list[1]}nav')
        self.lines.append(f'{self.id_list[2]}div.main-menu')
        self.lines.append(f'{self.id_list[3]}a.menu-branding(href="/")')
        self.lines.append(
            f'{self.id_list[4]}img.menu-branding(src="{self.logo}" alt="branding-logo")')
        self.lines.append(f'{self.id_list[4]}h3 Devontae Reid')

        # Menu List
        self.lines.append(f'{self.id_list[3]}ul.menu-list')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/projects") Projects')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/articles") Articles')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/gospel") Gospel')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}button.display-switch ☀️')


    def __addFooter(self):
        self.lines.append(
            f'{self.id_list[0]}.footer')
        self.lines.append(f'{self.id_list[1]}.footer-container')
        self.lines.append(f'{self.id_list[2]}p Sola Scriptura ( Scripture Alone ), Solus Christus ( Christ Alone ), Sola fide ( Faith Alone ), Sola Gratia ( Grace Alone ), and Soli Deo Gloria ( Glory to God Alone )')
        self.lines.append(f'{self.id_list[2]}.socials')
        self.lines.append(f'{self.id_list[3]}ul')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://www.linkedin.com/in/devontaereid/")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/linkedin.png")')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://twitter.com/_yodev_")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/twitter.png")')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://github.com/y0dev")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/github.png")')

        # Copyright
        self.lines.append(f'{self.id_list[2]}p.footer-small Icons provided by ')
        self.lines.append(f'{self.id_list[3]}a(href="https://www.flaticon.com/authors/freepik" title="Freepik") Freepik')

    def __addPostTags(self):

        self.lines.append(f'{self.id_list[3]}div.post-header-tags')
        for tag in self.tags:
            self.lines.append(f'{self.id_list[5]}span.post-header-tag {tag}')
    
    def __addReadTime( self, indent_level:int ):
        time = self.post_info['time']
        timeStr = ''
        print(f'Time {time}')
        if int(time['hours']) != 0:
            if int(time['hours']) == 1:
                timeStr = '1 hour'
            else:
                timeStr = f'{int(time["hours"])} hours'
        elif int(time['mins']) != 0:
            if int(time['mins']) == 1:
                if int(time['secs']) >= 30:
                    timeStr = f'{int(time["mins"]) + 1} mins'
                else:
                    timeStr = '1 min'
            else:
                if int(time['secs']) >= 30:
                    timeStr = f'{int(time["mins"]) + 1} mins'
                else:
                    timeStr = f'{int(time["mins"])} mins'
        elif time['secs'] != '0' and time['secs'] != '00':
            timeStr = '< 1 min'

        self.lines.append(
            f'{self.id_list[indent_level]}p#post-read-time {timeStr}')
        

    def __addPostContent(self):
        self.lines.append(f'{self.id_list[1]}div.post-content')
        for content in self.post_info['content']:
            new_string = ''.join(c for c in content["title"]["text"] if c.isalnum() or c == ' ')
            id_tag = f'{new_string.replace(" ","-").lower()}'
            self.lines.append(f'{self.id_list[2]}div.post-section-container#{id_tag}')
            self.lines.append(
                f'{self.id_list[3]}h2.section-title {content["title"]["text"]}')
            for paragraph in content['paragraphs']:
                self.__addContentParagraph(content, paragraph)

    # TODO: Need to finish
    def __addList(self, indent_level: int, items: list, list_type='ordered'):
        if list_type == 'unordered':
            self.lines.append(f'{self.id_list[indent_level]}ul')
        else:
            self.lines.append(f'{self.id_list[indent_level]}ol')

        for item in items:
            pass

    def __handlePath(self, line: str, indent_level=4) -> str:
        l_start = len(':path-start ')
        l_end = len(' :path-end')

        idx_start = line.index(':path-start')
        idx_end = line.index(':path-end')
        file_path = line[idx_start + l_start: idx_end]
        # print(file_path)
        self.lines.append(
            f'{self.id_list[indent_level + 3]}span.code-file-path {file_path}')

        code_line = line[idx_end + l_end:]
        if len(code_line) == 0:
            self.lines.append(
                f'{self.id_list[indent_level + 3]}br')
        else:
            self.lines.append(
                f'{self.id_list[indent_level + 4]}.')
            self.lines.append(
                f'{self.id_list[indent_level + 5]}{code_line[idx_end + l_end:]}')
            self.lines.append(
                f'{self.id_list[indent_level + 3]}br')
        return code_line

    def __handleString(self, line: str, indent_level=4) -> str:
        l_start = len(':string-open ')
        l_end = len(':string-close ')
        code_line = line
        if code_line[:l_start] == ':string-open ':
            idx_start = line.index(':string-open')
            idx_end = line.index(':string-close')
            string = line[idx_start + l_start:idx_end-1] + "\""
            # print(f'handleString Intro- {string}')
            self.lines.append(
                f'{self.id_list[indent_level + 3]}span.code-string {string}')
            code_line = line[idx_end + l_end:]
            # print(f'handleString-{code_line}')
        return code_line

    def __handlePunc(self, line: str, indent_level=4) -> str:
        l_start = len(':string-open ')
        l_end = len(':string-close ')
        code_line = line
        if code_line[:l_start] == ':string-open ':
            idx_start = line.index(':string-open')
            idx_end = line.index(':string-close')
            string = line[idx_start + l_start:idx_end] + "\""
            self.lines.append(
                f'{self.id_list[indent_level + 4]}span.code-punctuation {string}')
            code_line = line[idx_end + l_end:]
            # print(code_line)
        return code_line

    def __handleBrackets(self, line: str, indent_level=4) -> str:
        l_start = len(':bracket-open ')
        l_end = len(':bracket-close ')
        code_line = line
        if code_line[:l_start] == ':bracket-open ':
            idx_start = line.index(':bracket-open')
            open_bracket = line[idx_start + l_start]
            # print(open_bracket)
            self.lines.append(
                f'{self.id_list[indent_level + 3]}span.code-bracket {open_bracket}')
            code_line = line[idx_start + l_start + 2:]
        elif code_line[:l_end] == ':bracket-close ':
            idx_end = line.index(':bracket-close')
            closing_bracket = line[idx_end + l_end]
            # print(closing_bracket)
            self.lines.append(
                f'{self.id_list[indent_level + 3]}span.code-bracket {closing_bracket}')
            code_line = line[idx_end + l_end + 2:]
            if len(code_line) == 0:
                self.lines.append(f'{self.id_list[indent_level + 3]}br')
        # print(f'Bracket: {code_line}')
        return code_line

    def __addCodeBlock(self, code_content: dict, indent_level=4):

        if not self.code_script_added:
            self.code_script_added = True

        self.lines.append(
            f'{self.id_list[indent_level]}div.code-snippet-container')
        self.lines.append(
            f'{self.id_list[indent_level + 1]}div.code-snippet-header')
        self.lines.append(
            f'{self.id_list[indent_level + 2]}h5.code-snippet-title {code_content["title"]}')
        self.lines.append(f'{self.id_list[indent_level + 2]}button.copy-bttn')
        self.lines.append(
            f'{self.id_list[indent_level + 3]}img.copy-icon(src="/images/copy-icon.png")')

        self.lines.append(
            f'{self.id_list[indent_level + 1]}div.code-snippet-body')
        self.lines.append(
            f'{self.id_list[indent_level + 2]}pre.language-{code_content["language"]}')
        # Remove . from end
        self.lines.append(
            f'{self.id_list[indent_level + 3]}code.language-{code_content["language"]}')

        for line in code_content["content"]:
            if ':comment ' in line:
                l_start = len(':comment ')
                idx_start = line.index(':comment')
                comment = line[idx_start + l_start:]
                # print(comment)
                self.lines.append(
                    f'{self.id_list[indent_level + 4]}span.code-comment {comment}')
                self.lines.append(f'{self.id_list[indent_level + 4]}br')
                continue

            code_line = line
            # print(f'Original-Line{line}')
            while ':code-specific ' in code_line or ':path-start ' in code_line or ':bracket-open ' in code_line or ':bracket-close ' in code_line or ':string-open ' in code_line or ':indent-text' in code_line:

                # Check for indentation of line
                indent = ''
                if code_line[:len(':indent-text')] == ':indent-text':
                    i_start = len(':indent-text')
                    i_end = len(':indent-text[X]')
                    # print(f'indent size:{code_line[i_start:i_end]}')
                    indent = f'indent-{code_line[i_start+1:i_end-1]}'
                    code_line = code_line[i_end+1:]
                # print(indent,code_line)

                if code_line[:len(':code-specific ')] == ':code-specific ':
                    l_start = len(':code-specific ')
                    l_end = len(' :code-specific-end')

                    idx_start = code_line.index(':code-specific')
                    idx_end = code_line.index(':code-specific-end')
                    code_specific = code_line[idx_start + l_start: idx_end]
                    # print(code_specific)

                    # print(f'C-Line {code_line}')
                    if indent == '':
                        self.lines.append(
                            f'{self.id_list[indent_level + 4]}span.code-specific {code_specific}')
                    else:
                        self.lines.append(
                            f'{self.id_list[indent_level + 4]}span.code-specific(class="{indent}") {code_specific}')
                        
                    code_line = code_line[idx_end + l_end:]
                else:
                    # print(f'E-Line {code_line}')
                    # Check for any brackets or string before moving on
                    if code_line[:len(':path-start ')] == ':path-start ':
                        code_line = self.__handlePath(line=code_line,
                                                      indent_level=indent_level+1)
                        # print(f'P-Line {code_line}')
                    elif code_line[:len(':bracket-open ')] == ':bracket-open ' or code_line[:len(':bracket-close ')] == ':bracket-close ':
                        # print(f'B-Line {code_line[:len(": bracket-open ")]}')
                        code_line = self.__handleBrackets(
                            line=code_line, indent_level=indent_level+1)
                    # or code_line[:len(':string-close')] == ':string-close':
                    elif code_line[:len(':string-open ')] == ':string-open ':
                        # print(f'S-Line {code_line[:len(":string-open ")]}')
                        code_line = self.__handleString(
                            line=code_line, indent_level=indent_level+1)
                    else:
                        # Restart beginning of text, by finding the min_index keyword
                        # Maybe is some text
                        min_idx = 10000
                        name = ''
                        if ':code-specific' in code_line:
                            name = ':code-specific'
                            min_idx = min(
                                min_idx, code_line.index(':code-specific'))
                        if ':path-start' in code_line:
                            name = ':path-start'
                            min_idx = min(
                                min_idx, code_line.index(':path-start'))
                        if ':bracket-open' in code_line:
                            name = ':bracket-open'
                            min_idx = min(
                                min_idx, code_line.index(':bracket-open'))
                        if ':bracket-close' in code_line:
                            name = ':bracket-close'
                            min_idx = min(
                                min_idx, code_line.index(':bracket-close'))
                        if ':string-open' in code_line:
                            name = ':string-open'
                            min_idx = min(
                                min_idx, code_line.index(':string-open'))
                        length = len(name)

                        if length > 0:
                            # print(
                            #     f'El2-Line {code_line[:min_idx]}')
                            # print(
                            #     f'El2-Line {code_line[min_idx:]}')

                            # Must be line without keyword
                            if min_idx > 1 and self.lines[-1] != 'br':
                                self.lines.append(
                                    f'{self.id_list[indent_level + 4]}.')
                                
                            
                            self.lines.append(
                                f'{self.id_list[indent_level + 5]}{code_line[:min_idx]}')

                            code_line = code_line[min_idx:]

                            # print(min_idx)
                            # print(f'End-Line{code_line}')

            # Clean up any left over from line
            if len(code_line) != 0:
                # print(f'Exit Line {code_line}')
                
                if indent == '':
                    self.lines.append(f'{self.id_list[indent_level + 4]}.')
                    self.lines.append(
                        f'{self.id_list[indent_level + 5]}{code_line}')
                    self.lines.append(
                        f'{self.id_list[indent_level + 4]}br')
                else:
                    self.lines.append(
                        f'{self.id_list[indent_level + 4]}span.{indent} {code_line}')
                    self.lines.append(
                        f'{self.id_list[indent_level + 4]}br')


    def __addContentParagraph(self, content: dict, paragraph: str):
        # print(paragraph)
        temp_paragraph = paragraph
        # Check for image in paragraph
        if ':imagePlace' in temp_paragraph:
            items, positions = self.__parse_string(temp_paragraph,':imagePlace')
            # print(positions[0])
            for item in positions:
                img_id = self.__get_id_from_string(item['item'])
                temp_paragraph = self.__remove_key(temp_paragraph,item['item_with_key'])

            
            # print(temp_paragraph)
            # print(f'Image {img_id}')
            # print(l,idx,img_id)
            for image in content['images']:
                if image['id'] == img_id:
                    # print(image)
                    self.lines.append(
                        f'{self.id_list[3]}div.post-image-container')
                    self.lines.append(
                        f'{self.id_list[4]}a.post-image-container(href="{image["link"]}")')
                    self.lines.append(
                        f'{self.id_list[5]}img.post-image(src="{image["link"]}" alt="{image["alt"]}")')
                    self.lines.append(
                        f'{self.id_list[4]}figcaption.post-image-caption {image["caption"]}')
        # Check for any links in text
        if ':linkPlace' in temp_paragraph:
            items, positions = self.__parse_string(temp_paragraph,':linkPlace')
            start_idx = 0
            # print(items[12])
            for idx, item in enumerate(positions):
                link_id = self.__get_id_from_string(item['item'])
                # add previous text from paragraph into list if they are before link
                if idx == 0:
                    self.lines.append(
                        f'{self.id_list[3]}p.post-details')
                    self.lines.append(
                        f'{self.id_list[4]}| {items[idx]}')
                
                # search for id in list
                for link in content['links']:
                    if link['id'] == link_id:
                        text = self.__get_non_id_from_string(item['item'])
                        self.lines.append(
                            f'{self.id_list[4]}a.post-link(href="{link["link"]}") {link["text"]}{text}')
                
                temp_paragraph = self.__remove_key(temp_paragraph,item['item_with_key'])
                
        # Check for lists in text
        if ':listPlace' in temp_paragraph:
            items, positions = self.__parse_string(temp_paragraph,':listPlace')
            for item in positions:
                matches = re.search(r"listPlace\(\d{3}\)", item['item_with_key'])
                if matches:
                    list_id = self.__get_id_from_string(item['item'])

                    # Write text to file up until position of key
                    self.lines.append(
                        f'{self.id_list[3]}p.post-details {temp_paragraph[:item["position"] - item["key_length"]]}')
                    
                    # Search for id in list
                    for list in content['lists']:
                        if list['id'] == list_id:
                            if list['list_type'] == 'unordered':
                                self.lines.append(f'{self.id_list[3]}ul')
                            else:
                                self.lines.append(f'{self.id_list[3]}ol')
                            
                            # Check for any sublist in list
                            for li_item in list['items']:
                                if ':listPlace' in li_item:
                                    subitems, subpositions = self.__parse_string(li_item,':listPlace')
                                    for subpos in subpositions:
                                        submatch = re.search(r"listPlace\(\d{3}\)", subpos['item_with_key'])
                                        if submatch:
                                            sublist_id = self.__get_id_from_string(subpos['item'])
                                            
                                            # Write text to file up until position of key
                                            self.lines.append(
                                                f'{self.id_list[4]}li.post-list-item {li_item[:subpos["position"]  - subpos["key_length"]]}')
                                            
                                            for sub_list in content['lists']:
                                                if sub_list['id'] == sublist_id:
                                                    if sub_list['list_type'] == 'unordered':
                                                        self.lines.append(
                                                            f'{self.id_list[5]}ul.sublist')
                                                    else:
                                                        self.lines.append(
                                                            f'{self.id_list[5]}ol.sublist')
                                                    
                                                    for slitem in sub_list['items']:
                                                        self.lines.append(
                                                            f'{self.id_list[6]}li.post-sublist-item {slitem}')
                                            
                                            temp_paragraph = self.__remove_key(li_item,subpos['item_with_key'])
                                else:
                                    self.lines.append(
                                        f'{self.id_list[4]}li.post-list-item {li_item}')

                    temp_paragraph = self.__remove_key(temp_paragraph,item['item_with_key'])

        if ':codePlace' in temp_paragraph:
            l_start = len(':codePlace(XYZ)')
            idx_start = temp_paragraph.index(':codePlace')
            code_location = temp_paragraph[idx_start:idx_start + l_start]
            code_id = code_location[-4:-1]
            self.lines.append(
                f'{self.id_list[3]}p.post-details {temp_paragraph[:idx_start]}')
            for code in content['code']:
                if code['id'] == code_id:
                    self.__addCodeBlock(code)

        if ':user-defined-code' in temp_paragraph:
            l_start = len(':user-defined-code')
            l_end = len(':end')
            idx_start = temp_paragraph.index(':user-defined-code')
            idx_end = temp_paragraph.index(':end')
            code_ = temp_paragraph[idx_start + l_start:idx_end]
            self.lines.append(f'{self.id_list[3]}p.post-details')
            self.lines.append(f'{self.id_list[4]}| {temp_paragraph[:idx_start]}')
            self.lines.append(
                f'{self.id_list[4]}span.user-define-code{code_}')  # this can
            self.lines.append(
                f'{self.id_list[4]}| {temp_paragraph[idx_end + l_end:]}')
        
        # Check for text 
        if ':special-text(key=' in temp_paragraph:
            # print(temp_paragraph)
            p = self.__parse_string_to_get_between_par(temp_paragraph,':special-text', left_delimiter='(key=')
            start_idx = 0
            for idx, item in enumerate(p):
                end_idx = item['start_position']
                temp_para = self.__remove_key(temp_paragraph,item['item_with_key'])
                if start_idx == 0:
                    self.lines.append(f'{self.id_list[3]}p.post-details {temp_paragraph[start_idx:end_idx]}')
                else:
                    if temp_paragraph[start_idx:end_idx].strip() != '':
                        self.lines.append(f'{self.id_list[4]}| {temp_paragraph[start_idx:end_idx]}')
                
                self.lines.append(f'{self.id_list[4]}span.{item["key"]}-text {item["text"]}')

                start_idx = item['end_position']

            
            # Add rest of paragraph
            if temp_paragraph[start_idx:].strip() != '':
                if temp_paragraph[start_idx+1] == '.':
                    plus = 1
                else:
                    plus = 0
                self.lines.append(f'{self.id_list[4]}| {temp_paragraph[start_idx+plus:]}')
            
            # Since this is the final thing to search clear paragraph
            temp_paragraph = ''

        if temp_paragraph != '':
            self.lines.append(f'{self.id_list[3]}p.post-details {temp_paragraph}')
        
        
    def __addJavascriptFiles(self):
        self.pm.addJavascriptFile(js_filename='scripts/main.js')
        if self.code_script_added:
            self.pm.addJavascriptFile(js_filename='scripts/code_script.js')
        self.pm.addBibleJavascriptFile()

    def __setupBody(self):
        self.__addNavBar()
        self.lines.append(f'{self.id_list[0]}div.post-body')
        self.lines.append(f'{self.id_list[1]}article.button#post-container')
        self.lines.append(f'{self.id_list[1]}div.post-header-container')
        self.lines.append(f'{self.id_list[2]}div.post-header-details')
        self.lines.append(f'{self.id_list[3]}h1#post-header-title {self.title}')
        self.lines.append(f'{self.id_list[3]}div.post-header-meta')
        self.lines.append(
            f'{self.id_list[4]}img.post-header-icon(src="{self.headshot}" alt="headshot")')
        self.lines.append(
            f'{self.id_list[4]}p.post-header-time {self.post_info["date"]}')
        self.lines.append(f'{self.id_list[4]}span.post-header-divider |')

        self.__addReadTime(indent_level=4)
        
        self.lines.append(
            f'{self.id_list[4]}button.post-header-shareButton#shareButton')
        self.lines.append(
            f'{self.id_list[5]}span.post-header-shareButton-icon')
        self.lines.append(
            f'{self.id_list[6]}img(src="/images/share_icon.png" alt="share_icon")')
        self.lines.append(f'{self.id_list[6]}.')
        self.lines.append(f'{self.id_list[7]}Share')

        self.__addPostTags()
        self.lines.append(
            f'{self.id_list[2]}img.post-header-image(src="/{self.post_info["image"]["name"]}" alt="{self.post_info["image"]["alt"]}")')

        self.__addPostContent()
        self.__addFooter()

        self.__addJavascriptFiles()

    def __parse_string(self, string:str, key:str):
        # Split string by key
        items = string.split(key)
        string.split()
        # remove any leading or trailing white spaces from each item
        items = [item.strip() for item in items if item.strip()]

        # Initialize a dictionary to store each items's position in original string
        positions = []

        # Iterate over each parsed item and find its position in the original string
        start = 0
        for item in items:
            pos = string.find(item, start)
            itemInfo = {
                'item': item,
                'position': pos,
                'item_with_key': f'{key}{item}',
                'key_length': len(key)
            }
            itemInfo['end_position'] = itemInfo['position'] + len(itemInfo['item_with_key'])
            positions.append(itemInfo)
            start = pos + len(item)

        # Return a tuple containing the list of parsed items and the dictionary of positions
        return items, positions
    
    def __parse_string_to_get_between_par(self,input_string:str, separator:str, left_delimiter='(', right_delimiter=')'):
        # Split the input string into a list of individual items
        items = input_string.split(separator)
        end_key = None
        if separator == ':special-text':
            end_key = 'special-text-end'

        # Initialize a list to store the parsed information and its position in the input string
        parsed_items = []

        # Initialize a variable to keep track of the current position in the input string
        current_position = 0

        # Iterate over each item in the list
        for item in items:
            # Find the left and right delimiter strings in the item
            left_index = item.find(left_delimiter)
            right_index = item.find(right_delimiter)

            # If both delimiters are found and the left delimiter comes before the right delimiter
            if left_index != -1 and right_index != -1 and left_index < right_index:
                # Extract the information between the delimiters and add it to the parsed items list
                parsed_item = item[left_index + 1:right_index]
                new_item = {
                    'item': parsed_item,
                    'start_position': current_position - len(separator),
                    'position': current_position + left_index + 1,
                    'item_with_key': f'{separator}({parsed_item}){end_key}'
                }
                if end_key != None:
                    new_item['key'] = self.__extract_after_key_before_end_key(parsed_item,'=', ',')
                    new_item['text'] = self.__extract_after_key_before_end_key(parsed_item,',', '')
                    new_item['end_position'] = new_item['start_position'] + len(new_item['item_with_key'])

                parsed_items.append(new_item)

            # Increment the current position in the input string by the length of the current item and the separator
            current_position += len(item) + len(separator)

        # Return the list of parsed items
        return parsed_items
    
    def __get_id_from_string(self, string:str):
        # Replace all instances of "(" and ")" with empty strings
        return re.sub(r'\D', '', string)

    def __get_non_id_from_string(self, string:str):
        # Replace all instances of "(" and ")" with empty strings
        return re.sub(r'\d+', '', string).replace('()','')
    
    def __remove_key(self, string:str, key:str):
        # Replace all instances of "(" and ")" with empty strings
        return string.replace(key, "")
        
    def __remove_except_key(self, string:str, key:str):
         # Split the input string into a list of individual substrings
        substrings = string.split(key)

        # Initialize an empty string to store the output
        output_string = ''

        # Iterate over each substring in the list
        for i, substring in enumerate(substrings):
            # If the substring contains "key=", add it to the output string
            if key in substring:
                output_string += substring

            # If the substring does not contain "key=" and this is not the last substring in the list, add "key=" to the output string
            elif i < len(substrings) - 1:
                output_string += key

            # Return the resulting output string
        return output_string   
    
    def __extract_after_key_before_end_key(self, string:str, first_key:str, ending_key:str):
        # Find the index of the comma and closing parenthesis
        comma_index = string.find(first_key)
        if ending_key == '':
            paren_index = len(string) 
        else:
            paren_index = string.find(ending_key)

        # Extract the substring between the comma and closing parenthesis
        output_string = string[comma_index+1:paren_index]

        # Return the resulting output string
        return output_string

    def __add_string_at_index(self, string:str, index:int, string_to_add:str):
        # Use string slicing to split the input string into two parts
        first_part = string[:index]
        second_part = string[index:]

        # Concatenate the first part, the string to add, and the second part
        output_string = first_part + string_to_add + second_part

        # Return the resulting output string
        return output_string
    
    def __find_positions_in_string(self, string:str):

        # pattern to match special-text
        pattern = re.compile(":special-text\(key=(italic|bold),'(.+?)'\)special-text-end")

        # find all matches
        matches = pattern.findall(string)

        # replace the matches with the desired text
        new_string = re.sub(pattern, lambda match: match.group(2), string)

        # find the positions of the matches and the replaced text
        positions = []
        for match in matches:
            start = string.find(":special-text(key=%s,'%s')special-text-end" % (match[0], match[1]))
            end = start + len(match[1])
            positions.append((start, end))

        return positions, new_string
     
    def generatePugFile(self):
        self.pm.appendToBody(self.lines)
