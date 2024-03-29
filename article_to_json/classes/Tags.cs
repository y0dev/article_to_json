﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace article_to_json.classes
{
	class Tags
	{
		private List<string> tagList = new List<string>();
		private string docType;
		public Tags(string docType)
		{
			this.docType = docType;
			generateTagList();
		}

		public List<string> getTagList()
		{
			return tagList;
		}

		private void generateTagList()
		{
			switch ( this.docType.ToLower() )
			{
				case "theology":
					{
						tagList.Add("Theology");
						tagList.Add("God");
						tagList.Add("Gospel");
						tagList.Add("Reformed");
						break;
					}
				case "covenant":
					{
						tagList.Add("Christ");
						tagList.Add("Covenant");
						tagList.Add("Reformed");
						tagList.Add("Gospel");
						break;
					}
				case "thankful":
					{
						tagList.Add("Christ");
						tagList.Add("Salvation");
						tagList.Add("Love");
						tagList.Add("Thankful");
						break;
					}
				case "health":
					{
						tagList.Add("Health");
						tagList.Add("Fitness");
						break;
					}
				case "tech":
				case "technology":
					{
						tagList.Add("Technology");
						tagList.Add("Engineer");
						break;
					}
				case "algo":
				case "algorithm":
					{
						tagList.Add("Data Structures");
						tagList.Add("Algorithms");
						tagList.Add("Tech Interview");
						break;
					}
				case "system design":
					{
						tagList.Add("System Design");
						tagList.Add("Technology");
						tagList.Add("Tech Interview");
						break;
					}
				default:
					{
						tagList.Add("Template");
						tagList.Add("Info");
						tagList.Add("Beginner");
						break;
					}
			}
		}
	}
}
