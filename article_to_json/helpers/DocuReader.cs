using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using article_to_json.classes;
using Microsoft.Office.Interop.Word;

namespace article_to_json.helpers
{
    class DocuReader
    {
        public Article article { get; }
        private string filepath;
        public DocuReader(string documentTitle)
        {
            filepath = String.Format(@"F:\Documents\blog_articles\{0}.docx", documentTitle);
            // Console.WriteLine(filepath);
            

            if ( !parse_document() )
            {
                Console.WriteLine("Can not parse document because document doesn't not exist.");
                Console.WriteLine("Check the following file path: {0}", filepath);
            }
            else
            {

            }
        }

        

        private Boolean parse_document()
        {
            if (!File.Exists(filepath))
            {
                return false;
            }

            Application application = new Application();
            application.Visible = false;
            Document document = application.Documents.Open(filepath);
            int wordCount = document.Words.Count;
            //;
            //document.Lists.Count;
            //document.Hyperlinks.Count;
            Console.WriteLine("Paragraph Count: {0}", document.Paragraphs.Count);
            Console.WriteLine("Word Count: {0}", wordCount);
            /*
            foreach (List list in document.Lists)
            {
                //Type type = list.GetType();
                string styleName = list.StyleName;
                //string text = paragraph.Range.Text;


                Console.WriteLine("List Style: {0}", list.Range);
            }
            */
            int paragraphIdx = 0;
            int trueIdx = 0;
            int listIdx = 0;

            Content content = new Content();
            foreach (Paragraph paragraph in document.Paragraphs)
            {
                Style style = paragraph.get_Style() as Style;
                string styleName = style.NameLocal;
                string text = paragraph.Range.Text;

                Console.WriteLine("Style Name: {0}", styleName);
                Console.WriteLine("Text: {0}\nLength: {1}", text, text.Length);
                try
                {
                    switch (styleName)
                    {
                        case "Heading 1":
                        case "Heading 2":
                            {
                                content.title.tag = "h2";
                                content.title.text = text;
                                Console.WriteLine(content.title);
                                break;
                            }

                        case "Normal":
                            {
                                // Make sure there is text to read
                                if (text.Length > 1)
                                {
                                    
                                    string paragraphText = "";
                                    // Check if paragraph has links
                                    int linksCount = paragraph.Range.Hyperlinks.Count;

                                    if (linksCount > 0)
                                    {
                                        int idx = 0;
                                        List<ContentLink> links = new List<ContentLink>();
                                        foreach (Hyperlink link in paragraph.Range.Hyperlinks)
                                        {
                                            string linkPlace = String.Format(":linkPlace({0,2:D3})", idx + 1);
                                            string linkText = link.TextToDisplay;
                                            string linkAddress = link.Address;
                                            //Console.WriteLine("Link Text: {0}", linkText);
                                            //Console.WriteLine("Link Place: {0}", linkPlace);
                                            //Console.WriteLine("Link Address: {0}", linkAddress);

                                            // Replace Text with :linkPlace(001)
                                            paragraphText = text.Replace(linkText, linkPlace);
                                            Console.WriteLine("Link Text: {0}", paragraphText);
                                            ContentLink contentLink = new ContentLink();
                                            contentLink.id = String.Format("{0,2:D3}", idx + 1);
                                            contentLink.link = linkAddress;
                                            contentLink.text = linkText;
                                            links.Add(contentLink);

                                            Console.WriteLine(contentLink.ToString());
                                            idx += 1;
                                        }// end foreach links
                                        content.links = links;
                                    }

#if NOT_READY
                                    // Check if any word is bold or italized
                                    if (paragraph.Range.Font.Bold == -1)
                                {
                                    Console.WriteLine("Is bold");
                                    Console.Read();
                                }
#endif
                                    content.paragraghs.Add(paragraphText);
                                    trueIdx += 1;
                                }// end if
                                break;
                            }
                        case "List Paragraph":
                            {
                                //Console.WriteLine(content.ToString());
                                // Get previous paragraph to append to end
                                if (content.paragraghs.Count >= 1)
                                {
                                    // Add to end of previous paragraph
                                    string listPlace = String.Format(":listPlace({0,2:D3})", listIdx + 1);
                                    Console.WriteLine(content.paragraghs.Count);
                                    content.paragraghs[trueIdx - 1] += listPlace;
                                    listIdx += 1;
                                }
                                break;
                            }
                        default:
                            {
                                break;
                            }
                    }// end switch
                } // end try
                catch (IOException e)
                {
                    // Extract some information from this exception, and then
                    // throw it to the parent method.
                    if (e.Source != null)
                        Console.WriteLine("IOException source: {0}", e.Source);
                    break;
                }
                catch (NullReferenceException e )
                {
                    Console.WriteLine("NullReferenceException message: {0}", e.Message);
                    if (e.Source != null)
                        Console.WriteLine("NullReferenceException source: {0}", e.Source);
                    break;
                }
                catch
                {
                    break;
                }
                

                paragraphIdx += 1;
            }// end foreach paragraph
            Console.WriteLine(content.title.text);
            foreach(ContentLink link in content.links)
            {
                Console.WriteLine("{0}, {1}",link.link, link.text);
            }
            // Close word.
            document.Save();
            application.Quit();
            return true;
        }
    }
}
