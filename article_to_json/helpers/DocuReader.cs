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

            article = new Article();
            article.content = new List<Content>();
            if ( !parse_document() )
            {
                Console.WriteLine("Can not parse document because document doesn't not exist.");
                Console.WriteLine("Check the following file path: {0}", filepath);
            }
        }

        

        private Boolean parse_document()
        {
            if (!File.Exists(filepath))
            {
                return false;
            }
#if KEEP
			// Load the Word document.
			Aspose.Words.Document doc = new Aspose.Words.Document(filepath);

			// Shape nodes that have the "HasImage" flag set contain and display images.
			IEnumerable<Aspose.Words.Drawing.Shape> shapes = doc.GetChildNodes(Aspose.Words.NodeType.Shape, true)
				.OfType<Aspose.Words.Drawing.Shape>().Where(s => s.HasImage);
			int imageIndex = 0;

			// Loop through shapes.
			foreach (Aspose.Words.Drawing.Shape shape in shapes)
			{
				// Save images.
				string imageFileName =
					$"Image_{imageIndex}{Aspose.Words.FileFormatUtil.ImageTypeToExtension(shape.ImageData.ImageType)}";
				shape.ImageData.Save(imageFileName);
				imageIndex++;
			}
#endif           

			Application application = new Application();
            application.Visible = false;
            Document document = application.Documents.Open(filepath);
            int wordCount = document.Words.Count;

            int paragraphIdx = 0;
            int trueIdx = 0;
            int listIdx = 0;
			int imageIdx = 0;

			bool sameList = false;
			//grabImages(document);
            
            foreach (Paragraph paragraph in document.Paragraphs)
            {
                Style style = paragraph.get_Style() as Style;
                string styleName = style.NameLocal;
                string text = paragraph.Range.Text.Replace("\r", String.Empty);

				// Console.WriteLine("Style Name: {0}", styleName);
				// Console.WriteLine("Text: {0}\nLength: {1}", text, text.Length);

				// Check for images
				if (paragraph.Range.InlineShapes.Count > 0 && paragraph.Range.InlineShapes[1] != null )
				{


					// Handle cases where there are a paragraph before
					if (article.content[trueIdx - 1].paragraphs.Count < 1)
					{
						article.content[trueIdx - 1].paragraphs.Add("");
						paragraphIdx += 1;
					}


					InlineShape shape = paragraph.Range.InlineShapes[1];
					string imagePlace = String.Format(":imagePlace({0,2:D3})", imageIdx + 1);

					ContentImage image = new ContentImage();
					image.alt = "";
					image.caption = "";
					image.link = shape.Hyperlink.Address;
					image.id = String.Format("{0,2:D3}", imageIdx + 1);


					article.content[trueIdx - 1].paragraphs[paragraphIdx - 1] += imagePlace;
					article.content[trueIdx - 1].images.Add(image);

					imageIdx += 1;

					// Console.WriteLine($"Shape (width,height) = ({shape.Width},{shape.Height})");
					Console.WriteLine($"Shape type = {shape.Title}");
					Console.WriteLine($"Shape type = {shape.AlternativeText}");
					// Console.WriteLine($"Shape address = {shape.Hyperlink.Address}");
				}
				try
                {


					switch (styleName)
                    {
                        case "Heading 1":
                        case "Heading 2":
                            {
                                Content content = new Content();
                                article.content.Add(content);
                                content.title.tag = "h2";
                                content.title.text = text.Replace("\r", String.Empty);

                                // Console.WriteLine(content.title);
                                trueIdx += 1;
                                paragraphIdx = 0;
                                sameList = false;
                                break;
                            }

                        case "Normal":
                            {
                                string[] words = text.Split(new string[] { " " }, StringSplitOptions.None);
                                // Console.WriteLine("Word Length {0}",words.Length);

                                // Make sure there is text to read
                                if (text.Length > 1 && words.Length > 3 )
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
                                            paragraphText = text.Replace(linkText, linkPlace).Replace("\r", String.Empty);
                                            // Console.WriteLine("Link Text: {0}", paragraphText);

                                            ContentLink contentLink = new ContentLink();
                                            contentLink.id = String.Format("{0,2:D3}", idx + 1);
                                            contentLink.link = linkAddress;
                                            contentLink.text = linkText;
                                            links.Add(contentLink);

                                            // Console.WriteLine(contentLink.ToString());
                                            idx += 1;
                                        }// end foreach links
                                        article.content[trueIdx - 1].links = links;
                                    }
                                    else
                                    {
                                        paragraphText = text.Replace("\r", String.Empty);
                                    }

#if NOT_READY
                                    // Check if any word is bold or italized
                                    if (paragraph.Range.Font.Bold == -1)
                                {
                                    Console.WriteLine("Is bold");
                                    Console.Read();
                                }
#endif
                                    article.content[trueIdx - 1].paragraphs.Add(paragraphText);
                                    paragraphIdx += 1;
                                }// end if
                                else if ( text != "" && ( words.Length >= 1 && words.Length <= 3) )
                                {
                                    // Add another content since this is another heading
                                    Content content = new Content();
                                    article.content.Add(content);
                                    content.title.tag = "h2";
                                    content.title.text = text.Replace("\r", String.Empty);
                                    // Console.WriteLine(content.title);
                                    

                                    trueIdx += 1;
                                    listIdx = 0;
                                    paragraphIdx = 0;
                                    sameList = false;
                                }
                                break;
                            }
                        case "List Paragraph":
                            {
                                //Console.WriteLine(content.ToString());
                                // Handle cases where there are a paragraph before
                                if (article.content[trueIdx - 1].paragraphs.Count < 1 )
                                {
                                    article.content[trueIdx - 1].paragraphs.Add("");
                                    paragraphIdx += 1;
                                }


                                string listPlace = String.Format(":listPlace({0,2:D3})", listIdx + 1);

                                // Add to end of previous paragraph
                                if ( !sameList )
                                {
                                    // Console.WriteLine(article.content[trueIdx - 1].paragraghs.Count);
                                    article.content[trueIdx - 1].paragraphs[paragraphIdx - 1] += listPlace;

                                    string listType = paragraph.Range.ListFormat.ListType.ToString();
                                    ContentList clist = new ContentList();
                                    clist.id = String.Format("{0,2:D3}", listIdx + 1);
                                    clist.items.Add(text.Replace("\r", String.Empty));
                                    clist.listType = listType == "wdListBullet" ? "unordered" : "ordered";
                                    article.content[trueIdx - 1].lists.Add(clist);

                                    listIdx += 1;
                                    sameList = true;
                                }
                                else // List has already been created just update list items
                                {
                                    article.content[trueIdx - 1].lists[listIdx - 1].items.Add(text.Replace("\r", String.Empty));
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
                
            }// end foreach paragraph

            // Close word.
            document.Save();
            application.Quit();
            return true;
        } // end parseDoc()

		private void grabImages(Document doc)
		{
			foreach (InlineShape shape in doc.InlineShapes)
			{
				Console.WriteLine($"Shape (width,height) = ({shape.Width},{shape.Height})");
				Console.WriteLine($"Shape type = {shape.Type}");
				Console.WriteLine($"Shape title = {doc.Range(0)}");
				Console.WriteLine($"Shape address = {shape.Hyperlink.Address}");

				Console.WriteLine();
				if (shape.Type == WdInlineShapeType.wdInlineShapePicture)
				{
					// ...
				}
			}

		} // end grabImages()

#if KEEP
		private Image SaveInlineShapeToFile(int inlineShapeId, Microsoft.Office.Interop.Word.Application app)
		{
			var inlineShape = app.ActiveDocument.InlineShapes[inlineShapeId];
			inlineShape.Select();
			app.Selection.Copy();

			// Check data is in the clipboard
			if (Clipboard.GetDataObject() != null)
			{
				var data = Clipboard.GetDataObject();

				// Check if the data conforms to a bitmap format
				if (data != null && data.GetDataPresent(DataFormats.Bitmap))
				{
					// Fetch the image and convert it to a Bitmap
					Image image = (Image)data.GetData(DataFormats.Bitmap, true);
					return image;
				}
			}
			return null;
		}
#endif

	} // end class
} // end namespace
