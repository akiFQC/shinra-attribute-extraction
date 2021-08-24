from functools import wraps
import json 
import sys
import os 
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--source', '-s', default='/home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_original')
parser.add_argument('--target', '-t', default='/home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_mini')
parser.add_argument('--n', '-n', default=100, type=int)
parser.add_argument('--start',  default=100, type=int)


args = parser.parse_args()

categories= ['City', 'Company']
for cat in categories:
    path_json = os.path.join(args.source, 'annotation', f'{cat}_dist.json')
    path_ta_json = os.path.join(args.target, 'annotation', f'{cat}_dist.json')
    dir_target = os.path.join(args.target, 'plain', cat)
    os.makedirs(dir_target, exist_ok=True)
    os.makedirs(os.path.join(args.target, 'annotation'), exist_ok=True)

    line_new = []
    with open(path_json, 'r') as  f0:
        for line in  f0.readlines()[args.start:args.start+args.n+1]:
            line_new.append(line)
            #line = line.encode("utf-8")
            print('line', line)
            dic = json.loads(line)
            page_id = dic['page_id']
            shutil.copyfile(os.path.join(args.source,'plain',cat, f'{page_id}.txt'), os.path.join(dir_target, f'{page_id}.txt'))
    with open(path_ta_json , 'w') as  f1:
        f1.write(''.join(line_new))
        


