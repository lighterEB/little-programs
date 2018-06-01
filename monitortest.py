# coding: utf-8
import requests, time, sys, os, lxml, re, socket
import logging
from bs4 import BeautifulSoup


# 端口连通性测试
def check_server(address, p,dic,i):
    s = socket.socket()
    try:
        s.connect((address, p))
        print('可以连通,端口正常')
    except socket.error as e:
        print('连接失败,端口异常')
        logging.basicConfig(filename='errors.log', format='%(asctime)s - %(message)s')
        logging.warning(dic['分类'] + '，' + dic['区组'] + '，' + dic['应用名'] + '，' + dic['IP'] + ' 端口：' + i
                        + ' 连接超时，端口异常！\n'
                        )


#ping测试
def ping_check(dic):
    cmd = 'ping' + ' ' + dic['IP']
    res = os.popen(cmd)
    for i in res:
        print(i)
        if '数据包: 已发送 = 4，已接收 = 0，丢失 = 4 (100% 丢失)' in i:
            logging.basicConfig(filename='errors.log', format='%(asctime)s - %(message)s')
            logging.warning(dic['分类'] + '，' + dic['区组'] + '，' + dic['应用名'] + dic['IP'] + ' 请求超时！\n')


# 获取即时报警信息并测试
def get_info():
    cookies = {}
    url = ''
    source = requests.get(url, cookies=cookies)
    res = source.content.decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')
    info1 = soup.find_all(class_='e_sign')
    info2 = soup.find_all(class_='w_sign')
    info3 = soup.find_all(class_='info_sign')
    for info in info1:
        dic1 = {}
        dic1["时间"] = info.find_all('td')[1].text.strip()
        dic1["分类"] = info.find_all('td')[2].text.strip()
        dic1["区组"] = info.find_all('td')[3].text.strip()
        dic1["应用名"] = info.find_all('td')[4].text.strip()
        dic1["IP"] = info.find_all('td')[5].text.strip()
        dic1["Source_ip"] = info.find_all('td')[6].text.strip()
        dic1["错误说明"] = info.find_all('td')[7].text.strip()
        dic1["info"] = info.find_all('td')[8].text.strip()
        # print(dic1)
        if dic1["错误说明"] == '超时':
            print('发现超时报警：%s %s %s %s %s' % (dic1["时间"], dic1["分类"], dic1["区组"], dic1["应用名"], dic1['IP']))
            ping_check(dic1)
        elif dic1["错误说明"] == '端口':
            print('发现端口报警：%s %s %s %s %s %s' % (dic1["时间"], dic1["分类"], dic1["区组"], dic1["应用名"],
                                                        dic1['IP'],dic1['info'])
                    )
            port = re.findall('\d{1,5}.*', dic1['info'])
            port = ''.join(port).rstrip(',')
            d = port.split(',')
            print('IP为：%s ，端口为： %s' % (dic1['IP'], port))
            for i in d:
                print('Telnet %s %s' % (dic1['IP'], i))
                check_server(dic1['IP'], int(i), dic1, i)
            print('\n')
        else:
            pass

    for info in info2:
        dic2 = {}
        dic2["时间"] = info.find_all('td')[1].text.strip()
        dic2["分类"] = info.find_all('td')[2].text.strip()
        dic2["区组"] = info.find_all('td')[3].text.strip()
        dic2["应用名"] = info.find_all('td')[4].text.strip()
        dic2["IP"] = info.find_all('td')[5].text.strip()
        dic2["Source_ip"] = info.find_all('td')[6].text.strip()
        dic2["错误说明"] = info.find_all('td')[7].text.strip()
        dic2["info"] = info.find_all('td')[8].text.strip()
        if dic2["错误说明"] == '超时':
            print('发现超时报警：%s %s %s %s %s' % (dic2["时间"], dic2["分类"], dic2["区组"], dic2["应用名"], dic2['IP']))
            ping_check(dic2)
        elif dic2["错误说明"] == '端口':
            print('发现端口报警：%s %s %s %s %s %s' % (dic2["时间"], dic2["分类"], dic2["区组"], dic2["应用名"], dic2['IP'],
                                                dic2['info'])
                  )
            port = re.findall('\d{1,5}.*', dic2['info'])
            port = ''.join(port).rstrip(',')
            d = port.split(',')
            print('IP为：%s ，端口为： %s' % (dic2['IP'], port))
            for i in d:
                print('Telnet %s %s' % (dic2['IP'], i), dic2)
                check_server(dic2['IP'], int(i), dic2, i)
            print('\n')
        else:
            pass

    for info in info3:
        dic3 = {}
        dic3["时间"] = info.find_all('td')[1].text.strip()
        dic3["分类"] = info.find_all('td')[2].text.strip()
        dic3["区组"] = info.find_all('td')[3].text.strip()
        dic3["应用名"] = info.find_all('td')[4].text.strip()
        dic3["IP"] = info.find_all('td')[5].text.strip()
        dic3["Source_ip"] = info.find_all('td')[6].text.strip()
        dic3["错误说明"] = info.find_all('td')[7].text.strip()
        dic3["info"] = info.find_all('td')[8].text.strip()
        if dic3["错误说明"] == '超时':
            print('发现超时报警：%s %s %s %s %s' % (dic3["时间"], dic3["分类"], dic3["区组"], dic3["应用名"], dic3['IP']))
            ping_check(dic3)
        elif dic3["错误说明"] == '端口':
            print('发现端口报警：%s %s %s %s %s %s' % (dic3["时间"], dic3["分类"], dic3["区组"], dic3["应用名"], dic3['IP'],
                                                dic3['info'])
          )
            port = re.findall('\d{1,5}.*', dic3['info'])
            port = ''.join(port).rstrip(',')
            d = port.split(',')
            print('IP为：%s ，端口为： %s' % (dic3['IP'], port))
            for i in d:
                print('Telnet %s %s' % (dic3['IP'], i))
                check_server(dic3['IP'], int(i), dic3, i)
            print('\n')
        else:
            pass

if __name__ == '__main__':
    os.system('title 连通性测试工具，有问题联系：胡尚鹏程')
    os.system('CLS')
    while True:
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            print('若监测到超时或端口报警会自动测试并记录，无需操作！')
            print('所有的错误记录将记录在%s\n' % os.path.abspath('errors.log'))
            get_info()
            for i in range(60):
                sys.stdout.write('\r监控将在{}s后刷新'.format(60 - i))
                sys.stdout.flush()
                time.sleep(1)
            os.system('CLS')
            continue
        except KeyboardInterrupt:
            break
        except:
            logging.basicConfig(filename='errors.log', format='%(asctime)s - %(message)s')
            logging.warning('程序异常终止。')