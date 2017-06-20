# -*- coding=gbk -*-
import StringIO
import datetime
import gzip
import json
import os
import re
import urllib2
import urlparse
import zlib
import sys
import types
from basic_classes import *

def down_barrage(video_page_url) :
    #get av_number
    parts = urlparse.urlparse(video_page_url).path
    av_number = parts.split("/")[-2];
    #make dir
    xml_folder = r'./%s' % av_number
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
    #print video_page_html
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

    #supplier's weibo
    sup_weibo = re.findall(r'http://weibo.com/\w*', video_page_html)[0]
    if sup_weibo == "http://weibo.com/bilibiliweb":
        sup_weibo = ""
    #print sup_weibo

    #video tags
    video_tags = re.findall(r'kwtags\(\[[(..), \w, \W]*\]\)', video_page_html)[0]
    #print video_tags

    infofile = open('%s/info.txt' % (xml_folder), 'wb')
    infofile.write("supplier's weibo: " + sup_weibo + "\n")
    infofile.write("tags info: " + video_tags + "\n")
    infofile.close()

def down_page_comment(video_page_url, page = None):
    parts = urlparse.urlparse(video_page_url).path
    av_number = parts.split("/")[-2][2:];
    url = 'http://api.bilibili.com/feedback?type=jsonp&ver=3&mode=arc&aid=%s&pagesize=20&page=%d'%(av_number, page)
    request = urllib2.Request(url)
    page_zip = urllib2.urlopen(request).read()
    json_info = json.loads(page_zip)
    comment_list = CommentList();
    comment_list.comments = []
    comment_list.comment_len = json_info['results']
    comment_list.page = json_info['pages'];
    info_list = json_info['list']
    for i in info_list:
        cur_info = info_list[i]
        tip = Comment()
        tip.lv = cur_info.get('lv')
        tip.fbid = cur_info.get('fbid')
        tip.msg = cur_info.get('msg')
        tip.ad_check = cur_info.get('ad_check')
        tip.mid = cur_info.get('mid')
        tip.rank = cur_info.get('rank')
        tip.nick = cur_info.get('nick')
        tip.reply_count = cur_info.get('reply_count')
        comment_list.comments.append(tip)
        if tip.reply_count == 0:
            continue
        else:
            reply_list = cur_info.get('reply')
            for j in reply_list:
                cur_reply = reply_list[j]
                reply_tip = Comment()
                reply_tip.lv = cur_reply.get('lv')
                reply_tip.fbid = cur_reply.get('fbid')
                reply_tip.msg = cur_reply.get('msg')
                reply_tip.ad_check = cur_reply.get('ad_check')
                reply_tip.mid = cur_reply.get('mid')
                reply_tip.rank = cur_reply.get('rank')
                reply_tip.nick = cur_reply.get('nick')
                reply_tip.reply_count = cur_reply.get('reply_count')
                comment_list.comments.append(reply_tip)
    return comment_list


def down_comments(video_page_url):
    #get av_number
    parts = urlparse.urlparse(video_page_url).path
    av_number = parts.split("/")[-2];
    #make dir
    xml_folder = r'./%s' % av_number
    if os.path.exists(xml_folder):
        pass
    else:
        os.makedirs(xml_folder)
    comment_list = down_page_comment(video_page_url, 1)
    print comment_list.page
    if comment_list.page == 1:
        comments_file = open('%s/comments.txt' % xml_folder, 'wb')
        for tip in temp_comment_list.comments:
                comments_file.write(str(tip.mid) + " " + str(tip.fbid) + " " + str(tip.ad_check) + " ")
                comments_file.write(str(tip.rank) + " " + str(tip.lv) + " ")
                comments_file.write(tip.nick)
                comments_file.write(" ")
                comments_file.write(tip.msg)
                comments_file.write("\n")
        comments_file.close()
    
    print comment_list.comment_len
    comments_file = open('%s/comments.txt' %(xml_folder), 'wb')
    for p in range(1, comment_list.page):
        temp_comment_list = down_page_comment(video_page_url, page = p)
        for tip in temp_comment_list.comments:
            comments_file.write(str(tip.mid) + " " + str(tip.fbid) + " " + str(tip.ad_check) + " ")
            comments_file.write(str(tip.rank) + " " + str(tip.lv) + " ")
            comments_file.write(tip.nick)
            comments_file.write(" ")
            comments_file.write(tip.msg)
            comments_file.write("\n")
    comments_file.close()
#solve the problem of msg cannot write
#referred to http://wangye.org/blog/archives/629/
reload(sys)
sys.setdefaultencoding('utf-8')
down_barrage("http://www.bilibili.com/video/av1497960/")
down_comments("http://www.bilibili.com/video/av1539763/")
