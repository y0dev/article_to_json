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
			string DocType = "Sample";

			Article article;
			List<string> TagList = new List<string>();

            if ( args.Length > 0 )
            {
                Title = args[0];
                Filename = args[0];
                ID = args[0].Replace(" ","-").ToLower();

                if (args.Length > 1 & args.Length <= 2) // Include article type
                {
					DocType = args[1];
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
			}

            string file = Filename == "" ? "Sample" : Filename;
            string title = Title == "" ? "Sample" : Title;

            DocuReader docuReader = new DocuReader(file);
            article = docuReader.article;
            article.id = article.id == "" ? ID : article.id;
			article.generateImage( DocType );
            article.title = title;

			Tags tags = new Tags( DocType );
			TagList = tags.getTagList();

			article.tags = TagList;
			DateTime dt = new DateTime(DateTime.Today.Year, DateTime.Today.Month, DateTime.Today.Day);

			DateTimeOffset dto = new DateTimeOffset(dt);
			article.date = dto.ToUnixTimeMilliseconds().ToString();

            string stringjson = JsonConvert.SerializeObject(article, Formatting.Indented);
			// Console.WriteLine(stringjson);

			File.WriteAllText(String.Format(@"F:\Documents\blog_articles\json_outputs\{0}.json", title.ToLower()), stringjson);

			Console.WriteLine("Finished");

			// Console.ReadKey();
        }
    }
}
