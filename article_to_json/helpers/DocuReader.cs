using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using article_to_json.classes;
using Microsoft.Office.Interop.Word;


namespace article_to_json.helpers
{
	class DocuReader
    {
		const int MAX_TITLE_LENGTH = 3;
		public Article article { get; }
		public bool fileCreated { get; }
        private string filepath;

        public DocuReader(string documentTitle)
        {
            filepath = String.Format(@"F:\Documents\blog_articles\{0}.docx", documentTitle);
            // Console.WriteLine(filepath);

            article = new Article();
            article.content = new List<Content>();
			fileCreated = true;
			if ( !parse_document() )
            {
				fileCreated = false;
            } 
			else
			{
				int wordCount = 0;
				foreach( Content content in article.content )
				{
					foreach ( string paragraph in content.paragraphs )
					{
						wordCount +=  paragraph.Split(new string[] { " " }, StringSplitOptions.None).Length;
					}

					foreach ( ContentList list in content.lists )
					{
						foreach ( string item in list.items )
						{
							wordCount += item.Split(new string[] { " " }, StringSplitOptions.None).Length;
						}
					}
				}
				article.time = new TimeToRead( wordCount );
			}
        }

        

        private Boolean parse_document()
        {
            if ( !File.Exists(filepath) )
            {
				Console.WriteLine("Can not parse document because document doesn't not exist.");
				Console.WriteLine("Check the following file path: {0}", filepath);
				return false;
            }  
			

			Application application = new Application();
            application.Visible = false;
            Document document = application.Documents.Open(filepath, ReadOnly: true);
			

			Regex regx = new Regex(@"[\u25A0\u00A0\s]+",
				RegexOptions.Compiled | RegexOptions.IgnoreCase);
			bool articleTitleFound = false;
			bool articleIdFound = false;
			bool descriptionFound = false;
			int trueIdx = 0; // This is for each content in the document based on finding the heading or a title

            int paragraphIdx = 0;

            int listIdx = 0;

			bool imageFound = false;
			int imageIdx = 0;

			bool sameList = false;
            
            foreach (Paragraph paragraph in document.Paragraphs)
            {
                Style style = paragraph.get_Style() as Style;
                string styleName = style.NameLocal;
                string text = paragraph.Range.Text.Replace("\r", String.Empty);

				// Console.WriteLine("Style Name: {0}", styleName);
				// Console.WriteLine("Text: {0}\nLength: {1}", text, text.Length);

				// Check for title
				if (text.ToLower().Contains("article-title =") && !articleTitleFound)
				{
					int startIdx = "article-title = ".Length;
					string title = text.Substring(startIdx);
					article.title = title;
					articleTitleFound = true;
					continue;
				}

				// Check for id
				if ( text.ToLower().Contains("article-id =")  && !articleIdFound )
				{
					int startIdx = "article-id = ".Length;
					string id = text.Substring(startIdx).Replace(" ","-");
					article.id = id;
					// Console.WriteLine($"id = {id}");
					articleIdFound = true;
					continue;
				}

				// Handle the input of description
				if ( descriptionFound && text != "" )
				{
					article.description = text;
					descriptionFound = false;
					continue;
				}

				// Add caption to recently added image
				if ( imageFound )
				{
					article.content[trueIdx - 1].images[imageIdx - 1].caption = text;
					imageFound = false;
					continue;
				}

				// Check for images
				if (paragraph.Range.InlineShapes.Count > 0 && paragraph.Range.InlineShapes[1] != null )
				{
					// Handle cases where there are a paragraph before
					if ( article.content[trueIdx - 1].paragraphs.Count < 1 || 
						 article.content[trueIdx - 1].paragraphs[paragraphIdx - 1].Contains("listPlace") ||
						 article.content[trueIdx - 1].paragraphs[paragraphIdx - 1].Contains("imagePlace") )
					{
						article.content[trueIdx - 1].paragraphs.Add("");
						paragraphIdx += 1;
					}
					
					InlineShape shape = paragraph.Range.InlineShapes[1];
					// Console.WriteLine($"Shape (width,height) = ({shape.Width},{shape.Height})");
					// Console.WriteLine($"Shape address = {shape.Hyperlink.Address}");
					// Console.WriteLine($"Caption {paragraph.Range}");
					string imagePlace = String.Format(":imagePlace({0,2:D3})", imageIdx + 1);

					ContentImage image = new ContentImage();
					image.alt = "";
					image.link = shape.Hyperlink.Address;
					image.id = String.Format("{0,2:D3}", imageIdx + 1);


					article.content[ trueIdx - 1 ].paragraphs[ paragraphIdx - 1 ] += imagePlace;
					article.content[ trueIdx - 1 ].images.Add( image );

					imageFound = true;
					imageIdx += 1;
					continue;
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

								// Check if text is Description
								if ( text.ToLower() == "description" )
								{
									descriptionFound = true;
									continue;
								}


								// Check if any word is bold or italized
								foreach (Range rangeWord in paragraph.Range.Words)
								{
									// :special-text(key=
									// )special-text-end
									if (rangeWord.Bold != 0)
									{
										string boldString = String.Format(":special-text(key=bold,{0})special-text-end", rangeWord.Text);
										// Console.WriteLine($"{boldString}");
										rangeWord.Bold = 0;
										rangeWord.Text = boldString;
									}
									else if (rangeWord.Italic != 0)
									{
										string italicString = String.Format(":special-text(key=italic,{0})special-text-end", rangeWord.Text);
										// Console.WriteLine($"{italicString}");
										rangeWord.Italic = 0;
										rangeWord.Text = italicString;

									}
									/*
									else if (rangeWord.Underline != 0)
									{
										string underlineString = String.Format(":special-text(key=underline,{0})special-text-end", rangeWord.Text);
										Console.WriteLine($"{underlineString}");
										rangeWord.Underline = 0;
										rangeWord.Text = underlineString;

									}
									*/
								}

								text = paragraph.Range.Text.Replace("\r", String.Empty);

								// Remove all spaces to verify that there is text in the string
								string trimText = text.Trim();
								// Make sure there is text to read
								if (trimText.Length > 1 && words.Length > MAX_TITLE_LENGTH )
                                {
                                    
                                    string paragraphText = "";

                                    // Check if paragraph has links
                                    int linksCount = paragraph.Range.Hyperlinks.Count;

                                    if (linksCount > 0)
                                    {
                                        int idx = 0;
                                        List<ContentLink> links = new List<ContentLink>();
										string paragraphTextLinks = text;

										foreach (Hyperlink link in paragraph.Range.Hyperlinks)
                                        {
                                            string linkPlace = String.Format(":linkPlace({0,2:D3})", idx + 1);
                                            string linkText = link.TextToDisplay;
                                            string linkAddress = link.Address;
											// Console.WriteLine("Link Text: {0}", linkText);
											//Console.WriteLine("Link Place: {0}", linkPlace);
											//Console.WriteLine("Link Address: {0}", linkAddress);

											// Replace Text with :linkPlace(001)
											paragraphTextLinks = paragraphTextLinks.Replace(linkText, linkPlace)
																.Replace("\r", String.Empty);
											// paragraphTextLinks = regx.Replace(paragraphTextLinks, String.Empty);
                                            // Console.WriteLine("Link Text: {0}", paragraphTextLinks);

                                            ContentLink contentLink = new ContentLink();
                                            contentLink.id = String.Format("{0,2:D3}", idx + 1);
                                            contentLink.link = linkAddress;
                                            contentLink.text = linkText;
                                            links.Add(contentLink);

                                            // Console.WriteLine(contentLink.ToString());
                                            idx += 1;
                                        }// end foreach links
                                        article.content[trueIdx - 1].links = links;
										paragraphText = paragraphTextLinks.Replace("\r", String.Empty);
									}
                                    else
                                    {
                                        paragraphText = text.Replace("\r", String.Empty);
                                    }

                                    article.content[trueIdx - 1].paragraphs.Add(paragraphText);
                                    paragraphIdx += 1;
                                }// end if
                                else if ( trimText != "" && ( words.Length >= 1 && words.Length <= MAX_TITLE_LENGTH) )
                                {
									//Edge case where " " gets registered as a title
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
                catch (Exception e)
                {
					Console.WriteLine("Exception message: {0}", e.Message);
					if (e.Source != null)
						Console.WriteLine("Exception source: {0}", e.Source);
					break;
                }

			}// end foreach paragraph

			// Close word.
			object saveOption = WdSaveOptions.wdDoNotSaveChanges;
			object originalFormat = WdOriginalFormat.wdOriginalDocumentFormat;
			object routeDocument = false;
			document.Close(ref saveOption, ref originalFormat, ref routeDocument);
			// document.Save();
            application.Quit();
            return true;
        } // end parseDoc()


	} // end class
} // end namespace
