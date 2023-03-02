using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace article_to_json.classes
{
    /*
     * 
     * "title": "Help with System Design Interviews",
        "description": "System design study focuses on understanding user requirements, creating system architecture and developing a plan for implementation.",
        "date": "1675836000000",
        "id":  "system-design",
        "tags": 
        [
            "System Design", "Technology", "MAANG"
        ],
     */
    class Article
    {
        public string title { get; set; }
        public string description { get; set; }
        public string date { get; set; }
        public string id { get; set; }
        public List<string> tags { get; set; }
        public Image image { get; set; }
        public List<Content> content { get; set; }

        public Article()
        {
            title = "";
            description = "";
            date = "";
            id = "";
            tags = new List<string>();
            image = new Image();
            content = new List<Content>();
        }
    }
}
