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
			const string menuString = "Article to JSON\n" +
								"\n" +
								"To use: \n" +
								"                        article_to_json.exe \"document-name\" \"document-category\"\n" +
								"                                                                or\n" +
								"                        article_to_json.exe \"document-name\"";



			string Title = "";
            string Filename = "";
			string DocType = "Sample";

			List<string> TagList = new List<string>();

            if ( args.Length > 0 )
            {
                Title = args[0];
                Filename = args[0];

                if (args.Length > 1 & args.Length <= 2) // Include article type
                {
					DocType = args[1];
                }
				else if ( args.Length > 2 )
				{
					Console.WriteLine("\nToo many arguments!!!\n");
					Console.WriteLine(menuString);
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
            string title = Title == "" ? "Sample" : Title.Replace("-", " ").Replace("_", " ");

            DocuReader docuReader = new DocuReader(file);
			if (docuReader.fileCreated)
			{

				Article article;
				article = docuReader.article;
				article.generateImage(DocType);

				Tags tags = new Tags(DocType);
				TagList = tags.getTagList();

				article.tags = TagList;
				DateTime dt = new DateTime(DateTime.Today.Year, DateTime.Today.Month, DateTime.Today.Day);

				DateTimeOffset dto = new DateTimeOffset(dt);
				article.date = dto.ToUnixTimeMilliseconds().ToString();

				string stringjson = JsonConvert.SerializeObject(article, Formatting.Indented);
				// Console.WriteLine(stringjson);

				File.WriteAllText(String.Format(@"F:\Documents\blog_articles\json_outputs\{0}.json", title.ToLower().Replace(" ", "-")), stringjson);

				Console.WriteLine("Finished");

			}


			Console.ReadKey();
        }

		private static string FirstCharToUpper(string input)
		{
			switch (input)
			{
				case null: throw new ArgumentNullException(nameof(input));
				case "": throw new ArgumentException($"{nameof(input)} cannot be empty", nameof(input));
				default: return input[0].ToString().ToUpper() + input.Substring(1);
			}
		}
	}
}
