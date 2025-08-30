import time
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

authen = {
    'username': '',
    'password': '',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'origin': 'https://yjsxk.buaa.edu.cn',
    'referer' : 'https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/course.html'
}

session = requests.Session()
login_page = session.get("https://sso.buaa.edu.cn/login?service=https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/*default/index.do")
soup = BeautifulSoup(login_page.text, 'html.parser')
execution_input = soup.find('input', {'name': 'execution'})
execution_value = execution_input.get('value', '')

login_data = {
    'username': authen['username'],
    'password': authen['password'],
    'type': 'username_password',
    'submit': 'LOGIN',
    '_eventId': 'submit',
    'execution':execution_value
}

response = session.post("https://sso.buaa.edu.cn/login", data=login_data)

yx_url="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadKbxx.do?sfyx=1&sfjzsyzz=1&_="
timestamp = int(time.time() * 1000)
yx_url=yx_url+str(timestamp)
response = session.get(yx_url, headers=headers)
yx=response.json()

bjdm=[]
for nr in yx["rqpkjgallList"]:
	if nr["bjdm"] not in set(bjdm):
		bjdm.append(nr["bjdm"])

base_url="https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadAllCourseInfo.do?"
timestamp = int(time.time() * 1000)
new_url = base_url + "_=" + str(timestamp)+"&pageSize=3000"

course=session.get(new_url, headers=headers)
courses = course.json()

bjdm_set = set(bjdm)

head = ["课程名称", "学分","容量", "已选"]
cours=[]
for course in courses["datas"]:
    if course["BJDM"] in bjdm_set:
        cours.append([course['KCMC'],course['KCXF'],course['KXRS'],course['YXXKJGRS']])

print(tabulate(cours, head, tablefmt="fancy_grid"))
session.close()
