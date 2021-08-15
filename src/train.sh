python train.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/2020jp_tokenize_mecab_ipadic_bpe_tohoku_bert/JP-5/data1/ujiie/shinra/tohoku_bert/JP-5/City \
    --model_path models/City \
    --lr 1e-5 \
    --bsz 32 \
    --epoch 50 \
    --grad_acc 1 \
    --grad_clip 1.0 \
