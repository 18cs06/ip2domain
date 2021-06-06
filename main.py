#! /usr/bin/python
#coding:utf8
import re, time, requests
import sys
from os import path
from fake_useragent import UserAgent
from optparse import OptionParser
start = time.time()



ua = UserAgent()

def banner():
    print("""
    \033[1;36m    __                                                                \033[0m
    \033[1;36m   [   ]              ____                                  ___       \033[0m
    \033[1;36m    | |              / ___|                                [   ]      \033[0m
    \033[1;36m    | |  --.--.-.   | |                       .--.          | |       \033[0m
    \033[1;36m    | |  |  .--.|   | |      _____    _____   |  |----      | |       \033[0m 
    \033[1;36m    | |  |  |.-||    \ \__  /     \  /     \  |   ___.|     | |____   \033[0m
    \033[1;36m   [__ ] |  .---/     \__ | |_____/  |      | |  /     ____ | ___  |  \033[0m
    \033[1;36m         | |            | | |        |      | |  |    //    | |  | |          bete 0.1 \033[0m
    \033[1;36m         | |         ___/ /  \____   \_____/| |  |    ||    | |  | |  ----by kevu,Constantine   \033[0m    
    \033[1;36m        [___]       |____/                    .--.    \\___ [__]  [_]       """)
    print("\n")
    print('\033[1;36m   使用方法\033[0m')
    print("\n")
    print('\033[1;36m   python3 main.py -f xx.txt\033[0m')
    print("\n")
    print("\n")
if len(sys.argv) == 1:
    banner()
    sys.exit()

# ip138
headers_ip138 = {
    'Host': 'site.ip138.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://site.ip138.com/'}


def ip138_spider(ip):
    ip138_url = 'https://site.ip138.com/' + str(ip) + '/'
    ip138_r = requests.get(url=ip138_url, headers=headers_ip138, timeout=3).text
    ip138_address = re.findall(r"<h3>(.*?)</h3>", ip138_r)   # 归属地
    # result = re.findall(r"<li>(.*?)</li>", ip138_r)
    if '<li>暂无结果</li>' in ip138_r:
        print('[+]ip:{}'.format(ip))
        print('归属地：{}'.format(ip138_address[0]))
        print('未查到相关绑定信息！')
    else:
        print('[+]ip:{}'.format(ip))
        print('归属地：{}'.format(ip138_address[0]))
        result_time = re.findall(r"""class="date">(.*?)</span>""", ip138_r)  # 绑定时间
        result_site = re.findall(r"""</span><a href="/(.*?)/" target="_blank">""", ip138_r)  # 绑定域名结果
        print('绑定信息如下：')
        for i, j in enumerate(result_time):
            # print('{}-----{}'.format(j, result_site[i]))
            cv = str(ip) + '\t' + str(j) + '\t' + str(result_site[i])
            print(cv)
            with open('查询结果.txt', 'a') as k:  #将结果保存到查询结果.txt
                k.write(cv + '\n')

        # print(result_site[0])
    print('-'*25)

def main():
    usage = "Usage: %prgo -f <filename>"        #配置选项功能
    parser = OptionParser(usage=usage)
    parser.add_option("-f",'--file',type='string',dest='filename')
    (options,args)=parser.parse_args()

    filename = options.filename

    if (filename==None):             #判断是否传入参数
        print("please enter an Ip address file")
        sys.exit()

    if filename:
        if not path.exists(filename):
            print("the file is not exist")
            sys.exit()
        else:
            f = open(filename,'r+')         #在此处修改扫描的ip文件
            for i in f.readlines():
                r = i.strip('\n')
                we = re.findall(r'\d+.\d+.\d+.\d+', r)
                for ip in we:
                    try:
                        ip138_spider(ip)
                    except Exception as error:
                        print(error)
                    else:
                        pass
            f.close()

if __name__=='__main__':
    main()
    end = time.time()
    print("检索完毕")
    print("运行时间:{}秒".format(end - start))