import os
import time
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

authen = {
    'username': '',
    'password': '',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

session = requests.Session()

def get_web(url):
	try:
		page =session.get(url, headers=headers, timeout=10)
		return page
	except requests.exceptions.Timeout:
		print("界面超时，请重试。")
		exit(0)

login_page = get_web("https://sso.buaa.edu.cn/login?service=https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/*default/index.do")
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

def query():
    yx_url = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadKbxx.do?sfyx=1&sfjzsyzz=1&_="
    timestamp = int(time.time() * 1000)
    yx_url = yx_url + str(timestamp)
    response = get_web(yx_url)
    yx = response.json()

    bjdm = []
    yxk = {}
    for nr in yx["xkjgList"]:
        if nr["BJDM"] not in set(bjdm) and "MXMK" not in nr["BJDM"]:
            bjdm.append(nr["BJDM"])
            yxk[nr["BJDM"]] = nr["YYZ"]

    base_url = "https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/xsxkCourse/loadAllCourseInfo.do?"
    timestamp = int(time.time() * 1000)
    new_url = base_url + "_=" + str(timestamp) + "&pageSize=3000"

    course = get_web(new_url)
    courses = course.json()

    bjdm_set = set(bjdm)

    head = ["课程名称", "授课教师", "学分", "线下容量", "线上容量", "已选", "意愿值"]
    cours = []
    for course in courses["datas"]:
        if course["BJDM"] in bjdm_set:
            cours.append(
                [course['KCMC'], course['RKJS'], course['KCXF'], course['KXRS'], course['XSRL'], course['YXXKJGRS'],
                 yxk[course["BJDM"]]])

    print(tabulate(cours, head, tablefmt="fancy_grid"))


def loop():
	a = int(input("按1刷新，其余键退出："))
	if a == 1:
		os.system('cls')
		query()
		loop()
	else:
		session.close()
		exit(0)

if __name__ == "__main__":
	query()
	loop()
