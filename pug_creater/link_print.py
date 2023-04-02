# import datetime
# import time
 
# # ts stores the time in seconds
# ts = time.time()
 
# # print the current timestamp
# print(ts * 1000.0)

# # get the current date and time
# now = datetime.datetime.now()
# # py_timestamp = int(self.post_info['date'])/1000.0

# print(now)

# Javascript new Date().getTime()
"""
var today = new Date();
const dd = String(today.getDate()).padStart(2, '0');
const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
const yyyy = today.getFullYear();

today = mm + '/' + dd + '/' + yyyy;
const date = new Date(today).getTime();
"""

strs = ''
for i in range(1,14):
    strs += ':linkPlace(0{:02d}),'.format(i)
print(strs)