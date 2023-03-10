using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace article_to_json.classes
{
    class ContentTitle
    {
        public string tag { get; set; }
        public string text { get; set; }

        public ContentTitle()
        {
            tag = "";
            text = "";
        }

        public override string ToString()
        {
            return String.Format("{0} {1}", text, tag);
        }
    }

    class ContentImage
    {
        public string id { get; set; }
        public string alt { get; set; }
        public string caption { get; set; }
        public string link { get; set; }

        public ContentImage()
        {
            id = "";
            alt = "";
            caption = "";
            link = "";
        }
    }

    class ContentLink
    {
        public string id { get; set; }
        public string text { get; set; }
        public string link { get; set; }

        public ContentLink()
        {
            id = "";
            text = "";
            link = "";
        }

        public override string ToString()
        {
            return String.Format("Link: {0}\t\t{1}\t\t{2}", id, text, link );
        }
    }

    class ContentList
    {
        public string id { get; set; }
        public List<string> items { get; set; }
        public string listType { get; set; }

        public ContentList()
        {
            id = "";
            items = new List<string>();
            listType = "";
        }
    }

	class ContentQuotes
	{
		public string id { get; set; }
		public string author { get; set; }
		public string text { get; set; }

		public ContentQuotes()
		{
			id = "";
			author = "";
			text = "";
		}
	}

	class ContentCode
	{
		public string id { get; set; }
		public string title { get; set; }
		public string language { get; set; }
		public List<string> content { get; set; }

		public ContentCode()
		{
			id = "";
			title = "";
			language = "";
			content = new List<string>();
		}
	}

	class Content
    {
        public ContentTitle title { get; set; }
        public List<string> paragraphs { get; set; }
        public List<ContentImage> images { get; set; }
        public List<ContentLink> links { get; set; }
        public List<ContentList> lists { get; set; }
		public List<ContentQuotes> quotes { get; set; }
		public List<ContentCode> code { get; set; }

		public Content()
        {
            title = new ContentTitle();
            paragraphs = new List<string>();
            images = new List<ContentImage>();
            links = new List<ContentLink>();
            lists = new List<ContentList>();
			quotes = new List<ContentQuotes>();
			code = new List<ContentCode>();
        }

        public override string ToString()
        {
            string titleText = String.Format("{0}", title.ToString());
            string paragraphText = "";
            foreach(string para in paragraphs)
            {
                paragraphText += String.Format("{0}\n", para);
            }
            return string.Format("{0}\n{1}\n{2}", titleText, paragraphText, links.Count);
        }

        public static implicit operator List<object>(Content v)
        {
            throw new NotImplementedException();
        }
    }
}
