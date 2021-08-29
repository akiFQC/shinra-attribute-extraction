import argparse
import sys
from pathlib import Path
import json
import copy
from typing import Optional

import torch
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
import torch.optim as optim
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

from dataset import ShinraData, NerDataset, ner_collate_fn
from model import BertForMultilabelNER, create_pooler_matrix

import os

device =  "cuda:0" if torch.cuda.is_available() else "cpu"

torch.backends.cudnn.benchmark = True

def ner_for_shinradata(model, tokenizer, shinra_dataset, device):
    processed_data = shinra_dataset.ner_inputs
    dataset = NerDataset(processed_data, tokenizer)
    total_preds, _ = predict(model, dataset, device, sent_wise=True)

    shinra_dataset.add_nes_from_iob(total_preds)

    return shinra_dataset


def predict(model, dataset, device, sent_wise=False):
    model.eval()
    dataloader = DataLoader(dataset, batch_size=64, collate_fn=ner_collate_fn)

    total_preds = []
    total_trues = []
    #print('total iteration = ', len(dataloader))
    with torch.no_grad():
        for step, inputs in enumerate(dataloader):
            input_ids = inputs["tokens"]
            word_idxs = inputs["word_idxs"]

            labels = inputs["labels"]

            input_ids = pad_sequence([torch.tensor(t) for t in input_ids], padding_value=0, batch_first=True).to(device)
            attention_mask = input_ids > 0
            pooling_matrix = create_pooler_matrix(input_ids, word_idxs, pool_type="head").to(device)

            with torch.cuda.amp.autocast():
                preds = model.predict(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    word_idxs=word_idxs,
                    pooling_matrix=pooling_matrix
                )

            total_preds.append(preds)
            # test dataの場合truesは使わないので適当にpredsを入れる
            total_trues.append(labels if labels[0] is not None else preds)
        #print('step', step)
    attr_num = len(total_preds[0])
    total_preds = [[pred for preds in total_preds for pred in preds[attr]] for attr in range(attr_num)]
    total_trues = [[true for trues in total_trues for true in trues[attr]] for attr in range(attr_num)]

    if sent_wise:
        total_preds = [[total_preds[attr][idx] for attr in range(attr_num)] for idx in range(len(total_preds[0]))]
        total_trues = [[total_trues[attr][idx] for attr in range(attr_num)] for idx in range(len(total_trues[0]))]

    return total_preds, total_trues


#wikipediaのデータ取得
def get_wiki(path,page_id,extension = "txt"):
    try:
        with open("{}/{}.{}".format(path,page_id,extension), "r", encoding = "utf_8") as f:
            return str(f.read())
    except FileNotFoundError:
        # raise FileNotFoundError("file not found","{}/{}.{}".format(path,page_id,extension) )
        return None

def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_path", type=str, help="Specify input path in SHINRA2020")
    parser.add_argument("--model_path", type=str, help="Specify attribute_list path in SHINRA2020")
    parser.add_argument("--output_path", type=str, help="Specify attribute_list path in SHINRA2020")
    parser.add_argument('--plain_path', type=str, default = "", help='Specify path of plain text in SHINRA2020 (plain text)')
    parser.add_argument('--device', type=str, default = "cuda:0", help='Specify path of plain text in SHINRA2020 (plain text)')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_arg()

    bert = AutoModel.from_pretrained("cl-tohoku/bert-base-japanese")
    tokenizer = AutoTokenizer.from_pretrained("cl-tohoku/bert-base-japanese")

    input_path = Path(args.input_path)
    print('input_path', input_path / "attributes.txt")
    assert (input_path / "attributes.txt").exists()
    with open(input_path / "attributes.txt", "r") as f:
        attributes = [attr for attr in f.read().split("\n") if attr != '']
    device=args.device 
    model = BertForMultilabelNER(bert, len(attributes))
    model.load_state_dict(torch.load(args.model_path, map_location='cpu'))
    model.to(device)

    # dataset = [ShinraData(), ....]
    dataset = ShinraData.from_shinra2020_format(Path(args.input_path))
    # dataset = [d for idx, d in enumerate(dataset) if idx < 20 and d.nes is not None]

    # dataset = [ner_for_shinradata(model, tokenizer, d, device) for d in dataset]
    print('output', args.output_path)
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    with open(args.output_path, "w") as f:
        for ii, data in enumerate(dataset):
            #print('gen dataset ', ii, ', data.nes=', data.nes, ',', data.nes is None)
            #print(ii, vars(data))
            if data.nes is None:
                processed_data = ner_for_shinradata(model, tokenizer, data, device)
                #print('processed_data', processed_data)
                #print([json.dumps(ne, ensure_ascii=False) for ne in processed_data.nes])
                
                processed_data_nes_postprocessed = []
                for ne in processed_data.nes:
                    #print('ne', ne)
                    if 'text_offset' in ne:
                        #print('ne', type(ne), ne, ne.keys())
                        dic = copy.deepcopy(ne)
                        id_text = ne["page_id"] 
                        if args.plain_path =="":
                            dic['text_offset']['text'] = "".join([ t.lstrip('#')  for t in  ne['token_offset']['text'].split(' ') ])
                        else:
                            offset_type = 'text_offset'
                            plain_text = get_wiki(args.plain_path, id_text)
                            #print('got text: ', plain_text[:20].replace("\n", ''))
                            if plain_text is None:
                                #print('\n\nargs.plain_path, id_text', plain_text,  args.plain_path, id_text)
                                dic['text_offset']['text'] = "".join([ t.lstrip('#')  for t in  ne['token_offset']['text'].split(' ') ])
                            else:
                                splitext = plain_text.split("\n")
                                accum = ""
                                for idx,line_id in enumerate(range(ne[offset_type]["start"]["line_id"],ne[offset_type]["end"]["line_id"]+1)):
                                    sol,eol = 0,len(splitext[line_id])
                                    if idx == 0:
                                        sol = ne[offset_type]["start"]["offset"]
                                    else:
                                        accum += "\n"
                                    if idx == ne[offset_type]["end"]["line_id"] - ne[offset_type]["start"]["line_id"]:
                                        eol = ne[offset_type]["end"]["offset"]
                                    accum += splitext[line_id][sol:eol]
                                dic['text_offset']['text']  = accum      
                        #print(dic['title'], ': predicted', dic['text_offset']['text'], ':', dic['token_offset']['text'])
                        processed_data_nes_postprocessed.append(dic)
                    else:
                        processed_data_nes_postprocessed.append(ne)
                    
                f.write("\n".join([json.dumps(ne, ensure_ascii=True) for ne in processed_data_nes_postprocessed]))
                #f.write("\n".join([json.dumps(ne, ensure_ascii=True) for ne in processed_data.nes]))
                f.write("\n")
