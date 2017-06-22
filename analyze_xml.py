#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import xml.etree.ElementTree as ET

def analyze_one_file(filename, barrage_dict):
    xml_tree = ET.ElementTree(file=filename)
    root = xml_tree.getroot()

    for child in root:
        attribs = child.attrib
        if attribs.has_key('p'):
            attribs_values = attribs['p']
            attribs_values = attribs_values.strip().split(',')
            
            barrage_id = attribs_values[-1]
            if barrage_dict.has_key(barrage_id):
                continue

            send_time = attribs_values[0]
            sent_timestamp = float(attribs_values[4])
            st = time.localtime(sent_timestamp)
            format_send_date = time.strftime('%Y-%m-%d %H:%M:%S', st)
            value = child.text
            
            line_info = u''.join(send_time + '\t' + format_send_date + '\t' + value + '\n').encode('utf-8')
            barrage_dict[barrage_id] = line_info

if __name__ == '__main__':
    barrage_dict = dict()
    root_dir = '../movie_data/'
    analyze_one_file('../movie_data/av11315720/20170620.xml', barrage_dict)
    out_file = open('../movie_data/av11315720/av11315720.danmu', 'w')
    for key in barrage_dict:
        out_file.write(barrage_dict[key])
    out_file.close()