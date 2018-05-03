import pymysql

from functings.spider_function import *


def main(url):
    html = gethtml(url)
    comment_id = re.findall('/(\d+)\.html',url)[0]
    result = htmlparser(html)
    title = result.xpath('//h1/text()')[0].strip()
    all_comment = result.xpath('//a[@data-anchor="yhdp"]/text()')[0].strip()
    max_page = re.sub('[^\d+]','',all_comment)
    if not max_page:
        max_page = 0
    max_page = int(max_page)//5+1
    L = []
    for i in range(1,max_page+1):
        print('正在爬取第%s页'%i)
        url = 'http://huodong.ctrip.com/Activity-Booking-OnlineWebSite/Recommend/UserComments?id=%s&productName=%s&pageSize=5&pageIndex=%s'%(comment_id,title,i)
        html = gethtml(url)
        result = htmlparser(html)
        L += parser_xc_comment(result)
    return L


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='123456',charset='utf8',db='xiecheng',use_unicode=True)
    cur = conn.cursor()
    sql = 'SELECT comment_url,id,title FROM xc_index'
    cur.execute(sql)
    t = cur.fetchall()
    for i in t:
        url = 'http://huodong.ctrip.com' + i[0]
        id = i[1]
        title = i[2]
        try:
            L = main(url)
        except Exception as e:
            pass
        for i in L:
            user, comment, point, img = i['user'],i['comment'],i['point'],i['img']
            sql = 'INSERT INTO xc_comment VALUES (null,"%s","%s","%s","%s","%s")'%(user,comment,point,img,id)
            cur.execute(sql)
            try:
                with open('../result/%s.csv'%title,'a',encoding='utf8') as f:
                    f.writelines(user+'^'+comment+'^'+point+'^'+img+'\n')
            except Exception as e:
                pass


    conn.commit()
    cur.close()
    conn.close()







