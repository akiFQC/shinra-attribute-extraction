python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/2020jp_tokenize_mecab_ipadic_bpe_tohoku_bert/JP-5/data1/ujiie/shinra/tohoku_bert/JP-5/City \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/City/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_original/plain/City \
    --device "cuda:0";

echo "city end";
# 空行を除いて上書き保存
echo "空行削除"
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City.json ;
