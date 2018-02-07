import requests
import urllib2
url = "http://huoxun.com/cms/api/lives.html?cid=news&page=2"
content = requests.get(url)
print content.content