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
    }

    class ContentImage
    {
        public string id { get; set; }
        public string alt { get; set; }
        public string caption { get; set; }
        public string link { get; set; }
    }

    class ContentLink
    {
        public string id { get; set; }
        public string text { get; set; }
        public string link { get; set; }
    }

    class ContentList
    {
        public string id { get; set; }
        public List<string> items { get; set; }
        public string listType { get; set; }
    }

    class Content
    {
        public ContentTitle title { get; set; }
        public List<string> paragraghs { get; set; }
        public List<ContentImage> images { get; set; }
        public List<ContentLink> links { get; set; }
        public List<ContentList> lists { get; set; }
    }
}
