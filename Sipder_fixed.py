import requests
import re
import os
import time
import sys

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

def getlist(_start):
	title = []
	for i in range(_start*20,(_start+1)*20):
		url = "https://fabiaoqing.com/tag/detail/id/%d/page/%d.html"%(i,1)
		try:
			res = requests.get(url=url,headers=headers,timeout=5)
			while res.status_code == 503:
				time.sleep(0.15)
				res = requests.get(url=url,headers=headers,timeout=5)
			t = re.findall(r'<title>(.*?)</title>',res.text).pop().split("-").pop(0)
			title.append(t)
		except Exception as e:
			print(e,'\n','请检查网络')
	return title

def get_info(_id,page_num):
	url = "https://fabiaoqing.com/tag/detail/id/%d/page/%d.html"%(_id,1)
	res = requests.get(url=url,headers=headers)
	items = re.findall(r'data-original="([^"]+)" title="([^"]+)"',res.text)
	title = re.findall(r'<title>(.*?)</title>',res.text).pop().split("-").pop(0)
	print("Loading Page...",title,'1')
	if res.status_code != 200:
		print("请检查网络")
	page = re.findall(r'[\S\n\s]{200}下一页',res.text)
	if page:
		try:
			page = page[1].split("<").pop(0).strip()
			page = page if int(page) <= page_num else page_num
			for i in range(2,int(page)+1):
				print("Loading Page...",title,i)
				url = "https://fabiaoqing.com/tag/detail/id/%d/page/%d.html"%(_id,i)
				res = requests.get(url=url,headers=headers,timeout=5)
				while res.status_code != 200:
					res = requests.get(url=url,headers=headers,timeout=5)
					time.sleep(0.15)
				items.extend(re.findall(r'data-original="([^"]+)" title="([^"]+)"',res.text))
		except Exception as e:
			print(e,'\n','请检查网络')
	return items,title

def download(_ids,page_num):
	items,title = get_info(_ids,page_num)
	title = title.strip()
	if title and not os.path.exists(title):
		os.mkdir(title)
	for item in items:
		url = item[0].replace("bmiddle","large")
		filename = item[1].replace("/","").replace(".","").replace("\\","").replace("*","").replace(":","").replace("\n","").replace("\r","").replace("?","").replace(">","").replace("<","").replace("\"","").replace("\'","").replace("|","").strip()
		try:
			req = requests.get(url,headers=headers,timeout=3)
			while req.status_code != 200:
				req = requests.get(url,headers=headers,timeout=3)
			print("Staring Download...",filename)
			with open(title+"/"+filename+'.jpg',"wb") as fs:
				fs.write(req.content)
		except:
			pass

def menu():
	choice = -1
	index = 1
	while choice == -1:
		os.system("cls")
		print("请选择标签: \n当前第%d页 Loading..."%index)
		titles = getlist(index)
		[print(str(_) + "." + titles[_]) for _ in range(0,20)]
		i = input("下一页/标签页号(n/number):").strip()
		if i.lower() == "n":
			index += 1
		else:
			choice = int(i)
	return index*20 + choice

def main():
	_ids = menu()
	page_num = int(input("该分类需要下载的数量 * 40(可能会出现资源本身没这么多的情况): "))
	download(_ids,page_num)
	print('\n\n\n下载完成！')
	os.system("pause")

if __name__ == '__main__':
	main()