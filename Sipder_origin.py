import requests
import re
import os
import time
import sys

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}

def get_info(_id,page_num):
	url = "https://fabiaoqing.com/tag/detail/id/%d/page/%d.html"%(_id,1)
	res = requests.get(url=url,headers=headers)
	items = re.findall(r'data-original="([^"]+)" title="([^"]+)"',res.text)
	title = re.findall(r'<title>(.*?)</title>',res.text).pop().split("-").pop(0)
	page = re.findall(r'[\S\n\s]{200}下一页',res.text)
	if page:
		page = page[1].split("<").pop(0).strip()
		page = page if int(page) <= page_num else page_num
		for i in range(2,int(page)+1):
			print("Loading Page...",title,i)
			url = "https://fabiaoqing.com/tag/detail/id/%d/page/%d.html"%(_id,i)
			res = requests.get(url=url,headers=headers)
			items.extend(re.findall(r'data-original="([^"]+)" title="([^"]+)"',res.text))
	return items,title

def download(_ids,page_num):
	items,title = get_info(_ids,page_num)
	title = title.strip()
	if not os.path.exists("./Database"):
		os.mkdir("./Database")
	if title and not os.path.exists("./Database/" + title):
		os.mkdir("./Database/" + title)
	for item in items:
		url = item[0].replace("bmiddle","large")
		filename = item[1].replace("/","").replace(".","").replace("\\","").replace("*","").replace(":","").replace("\n","").replace("\r","").replace("?","").replace(">","").replace("<","").replace("\"","").replace("\'","").replace("|","").strip()
		try:
			req = requests.get(url,headers=headers,timeout=3)
			if req.status_code != 200:
				continue
			print("Staring Download...",filename)
			with open("./Database/"+title+"/"+filename+'.jpg',"wb") as fs:
				fs.write(req.content)
		except:
			pass

def main(depth,page_num):
	for i in range(1,depth):
		download(i,page_num)

if __name__ == '__main__':
	print("data will saved into folder `./Database`")
	if len(sys.argv) != 3:
		exit("Invaild Option:\n\npython fidder.py DEPTH MAX_PAGE_NUM_OF_EACH\n\nExample: python fiddle.py 10 10")
	main(int(sys.argv[1]),int(sys.argv[2]))