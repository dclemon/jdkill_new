# -*- coding:utf-8 -*-
import requests
import jd_config
import time
import sys
import threading

'''
待添加的功能：
1. 


'''


class Jd_goods(object):
    def __init__(self):
        self.jdtimenow = ''
        self.targettime = ''
        self.venderId = ''
        self.difftime = ''
        self.needinvoice = ''
        self.seckill_time_str = jd_config.read_ini('config', 'seckill_time', 'config.ini')
        self.yuyue_time = jd_config.read_ini('config', 'yuyue_time', 'config.ini')
        self.sku = jd_config.read_ini('config', 'sku_id', 'config.ini')


class Jd_account(object):
    def __init__(self):
        self.islogin = False
        self.cookie = {}
        self.pushplustoken = jd_config.read_ini('config', 'pushplus_token', 'config.ini')
        self.cokstr = jd_config.read_ini('config', 'cookies_String', 'config.ini')
        self.pwd = jd_config.read_ini('config', 'pwd', 'config.ini')
        self.eid = jd_config.read_ini('config', 'eid', 'config.ini')
        self.fp = jd_config.read_ini('config', 'fp', 'config.ini')
        self.key = jd_config.read_ini('config', 'key', 'config.ini')

    @staticmethod
    def login(cokstr):
        d, cookie = jd_config.jd_checklogin(cokstr)
        account.cookie = cookie
        return d

    @staticmethod
    def gettime():
        # 获取京东时间，延迟以及抢购时间
        jdtime, difftime = jd_config.gettime()
        return jdtime, difftime

    @staticmethod
    def yuyue(sku, key, cookie):
        url = 'https://yushou.jd.com/toYuyue.action?sku=' + sku + '&key=' + key
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'sec-fetch-user': '?1',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'referer': 'https://item.jd.com/'
        }
        requests.get(url, headers=head, cookies=cookie)
        url = 'https://yushou.jd.com/member/qualificationList.action'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': 'https://item.jd.com/',
            'Host': 'yushou.jd.com'
        }
        res = requests.get(url, headers=head, cookies=cookie)
        if goods.sku in res.text:
            print('预约成功！')
        else:
            print('预约失败。')
        return

    @staticmethod
    def jiagou(cookie, sku):
        url = 'https://cart.jd.com/gate.action?pcount=1&ptype=1&pid=' + sku
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': 'https://item.jd.com/'
        }
        res = requests.get(url, headers=head, cookies=cookie)
        a = '商品已成功加入购物车'
        if a in res.text:
            print('加入购物车成功！')
            return True
        else:
            print('加入购物车失败，请检查原因')
            return False

    @staticmethod
    def gouxuan(cookie, rm, wb, sku_id, jd_req, ref, refer):
        # 这一步是在订单页面勾选需要结算的商品，打勾后服务器会置cookie，拿着这个cookie进行下一步。
        # session会自动传递cookie
        # 获取店铺id
        url = f'https://item.jd.com/{sku_id}.html'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': 'https://order.jd.com/'
        }
        res = jd_req.get(url=url, headers=head, cookies=cookie)
        goods.venderId = jd_config.getmidstring(res.text, 'venderId:', ',')
        pin = cookie['pin']
        uid = cookie['__jdu']
        sid = cookie['__jdu']
        jdv = cookie['__jdu']
        url = f'https://mercury.jd.com/log.gif?t=other.000000&m=UA-J2011-1&pin={pin}&uid={uid}&sid={sid}|1&v=je%3D0' \
              f'%24sc%3D24-bit%24sr%3D1920x1080%24ul%3Dzh-cn%24cs%3DUTF-8%24dt%3D%E4%BA%AC%E4%B8%9C%E5%95%86%E5%9F%8E' \
              f'%20-%20%E8%B4%AD%E7%89%A9%E8%BD%A6%24hn%3Dcart.jd.com%24fl%3D-%24os%3Dwin%24br%3Dchrome%24bv%3D91.0' \
              f'.4472.101%24wb%3D{wb}%24xb%3D{wb}%24yb%3D' \
              f'{wb}%24zb%3D1%24cb%3D23%24usc%3Ddirect%24ucp%3D-%24umd%3Dnone%24uct%3D-%24ct%3D' \
              f'{rm}%24lt%3D0%24tad%3D-%24t1%3DShopcart_CheckProd%24t2%3D0_{sku_id}%24p0%3DQ%24cb%3D23%24pinid%3D' \
              f'{pin}%24jdv%3D{jdv}%24dataver%3D0.1&ref={ref}&rm={rm} '
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': refer
        }
        jd_req.get(url=url, headers=head, cookies=cookie)
        return

    @staticmethod
    def getorderinfo(jd_req):
        # 用之前获取的cookie访问这个地址，会得到商品名称和收货地址等信息。
        url = 'https://trade.jd.com/shopping/order/getOrderInfo.action'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': 'https://cart.jd.com/cart_index/'
        }
        a = jd_req.get(url=url, headers=head)
        b = jd_config.getmidstring(a.text, 'sopNotPutInvoice" value="', '"')
        return b

    @staticmethod
    def submitorder(jd_req):
        """
        提交订单，默认使用红包和优惠券，所以需要支付密码。
        pwd:支付密码
        venderid:店铺号
        eid:每个账号不同
        fp:每个账号不同
        """
        print('执行提交订单！')
        url = 'https://trade.jd.com/shopping/order/submitOrder.action?&presaleStockSign=1'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.142 Safari/537.36',
            'referer': 'https://trade.jd.com/shopping/order/getOrderInfo.action',
            'origin': 'https://trade.jd.com',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        j = ''
        for i in account.pwd:
            i = 'u3' + i
            j = j + i
        account.pwd = j
        dt2 = f'overseaPurchaseCookies=&submitOrderParam.payPassword={account.pwd}&vendorRemarks=[]&submitOrderParam.sopNotPutInvoice={goods.needinvoice}&submitOrderParam.trackID=TestTrackId&presaleStockSign=1&submitOrderParam.ignorePriceChange=0&submitOrderParam.btSupport=0&submitOrderParam.eid={account.eid}&submitOrderParam.fp={account.fp}&submitOrderParam.jxj=1 '
        data_js = jd_config.key_value_to_json(dt2)
        res = jd_req.post(url=url, headers=head, data=data_js)
        false = False
        true = True
        null = None
        a = eval(res.text)
        if a['success']:
            print('下单成功！')
            pushplus_send('抢购到订单啦！', res.text, account.pushplustoken)
        else:
            print('下单失败！')
            pushplus_send('没有抢到！', res.text, account.pushplustoken)
        return


def pushplus_send(title, message, token):
    requests.get(f'http://pushplus.hxtrip.com/send?token={token}&title={title}&content={message}&template=html')
    return


def step1():
    while True:

        account.islogin = account.login(account.cokstr)
        if not account.islogin:
            pushplus_send('京东抢购登录状态已经过期！', '123', account.pushplustoken)
        time.sleep(1800)
        return


def step2():
    while True:
        timeArray = time.strptime(str(goods.seckill_time_str), "%Y-%m-%d %H:%M:%S")
        goods.seckill_time = int(time.mktime(timeArray))
        print('秒杀时间：' + str(goods.seckill_time * 1000))
        goods.jdtimenow, goods.difftime = account.gettime()
        goods.targettime = int(goods.seckill_time) * 1000 - int(goods.difftime)
        print('京东时间：' + str(goods.jdtimenow))
        print('目标时间：' + str(goods.targettime))
        time.sleep(300)


account = Jd_account()
goods = Jd_goods()
jdreq = requests.session()
threads = []


def main():
    """
        预约，加购物车，抢购一条龙
        流程：
        1. 每隔30分钟检查一次登录状态，京东网页版的ck基本是24小时过期一次，失效后给pushplus发送通知;抢购前检查一次与京东的时间差
        2. 在登录状态下，立即执行一次预约操作，预约成功向pushplus发送一次通知，失败发送原因（预约成功后，商品会出现在购物车里）
        3. 获取所预约商品的抢购时间戳
        4. 获取与京东服务器的时间差
        5. 本地时间戳+网络延迟 = 抢购时间戳 时，发起一次勾选操作，然后提交订单
        这个脚本流程执行一次就停止
    """
    print(""" ▓█████▄  ▄████▄   ██▓    ▓█████  ███▄ ▄███▓ ▒█████   ███▄    █ 
▒██▀ ██▌▒██▀ ▀█  ▓██▒    ▓█   ▀ ▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ 
░██   █▌▒▓█    ▄ ▒██░    ▒███   ▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒
░▓█▄   ▌▒▓▓▄ ▄██▒▒██░    ▒▓█  ▄ ▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒
░▒████▓ ▒ ▓███▀ ░░██████▒░▒████▒▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░
 ▒▒▓  ▒ ░ ░▒ ▒  ░░ ▒░▓  ░░░ ▒░ ░░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
 ░ ▒  ▒   ░  ▒   ░ ░ ▒  ░ ░ ░  ░░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
 ░ ░  ░ ░          ░ ░      ░   ░      ░   ░ ░ ░ ▒     ░   ░ ░ 
   ░    ░ ░          ░  ░   ░  ░       ░       ░ ░           ░ 
 ░      ░                                                      """)

    threads.append(threading.Thread(target=step1))
    threads.append(threading.Thread(target=step2))
    for t in threads:
        t.start()
    account.islogin = account.login(account.cokstr)
    if not account.islogin:
        return
    else:
        timeArray = time.strptime(str(goods.yuyue_time), "%Y-%m-%d %H:%M:%S")
        goods.yuyue_time = int(time.mktime(timeArray)) * 1000
        c = goods.yuyue_time
        while True:
            a = int(time.time() * 1000)
            if a >= int(c):
                print('开始预约')
                account.yuyue(goods.sku, account.key, account.cookie)
                for k, v in account.cookie.items():
                    jdreq.cookies.set(k, v)
                goods.jdtimenow, goods.difftime = account.gettime()
                account.jiagou(account.cookie, goods.sku)
                b = goods.targettime
                while True:
                    a = int(time.time() * 1000)
                    if a >= int(b):
                        print('开始抢购！')
                        account.gouxuan(account.cookie, goods.jdtimenow, str(int(int(goods.jdtimenow) / 1000)),
                                        goods.sku,
                                        jdreq, '', 'https://cart.jd.com/')
                        goods.needinvoice = account.getorderinfo(jdreq)
                        account.submitorder(jdreq)
                        sys.exit()
                    else:
                        time.sleep(0.02)
            else:
                print('未到预约时间，等待60s')
                time.sleep(60)

if __name__ == '__main__':
    main()
