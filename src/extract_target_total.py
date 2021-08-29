
from functools import wraps
from genericpath import exists
import json 
import sys
import os 
import argparse
import shutil
import glob
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('--query', '-q', default='/home/afukuchi/Codes/shinra-attribute-extraction/total_targets')
parser.add_argument('--source', '-t', default='/home/afukuchi/Codes/shinra-attribute-extraction/2020jp_tokenize_mecab_ipadic_bpe_tohoku_bert/JP-5/data1/ujiie/shinra/tohoku_bert/JP-5')
parser.add_argument('--output', default='/home/afukuchi/Codes/shinra-attribute-extraction/JP-5/for_total_prediction')
args = parser.parse_args()


for category in ['City', 'Company']:
    dir_src  = os.path.join(args.source, category)
    token_dir_src = os.path.join(dir_src, 'tokens')
    os.makedirs(os.path.join(args.output, category), exist_ok=True)
    shutil.copyfile(os.path.join(dir_src, 'attributes.txt'), os.path.join(args.output, category, 'attributes.txt'))
    shutil.copyfile(os.path.join(dir_src, 'vocab.txt'),os.path.join(args.output, category, 'vocab.txt'))
    with open(os.path.join(args.output, category, f'{category}_dist.json'),  'w') as f:
        f.write('')
    token_dir_out =  os.path.join(args.output, category, 'tokens')
    with open(os.path.join(args.query, f'{category.lower()}_target.txt'), 'r')as f:
        tokens_query = [ s.strip('\n') for s in f.readlines()]
    os.makedirs(token_dir_out, exist_ok=True)
    for page_id in tokens_query:
        shutil.copyfile(os.path.join(token_dir_src, f'{page_id}.txt'), os.path.join(token_dir_out,  f'{page_id}.txt'))