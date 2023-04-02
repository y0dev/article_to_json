using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace article_to_json.classes
{
	class TimeToRead
	{
		public string secs { get; set; }
		public string mins { get; set; }
		public string hours { get; set; }

		public TimeToRead(int wordCount)
		{
			calculateTimeToRead(wordCount);
		}

		private void convertToPreferredFormat( decimal seconds )
		{
			decimal sec = seconds % (24 * 3600);
			decimal decHour = Math.Floor( sec / 3600 );
			sec %= 3600;
			decimal decMin = Math.Floor( sec / 60 );
			sec %= 60;
			// Console.WriteLine(seconds);
			secs = String.Format("{0}", (int) sec);
			mins = String.Format("{0}", (int) decMin);
			hours = String.Format("{0}", (int) decHour);
		}

		private void calculateTimeToRead(int wordCount)
		{
			const decimal WORDS_PER_MINUTE = 250;
			const int MINUTE = 60;
			const int HOUR = 60 * MINUTE; // 3600 seconds
			decimal timeToReadMins = ( (decimal) wordCount / WORDS_PER_MINUTE) * 60;

			// Console.WriteLine("{0} Word COunt: {1}", timeToReadMins, wordCount);
			convertToPreferredFormat(timeToReadMins);
			/*
			if (timeToReadMins >= 0 && timeToReadMins < 1 * MINUTE)
			{
				mins = "< 1";
			}
			else if (timeToReadMins >= 1 * MINUTE && timeToReadMins < 2 * MINUTE)
			{
				mins = "1";
			}
			else if (timeToReadMins >= 2 * MINUTE && timeToReadMins < 3 * MINUTE)
			{
				mins = "2";
			}
			else if (timeToReadMins >= 3 * MINUTE && timeToReadMins < 4 * MINUTE)
			{
				mins = "3";
			}
			else if (timeToReadMins >= 4 * MINUTE && timeToReadMins < 5 * MINUTE)
			{
				mins = "4";
			}
			else if (timeToReadMins >= 5 * MINUTE && timeToReadMins < 6 * MINUTE)
			{
				mins = "5";
			}
			else if (timeToReadMins >= 6 * MINUTE && timeToReadMins < 7 * MINUTE)
			{
				mins = "6";
			}
			else if (timeToReadMins >= 7 * MINUTE && timeToReadMins < 8 * MINUTE)
			{
				mins = "7";
			}
			else if (timeToReadMins >= 8 * MINUTE && timeToReadMins < 9 * MINUTE)
			{
				mins = "8";
			}
			else if (timeToReadMins >= 9 * MINUTE && timeToReadMins < 10 * MINUTE)
			{
				mins = "9";
			}
			else if (timeToReadMins >= 10 * MINUTE && timeToReadMins < 11 * MINUTE)
			{
				mins = "10";
			}
			else if (timeToReadMins >= 11 * MINUTE && timeToReadMins < 12 * MINUTE)
			{
				mins = "11";
			}
			else if (timeToReadMins >= 12 * MINUTE && timeToReadMins < 13 * MINUTE)
			{
				mins = "12";
			}
			else if (timeToReadMins >= 13 * MINUTE && timeToReadMins < 14 * MINUTE)
			{
				mins = "13";
			}
			else if (timeToReadMins >= 14 * MINUTE && timeToReadMins < 11 * MINUTE)
			{
				mins = "14";
			}
			else if (timeToReadMins >= 15 * MINUTE && timeToReadMins < 12 * MINUTE)
			{
				mins = "15";
			}
			else if (timeToReadMins >= 16 * MINUTE && timeToReadMins < 13 * MINUTE)
			{
				mins = "16";
			}
			else if (timeToReadMins >= 17 * MINUTE && timeToReadMins < 14 * MINUTE)
			{
				mins = "17";
			}

			if (timeToReadMins > HOUR )
			{
				hours = "1";
			}
			*/
		}
	}
}
