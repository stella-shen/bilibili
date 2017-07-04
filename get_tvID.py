# -*- coding=utf-8 -*-

import re, gzip, urllib2, StringIO

def get_tv_id(video_page_url):
    #get video id
    parts = video_page_url.strip().split('/')
    video_id = parts[-1].strip().split('#')[0].strip().split('.')[0]
    
    #analyze the video page
    video_page_gz = urllib2.urlopen(video_page_url).read()

    #get tvID number
    tvID = re.findall(r'data-player-tvid="(\d+)"', video_page_gz)[0]
    return video_id, tvID

if __name__ == '__main__':
    url_file = open('url_list', 'r')
    url_lines = url_file.readlines()

    out_file = open('tvID', 'w')

    for url in url_lines:
        video_id, tvID = get_tv_id(url)
        cur_line = video_id + '\t' + tvID + '\n'
        out_file.write(cur_line)

    url_file.close()
    out_file.close()
