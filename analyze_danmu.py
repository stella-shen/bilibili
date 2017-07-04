#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

def sort_file():
    root_dir = '../movie_data/'
    for file in os.listdir(root_dir):
        file_dir = root_dir + file
        if os.path.isdir(file_dir):
            print file
            danmu_file = file_dir+'/'+file+'.danmu'
            for sub_file in os.listdir(file_dir):
                if sub_file == file+'.danmu':
                    out_file = file_dir+'/'+file+'_sorted.danmu'
                    sort_cmd = "sort -t $'\t' -n -k1 %s > %s" % (danmu_file, out_file)
                    os.system(sort_cmd)

def analyze_one_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    l = int(float(lines[-1].strip().split('\t')[0])) + 1
    danmu_time = list()
    for line in lines:
        time = float(line.strip().split('\t')[0])
        danmu_time.append(time)
    bins = np.arange(0, l, 60)
    plt.hist(danmu_time, bins = bins)
    plt.xlabel('time')
    plt.ylabel('danmu number')
    file = filename.strip().split('/')[-1].split('_')[0]
    plt.savefig(file+'.jpg')
    plt.clf()



if __name__ == '__main__':
    av_list=['av1671130', 'av1691900', 'av2152016', 'av2853367', 'av10735186', 'av11303917', 'av11315720', 'av11321491']
    for av_num in av_list:
        analyze_one_file('../movie_data/%s/%s_sorted.danmu' % (av_num, av_num))
