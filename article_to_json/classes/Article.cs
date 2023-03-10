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

		public void generateImage(string docType)
		{
			
			switch ( docType.ToLower() )
			{
				case "theology":
				case "covenant":
					{
						image.alt = "bible-icon";
						image.name = "images/bible-icon.png";
						break;
					}
				case "thankful":
					{
						image.alt = "thankful-icon";
						image.name = "images/thankful.png";
						break;
					}
				case "family":
					{
						image.alt = "family-image";
						image.name = "images/family.png";
						break;
					}
				case "health":
					{
						image.alt = "health-img";
						image.name = "images/heart_strength.png";
						break;
					}
				case "code":
				case "tech":
				case "technology":
				case "system design":
					{
						image.alt = "web-dev-img";
						image.name = "images/web-dev.png";
						break;
					}
				case "docker":
					{
						image.alt = "docker-image";
						image.name = "images/docker.png";
						break;
					}
				case "jenkins":
					{
						image.alt = "jenkins-image";
						image.name = "images/jenkins.png";
						break;
					}
				default:
					{
						image.alt = "image-title";
						image.name = "images/image.png";
						break;
					}
			}
		}
    }
}
