# encoding=utf-8
import os

root_dir = '../data/iqiyi/'

for video_path in os.listdir(root_dir):
    video_dir = root_dir + video_path
    if os.path.isfile(video_dir):
        video_id = video_path.strip().split('.')[0].split('_')[-1]
        print 'loading video: '+ video_id
        out_dir = '../data/iqiyi/%s/' % (video_id)
        os.mkdir(out_dir)
        decode_cmd = '../bin/ffmpeg -v 0 -i %s -r 1 ../data/iqiyi/%s/%s_%s.jpg' % (video_dir, video_id, video_id, '%5d')
        os.system(decode_cmd)

