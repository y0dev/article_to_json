using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using article_to_json.classes;
using article_to_json.helpers;
using System.IO;

namespace article_to_json
{
    class Program
    {
        static void Main(string[] args)
        {
            string Title = "";
            string Filename = "";
            string ID = "";
            string ImageName = "";
            string ImageAlt = "";
            List<string> TagList = new List<string>();

            if ( args.Length > 0 )
            {
                Title = args[0];
                Filename = args[0];
                ID = args[0].Replace(" ","-").ToLower();

                if (args.Length > 1 & args.Length <= 2) // Include tags
                {

					Tags tags = new Tags(args[1]);
					TagList = tags.getTagList();
                }
                else if (args.Length > 2 & args.Length <= 4) // Include tags and image
                {
					Tags tags = new Tags(args[1]);
					TagList = tags.getTagList();

					ImageName = args[2];
                    ImageAlt = args[3];
                }
				else
				{
					Console.WriteLine("\nToo many arguments!!!\n");
					// Add Help Menu
					return;
				}
            }
            // Run on sample.docx
            else
            {
                Console.WriteLine("\nRunning on Sample.docx\n");
				Tags tags = new Tags("Sample");
				TagList = tags.getTagList();
			}

            Article article;
            string file = Filename == "" ? "Sample" : Filename;
            string title = Title == "" ? "Sample" : Title;

            DocuReader docuReader = new DocuReader(file);
            article = docuReader.article;
            article.id = ID;
            article.title = title;
            article.tags = TagList;
            article.image.name = ImageName;
            article.image.alt = ImageAlt;
            article.date = DateTimeOffset.Now.ToUnixTimeMilliseconds().ToString();

            string stringjson = JsonConvert.SerializeObject(article);
            // Console.WriteLine(stringjson);
            Console.WriteLine("Finished");
            File.WriteAllText(String.Format(@"F:\Documents\blog_articles\json_outputs\{0}.json", title.ToLower()), stringjson);
            // Console.ReadKey();
        }
    }
}
