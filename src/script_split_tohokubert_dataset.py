from functools import wraps
import json 
import sys
import os 
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--source', '-s', default='/home/afukuchi/Codes/shinra-attribute-extraction/2020jp_tokenize_mecab_ipadic_bpe_tohoku_bert/JP-5/data1/ujiie/shinra/tohoku_bert/JP-5')
parser.add_argument('--target', '-t', default='/home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_tohoku_bert_mini')
parser.add_argument('--n', '-n', default=1000, type=int)
parser.add_argument('--start',  default=0, type=int)


args = parser.parse_args()

categories= ['City', 'Company']
for cat in categories:
    os.makedirs(os.path.join(args.target, cat), exist_ok=True)
    target_token_path = os.path.join(args.target, cat, 'tokens')
    os.makedirs(target_token_path, exist_ok=True)
    shutil.copyfile(os.path.join(args.source, cat, 'vocab.txt'), os.path.join(args.target, cat, 'vocab.txt'))
    shutil.copyfile(os.path.join(args.source, cat, 'attributes.txt'), os.path.join(args.target, cat, 'attributes.txt'))

    path_json = os.path.join(args.source, cat,  f'{cat}_dist.json')
    path_ta_json = os.path.join(args.target,cat, f'{cat}_dist.json')
    line_new = []
    with open(path_json, 'r') as  f0:
        for line in  f0.readlines()[args.start:args.start+args.n+1]:
            line_new.append(line)
            #line = line.encode("utf-8")
            print('line', line)
            dic = json.loads(line)
            page_id = dic['page_id']
            shutil.copyfile(
                os.path.join(args.source, cat, 'tokens', f'{page_id}.txt'),
                os.path.join(target_token_path, f'{page_id}.txt'),
                 )
    with open(path_ta_json , 'w') as  f1:
        f1.write('')

    with open(os.path.join(args.target,cat, f'__{cat}_dist__.json') , 'w') as  f1:
        f1.write(''.join(line_new))
        


