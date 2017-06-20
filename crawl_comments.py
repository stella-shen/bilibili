# -*- coding=gbk -*-

import os
import re
import sys
import json
import zlib
import types
import urllib2
import urlparse
from basic_classes import *

def down_page_comment(video_page_url, page = 1):
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
    comment_folder = r'./%s' % av_number
    if os.path.exists(comment_folder):
        pass
    else:
        os.makedirs(comment_folder)
    comment_list = down_page_comment(video_page_url, 1)
    print comment_list.page
    if comment_list.page == 1:
        comments_file = open('%s/comments.txt' % comment_folder, 'wb')
        for tip in temp_comment_list.comments:
                comments_file.write(str(tip.mid) + " " + str(tip.fbid) + " " + str(tip.ad_check) + " ")
                comments_file.write(str(tip.rank) + " " + str(tip.lv) + " ")
                comments_file.write(tip.nick)
                comments_file.write(" ")
                comments_file.write(tip.msg)
                comments_file.write("\n")
        comments_file.close()
    
    print comment_list.comment_len
    comments_file = open('%s/comments.txt' %(comment_folder), 'wb')
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
down_comments("http://www.bilibili.com/video/av1539763/")
