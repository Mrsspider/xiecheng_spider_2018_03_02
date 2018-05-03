import re
import requests
from lxml import etree

from random import choice
import random
from time import sleep

from settings.spider_setting import *

x = random.randint(1,3)
# 提取html页面
def gethtml(url,myip=choice(getip())):
    '''输入url,输出字符串respons.text'''
    try:
        respons = requests.get(url,myip,headers=headers)
        respons.encoding
        # sleep(x)
        return respons.text
    except Exception as e:
        logbook = {'errorFunc':'gethtml','errorType':e,'errorUrl':url,'errorHeaders':headers}
        mywrith('../logbook/logbook.txt', str(logbook) + '\n')
        return None

# 使用xpath解析网页
def htmlparser(html):
    try:
        html = etree.HTML(html,parser=etree.HTMLParser())
        return html
    except Exception as e:
        logbook = {'errorFunc':'htmlparser','htmlparser':e}
        mywrith('../logbook/logbook.txt', str(logbook) + '\n')


def not_none(L):
    '''此函数用于保证列表不为空,无点评的人为生成0条点评'''
    if L:
        return L
    else:
        return ['0']

def parser_xc_index(result):
    '''此函数用于解析携程玩乐主界面'''
    L = []
    xy_list = result.xpath('//div[@id="xy_list"]/div')
    for xy in xy_list:
        d = {}
        title = xy.xpath('.//h2/text()')[0].strip()
        title = re.sub('"','\'',title)
        point_num = not_none(xy.xpath('.//em[@class="green"]/text()'))[0]
        comment_url = xy.xpath('./a/@href')[0]
        price = xy.xpath('.//span[@class="base_price"]/strong/text()')[0]
        if not price:
            price = '0'
        product_comment = not_none(xy.xpath('.//span[@class="product_comment"]/text()'))[0]
        product_comment = re.sub('[^\d+]', '', product_comment)
        if not product_comment:
            product_comment = '0'
        product_num = not_none(xy.xpath('.//span[@class="product_num"]/em/text()'))[0]
        product_num = re.sub('[^\d+]', '', product_num)
        d['title'], d['point_num'], d['comment_url'], d['price'], \
        d['product_comment'], d['product_num'] = title, point_num, \
                                                 comment_url, price, product_comment, product_num
        L.append(d)
    return L

def parser_xc_comment(result):
    '''此函数用于解析协程旅游产品详情页面,传入url,返回所有用户评论的字典列表'''
    L = []
    result_list = result.xpath('//li[@class="basefix"]')
    for result in result_list:
        user = result.xpath('.//div[@class="ticket_user_pro basefix"]/span[1]/text()')
        comment = result.xpath('.//div[@class="ticket_user_left"]/text()')
        comment_list = []
        for i in comment:
            i = i.strip()
            if i:
                comment_list.append(i)
        comment = comment_list
        point = result.xpath('.//h4/span/@class')
        point_list = []
        for i in point:
            i = re.sub('[^\d+]','',i)
            point_list.append(i)
        point = point_list
        img = result.xpath('.//img/@src')
        if not img:
            img = ['未上传图片']
        else:
            s = ""
            for i in img:
                s+=','+i
            img = [s[1:]]
        user,comment,point,img=user[0],comment[0],point[0],img[0]
        d={'user':user,'comment':comment,'point':point,'img':img}
        L.append(d)
    return L



# 存档
def mywrith(filename,result):
    try:
        with open(filename,'a',encoding='utf8') as f:
            f.writelines(result)
    except Exception as e:
        logbook = {'errorFunc':'mywrith','mywrith':e}
        with open('../logbook/logbook.txt','a',encoding='utf8') as f:
            f.writelines((str(logbook)+'\n'))

# 该函数测试ip是否可用，可用的ip作为列表输出
def test_ip(iplist):
    '''没有参数，输出可用[ip:port,...]列表'''
    prolist = []
    try:
        for ip in iplist:
            url = 'https://www.baidu.com/'
            pro = {'http':ip}
            head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
            test_num = requests.get(url,proxies=pro,headers=head).status_code
            if test_num == 200:
                prolist.append(ip+',')
            with open('../settings/proxy.txt','a',encoding='utf8') as f:
                f.writelines(prolist)
    except Exception as e:
        e = {'test_ip':e}
        with open('../logbook/logbook.txt','a',encoding='utf-8') as f:
            f.writelines(str(e))


# 该函数爬取速度小于3s的ip并写入proxy.text
def get_ip(num):
    '''输入爬取页数，把ip以逗号间隔写入proxy.txt首行'''
    url = 'https://www.kuaidaili.com/free/inha/'
    try:
        iplist = []
        for i in range(1,num):
            url = url + str(i)
            respons = requests.get(url).text
            pat = '<td data-title="IP">(.*?)</td>\s+<.*?>(\d+)</td>\s+<.*?>高匿名</td>\s+<.*?>.*?</td>\s+<.*?>.*?<.*?>\s+<.*?>(.*?)秒<'
            pattern = re.compile(pat)
            prolist = re.findall(pattern,respons)
            for pro in prolist:
                print(pro)
                if float(pro[2]) < 3:
                    pro = pro[0]+':'+pro[1]
                    iplist.append(pro)
        print('正在测试爬取到的ip',iplist)
        test_ip(iplist)
    except Exception as e:
        e = {'getip':e}
        with open('../logbook/logbook.txt','a',encoding='utf-8') as f:
            f.writelines(str(e))

def write_log(d):
    with open('../logbook/logbook.txt', 'a', encoding='utf-8') as f:
        f.writelines(str(d))


if __name__ == '__main__':
    get_ip(20)

