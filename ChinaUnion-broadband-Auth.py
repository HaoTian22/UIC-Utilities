import requests
import re
import base64

'''自己修改的数据'''
# UIC网络账户
UICAccountID='t*******'
# 运营商宽带密码
wlan_password='*******' 
# UIC网络密码
UICPassword='*******'

'''以下部分应该不用修改，如果不同可以自己修改'''
# 推算出来的学号
UICStudentID='2'+UICAccountID[1:]
# 推算出来的宽带用户名
username='vip'+UICStudentID

# 固定数据
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69',
    'Content-Type': 'application/x-www-form-urlencoded'
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Content-Length": "195",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "portal.gd165.com",
    "Origin": "http://portal.gd165.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://portal.gd165.com/?wlanuserip=172.29.105.168&wlanacname=&basname=120.80.200.50&ssid=uiczh.edu&vlanid=ethtrunk/10:4001.0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"
}




# 第一层-UIC登录
AuthIP=requests.get('http://www.gstatic.com/generate_204')
if AuthIP.status_code==204:
  print("Already login")
else:
  print(AuthIP)
redirect_url=requests.get("http://www.baidu.com",allow_redirects=False).headers['Location']
match = re.search(r"byod", redirect_url)
if match:
  # http://172.29.250.5:30004/byod/byodrs/login/defaultLogin
  UICauth= requests.post(url=redirect_url,data='{{"userName":"{0}","userPassword":"{1}","serviceSuffixId":"-1","dynamicPwdAuth":false,"code":"","codeTime":"","validateCode":"","licenseCode":"","userGroupId":0,"validationType":0,"guestManagerId":0,"shopIdE":null,"wlannasid":null}}'.format(UICAccountID,base64.b64encode(UICPassword.encode('utf-8')).decode('utf-8')))
  # print("Getting UIC Login Page...")
  # print(UICauth)
  UICauth_result=eval(UICauth.text)
  if UICauth_result["code"]==-1:
    print("Failed")



# 第二层-运营商登录

redirect_url=requests.get("http://www.baidu.com",allow_redirects=False).headers['Location']
wlanip = re.findall(r"wlanuserip=(.*)", redirect_url)[0]
#  requests.get("http://portal.gd165.com/?wlanuserip=172.29.105.168&wlanacname=&basname=120.80.200.50&ssid=uiczh.edu&vlanid=ethtrunk/10:4001.0")

login_page=requests.post(url="http://portal.gd165.com/index.do",data="basPushUrl=http%3A%2F%2Fportal.gd165.com%2F%3Fwlanuserip%3D{}%26wlanacname%3D%26basname%3D120.80.200.50%26ssid%3Duiczh.edu%26vlanid%3Dethtrunk%2F10%3A4001.0&debugua=&testmacauth=false".format(wlanip),headers=headers)

# basPushUrl=http%3A%2F%2Fportal.gd165.com%2F%3Fwlanuserip%3D172.29.105.168%26wlanacname%3D%26basname%3D120.80.200.50%26ssid%3Duiczh.edu%26vlanid%3Dethtrunk%2F10%3A4001.0&debugua=&testmacauth=false
print("Getting ChinaUnion Login Page...")
# print(login_page.text)

def extract_token(html_code):
  pattern = r'<input type="hidden" name="token" value="(.*?)" />'
  match = re.search(pattern, html_code)
  if match:
    return match.group(1)
  else:
    return None

token = extract_token(login_page.text)

login_result=requests.post(url='http://portal.gd165.com/login.do',data='loginpage=gd%2Fzhbsd%2Flogin.jsp&onlinepage=gd%2Fzhbsd%2Fonline.jsp&logoutpage=&accountprefixname=&accountsuffixname=&pagetype=0&macauth=0&accountvalid=1800&customerId=001&customerName=campus&basName=120.80.200.50&basPushUrl=http%3A%2F%2Fportal.gd165.com%2F%3Fwlanuserip%3D{0}%26wlanacname%3D%26basname%3D120.80.200.50%26ssid%3Duiczh.edu%26vlanid%3Dethtrunk%2F10%3A4001.0&accountName=&sendSMS=&attrName=ssid&attrValue=%5Buiczh.edu%5D&realmName=&fixedAccountPrefixName=&errormessage=&keepAliveTime=&wlanuserip={0}&client_type=pz&basname=120.80.200.50&setUserOnline=&userOpenAddress=&accountType=&token={1}&checkbox=0&username={2}3&password={3}'.format(wlanip,token,username,wlan_password),headers=headers)

# loginpage=gd%2Fzhbsd%2Flogin.jsp&onlinepage=gd%2Fzhbsd%2Fonline.jsp&logoutpage=&accountprefixname=&accountsuffixname=&pagetype=0&macauth=0&accountvalid=1800&customerId=001&customerName=campus&basName=120.80.200.50&basPushUrl=http%3A%2F%2Fportal.gd165.com%2F%3Fwlanuserip%3D172.29.105.168%26wlanacname%3D%26basname%3D120.80.200.50%26ssid%3Duiczh.edu%26vlanid%3Dethtrunk%2F10%3A4001.0&accountName=&sendSMS=&attrName=ssid&attrValue=%5Buiczh.edu%5D&realmName=&fixedAccountPrefixName=&errormessage=&keepAliveTime=&wlanuserip=172.29.105.168&client_type=pz&basname=120.80.200.50&setUserOnline=&userOpenAddress=&accountType=&token=6521488d5ee29672df88d4ddbd594faf&checkbox=0&username=&password=
def find_login_failed(html_code):
  pattern = r"登录失败"
  match = re.search(pattern, html_code)
  return match is not None

print("Login result")
if find_login_failed(login_result.text):
  print("Wrong Account or Already Login")
