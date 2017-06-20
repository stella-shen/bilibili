import re
import urllib2
import urlparse

url = "http://www.bilibili.com/video/av1531744/"
splits = urlparse.urlparse(url)
print splits
print splits.path.split("/")[-2]