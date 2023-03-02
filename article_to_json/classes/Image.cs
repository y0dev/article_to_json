using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace article_to_json.classes
{
    class Image
    {
        /*
         * "image": 
        {
            "name": "images/web-dev.png",
            "alt": "web-dev-img"
        },
         */
        public string name { get; set; }
        public string alt { get; set; }

        public Image()
        {
            name = "";
            alt = "";
        }
    }
}
