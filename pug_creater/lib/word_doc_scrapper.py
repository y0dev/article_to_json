import win32com.client as winClient

# word = winClient.Dispatch("Word.Application")
# word.visible = False
# wb = word.Documents.Open("myfile.doc")
# doc = word.ActiveDocument
# print(doc.Range().Text)


class DocScrapper:
    def __init__(self, filename:str) -> None:
        self.filename = filename
        word = winClient.Dispatch("Word.Application")
        word.visible = False
        self.wb = word.Documents.Open(filename)
        self.doc = word.ActiveDocument
    
    def getText(self) -> str:
        return self.doc.Range().Text
    
ds = DocScrapper("F:\\Documents\\System Design.docx")
print(ds.getText())