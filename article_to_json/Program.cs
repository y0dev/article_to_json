using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using article_to_json.classes;
using article_to_json.helpers;

namespace article_to_json
{
    class Program
    {
        static void Main(string[] args)
        {
            // The code provided will print ‘Hello World’ to the console.
            // Press Ctrl+F5 (or go to Debug > Start Without Debugging) to run your app.
            Console.WriteLine("Hello World!");
            Article article;
            DocuReader docuReader = new DocuReader("Why am I Presbyterian");
            article = docuReader.article;
            article.title = "Why am I Presbyterian";
            string stringjson = JsonConvert.SerializeObject(article);
            stringjson.Replace("\r", "");
            Console.WriteLine(stringjson);
            Console.ReadKey();
        }
    }
}
