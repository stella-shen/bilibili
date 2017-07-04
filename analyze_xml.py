#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import xml.etree.ElementTree as ET

def analyze_one_file(filename, barrage_dict):
    try:
        xml_tree = ET.ElementTree(file=filename)
        root = xml_tree.getroot()
    except:
        return

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
            if value is not None and send_time is not None and format_send_date is not None:
                line_info = u''.join(send_time + '\t' + format_send_date + '\t' + value + '\n').encode('utf-8')
                barrage_dict[barrage_id] = line_info

def analyze_all_xml():
    root_dir = '../movie_data/'
    for file in os.listdir(root_dir):
        file_dir = root_dir + file
        if file == 'av11303917' and os.path.isdir(file_dir):
            danmu_dict = dict()
            for sub_file in os.listdir(file_dir):
                print sub_file
                sub_file_dir = file_dir + '/' + sub_file
                file_type = sub_file.strip().split('.')[-1]
                if file_type == 'xml':
                    analyze_one_file(sub_file_dir, danmu_dict)
            danmu_file = open(file_dir+'/'+file+'.danmu', 'w')
            for key in danmu_dict:
                danmu_file.write(danmu_dict[key])
            danmu_file.close()


if __name__ == '__main__':
    analyze_all_xml()