#_*_coding:utf-8_*_
import requests
import platform
import os,sys
import getopt
import socket
import zlib
import json
import webbrowser

cmdlist = sys.argv

if len(cmdlist) == 2:
    url = cmdlist[1]
else:
    print('''使用方法：
    python main.py http://www.baidu.com
    python main.py http://baidu.com
    ''')
    sys.exit(0)


dq_system = platform.system() #当前系统
print('当前操作系：',dq_system)
xt_path = os.getcwd() #当前路径

def get_remote_machine_info(remote_host):  # 使用socket获取IP函数
    try:  # try-except块
        rip = socket.gethostbyname(remote_host)
        #print("IP address of %s: %s" % (remote_host, rip))
        # 打印远端设备名称及对应的IP地址
        return rip
    except socket.error as err_msg:    # 如果IP地址没有获取成功,则打印对应的错误消息
        print("%s: %s" % (remote_host, err_msg))
        return False


#url ="http://www.xiaodi8.com"

#检点url处理
if url.find(r'//'):
    if url.split(r'//')[1].startswith(r'www'):
        x_url = url.split(r'//')[1].replace(r"://www.","",1)
    else:
        x_url = url.split(r'//')[1]
else:
    if url.startswith(r'www'):
        x_url = url.replace(r"www.","",1)
    else:
        x_url = url

url_ip = get_remote_machine_info(url.split(r'//')[1])


add_header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
request=requests.get(url,headers=add_header,timeout=15)

#print(request.headers['Server'])


print('当前URL：' ,request.url)
print('当前请求状态：',request.status_code)
print('当前server信息：' ,request.headers['Server'])
print('当前请求服务器IP信息：' ,url_ip)

print('-----------------'*3)

if dq_system == 'Windows':
    #print('Windows系统')
    #打开目录扫描工具7kbscan-WebPathBrute
    print('打开目录扫描工具7kbscan-WebPathBrute')
    os.startfile(xt_path+"\\7kbscan-WebPathBrute 1.6.2\\7kbscan-WebPathBrute.exe")  # 打开软件
    
    print('运行nmap扫描端口')
    os.chdir(xt_path+"\\nmap-7.91")
    
    nmap_cmd_dict = {"SYN开放端口检测1-65535：":r"nmap -sS -p 1-65535 "+url_ip,
    "UDP开放端口检测1-65535：":r"nmap -sU -p 1-65535 "+url_ip,
    "URL系统检测A：":r"nmap -A "+url_ip,
    "URL地址系统：":r"nmap -O "+url_ip}
    
    for k,v in nmap_cmd_dict.items():
        print(k,v)
        nmap_cmd = os.popen(v, "r")
        nmap_cmd_d = nmap_cmd.read()
        print(nmap_cmd_d)
        
        '''
        if k == "SYN开放端口检测1-65535：":
            print("开放端口检测1-65535：nmap -p 1-65535 "+url_ip)
            nmap_cmd = os.popen(r"nmap -p 1-65535 "+url_ip, "r")
            nmap_cmd_d = nmap_cmd.read()
            print(nmap_cmd_d)
        '''
    nmap_cmd.close()
    os.chdir(xt_path)
    
    print('-----------------'*3)
    
    #print('进行子域名收集：')
    print('使用subbrute进行子域名收集：子域名信息存储在当前目录域名.txt')
    
    os.chdir(xt_path+"\\subbrute-master\\windows")
    print("开始收集：subbrute.exe -o %s\\%s.txt %s" % (xt_path,x_url,x_url))
    subbrute_cmd = os.popen(r"subbrute.exe -o %s\\%s.txt %s" % (xt_path,x_url,x_url), "r")
    subbrute_cmd_d = subbrute_cmd.read()
    print(subbrute_cmd_d)
    os.chdir(xt_path)
    
    print('-----------------'*3)
    
    #CMS识别
    print('使用http://whatweb.bugscaner.com在线CMS识别：',url)
    
    def whatweb(url):
        response = requests.get(url,verify=False)
        #只要获取到response即可
        whatweb_dict = {"url":response.url,"text":response.text,"headers":dict(response.headers)}
        whatweb_dict = json.dumps(whatweb_dict)
        whatweb_dict = whatweb_dict.encode()
        whatweb_dict = zlib.compress(whatweb_dict)
        data = {"info":whatweb_dict}
        return requests.post("http://whatweb.bugscaner.com/api.go",files=data)
    
    bugscaner_cms_request = whatweb(url)
    print(u"今日识别剩余次数：",bugscaner_cms_request.headers["X-RateLimit-Remaining"])
    print(u"识别结果",bugscaner_cms_request.json())
    
    #print('本地Windows下未找到好的识别工具后期补上')
    
    
    print('-----------------'*3)
    
    #WAF识
    print('使用wafw00f进行waf检测：')
    
    os.chdir(xt_path+"\\wafw00f-master")
    print("开始检测：python main.py %s" % url)
    subbrute_cmd = os.popen(r"python main.py %s" % url, "r")
    subbrute_cmd_d = subbrute_cmd.read()
    print(subbrute_cmd_d)
    os.chdir(xt_path)
    
    print('-----------------'*3)
    
    #CDN识别
    print("使用Ping检测是否存在CDN：ping "+x_url)
    cdn_ping_cmd = os.popen(r"ping "+x_url, "r")
    cdn_ping_cmd_d = cdn_ping_cmd.read()
    print(cdn_ping_cmd_d)
    if cdn_ping_cmd_d.splitlines()[1].split()[2] == x_url:
        print(x_url,'疑似不存在CDN')
    else:
        print(x_url,'疑似存在CDN')
    
    print('-----------------'*3)
    
    print("打开浏览器:")
    print("使用站长工具http://ping.chinaz.com/全国ping "+url)
    webbrowser.open('http://ping.chinaz.com/'+url)
    #技术有限不做页面数据抓取和分析
    
    print('-----------------'*3)
    
    #黑暗引擎查询
    print('使用fofa.os查询：https://fofa.so/result?q='+url_ip)
    webbrowser.open('https://fofa.so/result?q='+url_ip)
    print('使用fofa.os查询：https://fofa.so/result?q='+x_url)
    webbrowser.open('https://fofa.so/result?q='+x_url)
    print('使用www.shodan.io查询：https://www.shodan.io/host/'+url_ip)
    webbrowser.open('https://www.shodan.io/host/'+url_ip)
    print('使用www.zoomeye.org查询：https://www.zoomeye.org/searchResult?q='+url_ip)
    webbrowser.open('https://www.zoomeye.org/searchResult?q='+url_ip)
    
    print('-----------------'*3)
    
elif dq_system == 'Linux':
    print('Linux系统')
elif dq_system == 'Mac':
    print('MAC')
else:
    print('其他')

