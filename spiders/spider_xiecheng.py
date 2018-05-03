
'''
此模块用于爬取携程旅游的玩乐搜索关键字后的全部信息
'''
import pymysql

from functings.spider_function import *



def main(keyword):
    '''此函数为spider_xiecheng的主功能函数'''
    url = 'http://huodong.ctrip.com/activity/search/?keyword=%s'%keyword
    html = gethtml(url)
    result = htmlparser(html)
    L = parser_xc_index(result)
    select = result.xpath('//a[@class="select"]/text()')[0]
    select = re.sub('[^\d+]','',select)
    max_page = int(select) // 10 + 1
    for i in range(2,max_page+1):
        print('正在爬取%s关键词的第%s页'%(keyword,i))
        url = 'http://huodong.ctrip.com/activity/search/?keyword=%s&filters=p%s'%(keyword,i)
        html = gethtml(url)
        result = htmlparser(html)
        L1 = parser_xc_index(result)
        L += L1
    return L

if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1',port=3306,user\
    ='root',passwd='123456',db='xiecheng',use_unicode=True,\
                           charset='utf8')
    cur = conn.cursor()
    keyword = input('输入关键字爬取信息')
    L = main(keyword)
    for i in L:
        title, point_num, comment_url, price, \
        product_comment, product_num = i['title'], \
        i['point_num'], i['comment_url'], i['price'], \
        i['product_comment'], i['product_num']

        sql = 'INSERT INTO xc_index VALUES (NULL ,"%s",\
"%s","%s","%s","%s","%s")'%(title,point_num,comment_url\
,price,product_comment,product_num)
        print(sql)
        cur.execute(sql)

        with open('../result/%s_xc_index.csv'%keyword,'a',encoding='utf8') as f:
            f.writelines(title+'^'+point_num+'^'+comment_url+'^'+\
            price+'^'+product_comment+'^'+product_num+'\n')

    conn.commit()
    cur.close()
    conn.close()


