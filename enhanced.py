import requests
import re
import os
import time
import sys
import hashlib

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

banner = """
 ____                    __                  
/\\  _`\\           __    /\\ \\                 
\\ \\,\\L\\_\\  _____ /\\_\\   \\_\\ \\     __   _ __  
 \\/_\\__ \\ /\\ '__`\\/\\ \\  /'_` \\  /'__`\\/\\`'__\\
   /\\ \\L\\ \\ \\ \\L\\ \\ \\ \\/\\ \\L\\ \\/\\  __/\\ \\ \\/ 
   \\ `\\____\\ \\ ,__/\\ \\_\\ \\___,_\\ \\____\\\\ \\_\\ 
    \\/_____/\\ \\ \\/  \\/_/\\/__,_ /\\/____/ \\/_/ 
             \\ \\_\\                           
              \\/_/                            by fengx1a0
"""


class com_fabiaoqing_www:
	def __init__(self):
		pass

	def get_info(self,url):
		res = requests.get(url=url,headers=headers)
		if "tag" in url:
			items = re.findall(r'data-original="([^"]+)" title="([^"]+)"',res.text)
		else:
			items = re.findall(r'data-original="([^"]+)" src="[^"]+" title="([^"]+)"',res.text)
		title = re.findall(r'<title>[\n\s]{0,50}(.*?)[\n\s]{0,50}</title>',res.text).pop().split("-").pop(0)
		if res.status_code != 200:
			print("请检查网络")
		return items,title

	def download(self,url):
		items,title = self.get_info(url)
		title = title.strip()
		if title and not os.path.exists(title):
			os.mkdir(title)
		for item in items:
			url = item[0].replace("bmiddle","large")
			filename = item[1].replace("/","").replace(".","").replace("\\","").replace("*","").replace(":","").replace("\n","").replace("\r","").replace("?","").replace(">","").replace("<","").replace("\"","").replace("\'","").replace("|","").strip()
			try:
				req = requests.get(url,headers=headers,timeout=3)
				while req.status_code != 200:
					time.sleep(0.15)
					req = requests.get(url,headers=headers,timeout=3)
				print("Staring Download...",filename)
				with open(title+"/"+filename+url[-4:],"wb") as fs:
					fs.write(req.content)
			except:
				pass

class com_doutula_www:
	def __init__(self):
		pass

	def get_info(self,url):
		res = requests.get(url=url,headers=headers)
		if "detail" in url:
			items = re.findall(r'src="(http://img.doutula.com/production/uploads/image/[^"]+)"',res.text)
		else:
			items = re.findall(r'data-original="(http://img.doutula.com/production/uploads/image/[^"]+)"',res.text)
		if res.status_code != 200:
			print("请检查网络")
		return items

	def download(self,url):
		items = self.get_info(url)
		title = "com_doutula_www - " + hashlib.md5(str(time.time()).encode()).hexdigest()
		if title and not os.path.exists(title):
			os.mkdir(title)
		for url in items:
			try:
				req = requests.get(url,headers=headers,timeout=3)
				while req.status_code != 200:
					time.sleep(0.15)
					req = requests.get(url,headers=headers,timeout=3)
				print("Staring Download...",url.rsplit("/",1)[1])
				with open(title+"/"+ url.rsplit("/",1)[1],"wb") as fs:
					fs.write(req.content)
			except:
				pass

class com_dbbqb_www:
	def __init__(self):
		pass
	def search_and_download(self,url):
		keyword = url.split("=",1)[1]
		url = "https://www.dbbqb.com/api/search/json?start=0&w=" + keyword
		try:
			res = requests.get(url,headers=headers,timeout=5)
		except Exception as e:
			print(e)
			print("请检查网络")
		items = res.json()
		title = "com_dbbqb_www - " + hashlib.md5(str(time.time()).encode()).hexdigest()
		if title and not os.path.exists(title):
			os.mkdir(title)
		for url in items:
			try:
				_url = "https://image.dbbqb.com/" + url['path']
				req = requests.get(_url,headers=headers,timeout=3)
				while req.status_code != 200:
					time.sleep(0.15)
					req = requests.get(_url,headers=headers,timeout=3)
				print("Staring Download...", _url.split("/",3).pop())
				with open(title+"/"+ _url.rsplit("/",2)[1] +'--'+ _url.rsplit("/",2)[2] + ".jpg","wb") as fs:
					fs.write(req.content)
			except Exception as e:
				print(e)


def menu():
	os.system('cls')
	print(banner)
	print("目前支持的网站: \n\t1.www.fabiaoqing.com\n\t2.www.doutula.com\n\t3.www.dbbqb.com\n支持自动下载当前页面的所有图片，不支持只有单张图片的页面\n")
	url = input("请输入完整url地址(比如你觉得https://fabiaoqing.com/bqb/detail/id/54595.html的表情不错,直接复制进来就可以啦): ")
	return url

def main():
	url = menu()
	if "fabiaoqing" in url:
		com_fabiaoqing_www().download(url)
	elif "doutula" in url:
		com_doutula_www().download(url)
	elif "dbbqb" in url:
		com_dbbqb_www().search_and_download(url)
	else:
		print("该网站尚未支持！")
	print("\n\n\ndownload successfully!")
	os.system("pause")

if __name__ == '__main__':
	main()
