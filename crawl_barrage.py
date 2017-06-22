# -*- coding=utf-8 -*-

import os
import re
import sys
import gzip
import json
import zlib
import types
import urllib2
import datetime
import StringIO
import urlparse

def down_barrage(video_page_url) :
    #get av_number
    parts = urlparse.urlparse(video_page_url).path
    av_number = parts.split("/")[-2];
    #make dir
    xml_folder = r'../movie_data/%s' % av_number
    if os.path.exists(xml_folder):
        pass
    else:
        os.makedirs(xml_folder)
    #analyze the video page
    video_page_request = urllib2.Request(video_page_url)
    video_page_gz = urllib2.urlopen(video_page_request).read()
    video_page_buffer = StringIO.StringIO(video_page_gz)
    #gzip decompress
    video_page_html = gzip.GzipFile(fileobj = video_page_buffer).read()
    
    #get chat ID number
    cid_number = re.findall(r'cid=(\d+)', video_page_html)[0]
    comments_page_url = 'http://comment.bilibili.tv/rolldate,%s' % cid_number
    comments_page_request = urllib2.Request(comments_page_url)
    comments_page_zip = urllib2.urlopen(comments_page_request).read()
    #deflate decompress
    comments_page_json = zlib.decompressobj(-zlib.MAX_WBITS).decompress(comments_page_zip)
    comments_python_object = json.loads(comments_page_json)
    for i in range(0, len(comments_python_object)): 
        comment_timestamp = comments_python_object[i]['timestamp']
        comment_then_url = 'http://comment.bilibili.tv/dmroll,%s,%s' % (comment_timestamp, cid_number)
        comment_then_request = urllib2.Request(comment_then_url)
        comment_then_zip = urllib2.urlopen(comment_then_request).read()
        comment_then_xml = zlib.decompressobj(-zlib.MAX_WBITS).decompress(comment_then_zip)
        comment_date = datetime.datetime.fromtimestamp(int(comment_timestamp)).strftime('%Y%m%d')
        comment_file = open('%s/%s.xml' % (xml_folder, comment_date), 'wb')
        comment_file.write(comment_then_xml)
        comment_file.close()
    #print cid_number

    #supplier's name
    #sup_name = re.findall(r'UP主：(..)+', video_page_html.encode('gbk'))[-1]
    #print sup_name
'''
    #supplier's weibo
    sup_weibo = re.findall(r'http://weibo.com/\w*', video_page_html)[0]
    if sup_weibo == "http://weibo.com/bilibiliweb":
        sup_weibo = ""
    #print sup_weibo

    infofile = open('%s/info.txt' % (xml_folder), 'wb')
    infofile.write("supplier's weibo: " + sup_weibo + "\n")
    infofile.close()
'''

if __name__ == '__main__':
    down_barrage('http://www.bilibili.com/video/av11315720/')
    down_barrage('http://www.bilibili.com/video/av11321491/')
    '''
    video_url_file = open('../movie_data/urlList')
    video_urls = video_url_file.readlines()
    for url in video_urls:
        print url
        down_barrage(url)
    '''