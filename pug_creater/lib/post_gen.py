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
        self.languages = []
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
                f'{self.id_list[3]}{content["title"]["tag"]}.section-title {content["title"]["text"]}')
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


    def __addCodeBlock(self, code_content: dict, indent_level=4):

        # print(code_content)
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
            f'{self.id_list[indent_level + 2]}pre')
        self.lines.append(
            f'{self.id_list[indent_level + 3]}code.code-body.language-{code_content["language"]}')
        for content in code_content['content']:
            # print(content)
            self.lines.append(
                f'{self.id_list[indent_level + 4]}| {content}')
        

        


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
            
            # Handle case where just a string with imagePlace
            if len(temp_paragraph.split()) != 0:
                self.lines.append(f'{self.id_list[3]}p.post-details {temp_paragraph}')

            # print(temp_paragraph)
            # print(f'Image {img_id}')
            # print(l,idx,img_id)
            # Add content image
            for image in content['images']:
                if image['id'] == img_id:
                    # print(image)
                    self.lines.append(
                        f'{self.id_list[3]}div.post-image-container')
                    self.lines.append(
                        f'{self.id_list[4]}a.post-image-container(href="{image["link"]}")')
                    if "width" in image:
                        self.lines.append(
                            f'{self.id_list[5]}img.post-image(src="{image["link"]}" alt="{image["alt"]}" style="width:{image["width"]};")')
                    else:
                        self.lines.append(
                            f'{self.id_list[5]}img.post-image(src="{image["link"]}" alt="{image["alt"]}")')
                    self.lines.append(
                        f'{self.id_list[4]}figcaption.post-image-caption {image["caption"]}')
            
            temp_paragraph = ''
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
                        f'{self.id_list[4]}| {items[idx]} ')
                
                # search for id in list
                for link in content['links']:
                    if link['id'] == link_id:
                        text = self.__get_non_id_from_string(item['item'])
                        self.lines.append(
                            f'{self.id_list[4]}a.post-link(href="{link["link"]}") {link["text"]}')
                        # Add rest of paragraph
                        self.lines.append(
                            f'{self.id_list[4]}| {text} ')
                
                temp_paragraph = self.__remove_key(temp_paragraph,item['item_with_key'])
                
        # Check for lists in text
        if ':listPlace' in temp_paragraph:
            items, positions = self.__parse_string(temp_paragraph,':listPlace')
            for item in positions:
                matches = re.search(r"listPlace\(\d{3}\)", item['item_with_key'])
                if matches:
                    list_id = self.__get_id_from_string(item['item'])
                    # print(temp_paragraph[:item["position"] - item["key_length"]])
                    # Write text to file up until position of key
                    self.lines.append(
                        f'{self.id_list[3]}p.post-details {temp_paragraph[:item["position"] - item["key_length"]]}')
                    
                    # Search for id in list
                    for list in content['lists']:
                        if list['id'] == list_id:
                            # Legacy
                            if "list_type" in list:
                                if list['list_type'] == 'unordered':
                                    self.lines.append(f'{self.id_list[3]}ul')
                                else:
                                    self.lines.append(f'{self.id_list[3]}ol')
                            elif "listType" in list:
                                if list['listType'] == 'unordered':
                                    self.lines.append(f'{self.id_list[3]}ul')
                                else:
                                    self.lines.append(f'{self.id_list[3]}ol')
                                
                            # Loop through list items
                            for li_item in list['items']:

                                # Check for any sublist in list
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
                                                    # Legacy
                                                    if "list_type" in sub_list:
                                                        if sub_list['list_type'] == 'unordered':
                                                            self.lines.append(
                                                                f'{self.id_list[5]}ul.sublist')
                                                        else:
                                                            self.lines.append(
                                                                f'{self.id_list[5]}ol.sublist')
                                                    elif "listType" in sub_list:
                                                        if sub_list['listType'] == 'unordered':
                                                            self.lines.append(
                                                                f'{self.id_list[5]}ul.sublist')
                                                        else:
                                                            self.lines.append(
                                                                f'{self.id_list[5]}ol.sublist')
                                                    
                                                    for slitem in sub_list['items']:
                                                        self.lines.append(
                                                            f'{self.id_list[6]}li.post-sublist-item {slitem}')
                                            
                                            temp_paragraph = self.__remove_key(li_item,subpos['item_with_key'])
                                            # print(temp_paragraph)
                                else:
                                    if ':user-defined-code' in li_item:
                                        code_ = self.__find_user_defined_code(li_item)
                                        # print(code_)

                                        self.lines.append(f'{self.id_list[4]}li.post-list-item')
                                        self.lines.append(f'{self.id_list[5]}| {code_["before_text"]} ')
                                        self.lines.append(
                                            f'{self.id_list[5]}span.user-define-code {code_["user_defined_code"]}')  # this can
                                        self.lines.append(
                                            f'{self.id_list[5]}| {code_["after_text"]}')
                                    else:
                                        self.lines.append(
                                            f'{self.id_list[4]}li.post-list-item {li_item}')
                    # Remove list key
                    temp_paragraph = self.__remove_key(temp_paragraph,item['item_with_key'])
            
            # Clear the paragraph
            temp_paragraph = ''       
        if ':codePlace' in temp_paragraph:

            # items, positions = self.__parse_string(temp_paragraph,':codePlace')
            l_start = len(':codePlace(XYZ)')
            idx_start = temp_paragraph.index(':codePlace')
            code_location = temp_paragraph[idx_start:idx_start + l_start]
            code_id = code_location[-4:-1]
            self.lines.append(
                f'{self.id_list[3]}p.post-details {temp_paragraph[:idx_start]}')
            
            temp_paragraph = ''
            
            # Loop through code list
            for code in content['code']:
                if code['id'] == code_id:
                    if not code['language'] in self.languages:
                        self.languages.append(code['language'])
                    self.__addCodeBlock(code)

        if ':user-defined-code' in temp_paragraph:
            code_ = self.__find_user_defined_code(li_item)
            # print(code_)

            self.lines.append(f'{self.id_list[3]}p.post-details')
            self.lines.append(f'{self.id_list[4]}| {code_["before_text"]} ')
            self.lines.append(
                f'{self.id_list[4]}span.user-define-code {code_["user_defined_code"]}')  # this can
            self.lines.append(
                f'{self.id_list[4]}| {code_["after_text"]}')
        
        # Check for bold and italic texts
        if ':special-text(key=' in temp_paragraph:
            p = self.__parse_string_to_get_between_par(temp_paragraph,':special-text', left_delimiter='(key=')
            start_idx = 0
            # Iterate through 
            for idx, item in enumerate(p):
                # print(item)
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
            # print(temp_paragraph)
        
        
    def __addJavascriptFiles(self):
        self.pm.addJavascriptFile(js_filename='scripts/main.js')
        if self.code_script_added:
            self.pm.addJavascriptFile(js_filename='scripts/code_script.js')
            self.pm.addPrismCode(self.languages)
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
            right_index = item.find(right_delimiter+end_key)

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
    
    def __find_user_defined_code(self, text):
        start_marker = ':user-defined-code'
        end_marker = ':end'
        
        start_index = text.find(start_marker)
        end_index = text.find(end_marker)
        
        if start_index == -1 or end_index == -1:
            return None
        
        start_index += len(start_marker)
        user_defined_code = text[start_index:end_index].strip()
        
        before_text = text[:start_index - len(start_marker)].strip()
        after_text = text[end_index + len(end_marker):].strip()
        
        return {
            'location': (start_index, end_index),
            'before_text': before_text,
            'user_defined_code': user_defined_code,
            'after_text': after_text
        }
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
