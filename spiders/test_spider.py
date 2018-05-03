

from functings.spider_function import *


for i in range(1,2):
    url = 'http://huodong.ctrip.com/Activity-Booking-OnlineWebSite/Recommend/UserComments?id=2071349&productName=fdfd&pageSize=5&pageIndex='

L = parser_comment_url(url)
print(L)


