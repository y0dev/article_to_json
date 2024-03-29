﻿using System;
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

			float documentWidth = document.PageSetup.PageWidth;
			
			// Calculate three-fourths of the page width
			float threeFourthPageWidth = (3f / 4f) * documentWidth;


			Regex regx = new Regex(@"[\u25A0\u00A0\s]+",
				RegexOptions.Compiled | RegexOptions.IgnoreCase);
			bool articleTitleFound = false;
			bool articleIdFound = false;
			bool descriptionFound = false;
			bool codeBlockFound = false;
			int trueIdx = 0; // This is for each content in the document based on finding the heading or a title

            int paragraphIdx = 0;

            int listIdx = 0;
			int codeIdx = 0;

			bool imageFound = false;
			int imageIdx = 0;

			bool sameList = false;
			bool sameSublist = false;
            
            foreach (Paragraph paragraph in document.Paragraphs)
            {
                Style style = paragraph.get_Style() as Style;
                string styleName = style.NameLocal;
                string text = paragraph.Range.Text.Replace("\r", String.Empty);
				int textLength = text.Length;
				string formattedString = "";

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
					image.width = shape.Width < threeFourthPageWidth ? "auto" : "";


					article.content[ trueIdx - 1 ].paragraphs[ paragraphIdx - 1 ] += imagePlace;
					article.content[ trueIdx - 1 ].images.Add( image );

					imageFound = true;
					imageIdx += 1;
					continue;
				}

				// Check if this is a code block
				if (text == "code-start" && !codeBlockFound)
				{
					// Create a new code object
					// Console.WriteLine("Code Start: {0}", text);
					string codePlace = String.Format(":codePlace({0,2:D3})", codeIdx + 1);
					Code code = new Code();
					code.id = String.Format("{0,2:D3}", codeIdx + 1);

					// Add code to content
					article.content[trueIdx - 1].code.Add(code);
					article.content[trueIdx - 1].paragraphs[paragraphIdx - 1] += codePlace;

					codeIdx += 1;
					codeBlockFound = true;
					continue;
				}
				else if (text == "code-end" && codeBlockFound)
				{
					// Console.WriteLine("Code End: {0}", text);
					codeBlockFound = false;
					continue;
				}
				else if (codeBlockFound)
				{
					if(text.ToLower().Contains("language= "))
					{
						int startIdx = "language= ".Length;
						string language = text.Substring(startIdx);
						article.content[trueIdx - 1].code[codeIdx - 1].language = language;
						continue;
					}
					else if (text.ToLower().Contains("code-title= "))
					{
						int startIdx = "code-title= ".Length;
						string codeTitle = text.Substring(startIdx);
						article.content[trueIdx - 1].code[codeIdx - 1].title = codeTitle;
						continue;
					}
					article.content[trueIdx - 1].code[codeIdx - 1].content.Add(text);
					// Console.WriteLine("Code: {0}", text);
					continue;
				}

				try
                {


					switch (styleName)
					{
						case "Heading 1":
							{
								Content content = new Content();
								article.content.Add(content);
								content.title.tag = "h2";
								content.title.text = text.Replace("\r", String.Empty);

								// Console.WriteLine(content.title);
								trueIdx += 1;
								paragraphIdx = 0;
								listIdx = 0;
								sameList = false;
								sameSublist = false;
								break;
							}
						case "Heading 2":
							{
								Content content = new Content();
								article.content.Add(content);
								content.title.tag = "h3";
								content.title.text = text.Replace("\r", String.Empty);

								// Console.WriteLine(content.title);
								trueIdx += 1;
								paragraphIdx = 0;
								listIdx = 0;
								sameList = false;
								sameSublist = false;
								break;
                            }

                        case "Normal":
                            {
								// Clear index counts at the start of each paragraph
								if (listIdx != 0)
								{
									listIdx = 0;
								}

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
									int boldStart  = -1;
									int boldEnd = -1;

									int italicStart = -1;
									int italicEnd = -1;
									// :special-text(key=
									// )special-text-end
									if (rangeWord.Bold != 0 && rangeWord.Italic != 0)
									{
										// If we're not already in a bold and italicized word, record the start position
										if (boldStart == -1 && italicStart == -1)
										{
											boldStart = rangeWord.Start;
											italicStart = rangeWord.Start;
										}
										// If we're already in a bold and italicized word, update the end position
										boldEnd = rangeWord.End;
										italicEnd = rangeWord.End;
									}
									if (rangeWord.Bold != 0)
									{
										// If we're not already in an bold word, record the start position
										if ( boldStart  == - 1 )
										{
											boldStart = rangeWord.Start;
										}
										// If we're already in an italicized word, update the end position
										boldEnd = rangeWord.End;

										Range wordRange = document.Range(boldStart, boldEnd);
										// Check for (***)
										/*
										if ( wordRange.Text == "(" )
										{
											// Check paragraph for next )
											Range paragraphRange = paragraph.Range;
											// Find the first closing parenthesis starting from the specified index
											int closingParenIndex = FindNextClosingParenthesis(paragraphRange.Text, boldStart);

											if (closingParenIndex != -1)
											{
												Console.WriteLine($"Closing parenthesis found at index: {closingParenIndex}");
											}
											else
											{
												Console.WriteLine("Closing parenthesis not found.");
											}
										}
										*/
										string boldString = String.Format(":special-text(key=bold,{0})special-text-end ", wordRange.Text);
										// Console.WriteLine($"{boldString}");
										rangeWord.Bold = 0;
										rangeWord.Text = boldString;
										
									}
									else if (rangeWord.Italic != 0)
									{
										//Console.WriteLine(rangeWord.Text);
										if (italicStart == -1)
										{
											italicStart = rangeWord.Start;
										}
										// If we're already in an italicized word, update the end position
										italicEnd = rangeWord.End;
										Range wordRange = document.Range(italicStart, italicEnd);
										string italicString = String.Format(":special-text(key=italic,{0})special-text-end ", wordRange.Text);
										//Console.WriteLine($"{italicString}");
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
									// Add Links to paragraph
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
										if (formattedString != "")
										{
											Console.WriteLine(formattedString);
											formattedString = "";
										}
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

								// Get level of list
								int listLevel = GetListLevel(paragraph.Range.ListFormat);

								// Determine the type of list
								string listType = paragraph.Range.ListFormat.ListType.ToString();

								string listPlace = String.Format(":listPlace({0,2:D3})", listIdx + 1);

                                // Add to end of previous paragraph
                                if ( !sameList )
                                {
                                    // Console.WriteLine(article.content[trueIdx - 1].paragraghs.Count);
									// Append list placement to paragraph
                                    article.content[trueIdx - 1].paragraphs[paragraphIdx - 1] += listPlace;

									// Create a content list object
									ContentList clist = CreateContentList(trueIdx, listType, listIdx + 1, text.Replace("\r", String.Empty));
                                    article.content[trueIdx - 1].lists.Add(clist);

                                    listIdx += 1;
                                    sameList = true;
									sameSublist = false;
								}
                                else // List has already been created just update list items
                                {
									// Check for sublist
									if (listLevel > 1)
									{
										// Create new sublist
										if ( !sameSublist )
										{
											int listItemLength = article.content[trueIdx - 1].lists[listIdx - 1].items.Count;
											// Append to previous list text
											article.content[trueIdx - 1].lists[listIdx - 1].items[listItemLength - 1] += listPlace;

											// Create a content list object
											ContentList clist = CreateContentList(trueIdx, listType, listIdx + 1, text.Replace("\r", String.Empty));
											article.content[trueIdx - 1].lists.Add(clist);
											listIdx += 1;
											sameSublist = true;
										}
										else
										{
											// Append text to list
											article.content[trueIdx - 1].lists[listIdx - 1].items.Add(text.Replace("\r", String.Empty));
										}

									}
									else
									{
										// Append text to list
										article.content[trueIdx - 1].lists[listIdx - 1].items.Add(text.Replace("\r", String.Empty));
									}


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

		private int FindNextClosingParenthesis(string text, int startIndex)
		{
			for (int i = startIndex; i < text.Length; i++)
			{
				if (text[i] == ')')
				{
					return i;
				}
			}
			return -1;
		}

		private int GetListLevel(ListFormat listFormat)
		{
			if (listFormat.ListType != WdListType.wdListNoNumbering)
			{
				return listFormat.ListLevelNumber;
			}
			return 0;
		}

		private ContentList CreateContentList(int paragraphIndex, string listType, int listIndex, string text)
		{
			// Create a content list object
			ContentList clist = new ContentList();
			clist.id = String.Format("{0,2:D3}", listIndex);
			clist.items.Add(text.Replace("\r", String.Empty));
			clist.listType = listType == "wdListBullet" ? "unordered" : "ordered";

			return clist;
		}
	} // end class
} // end namespace
