python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_tohoku_bert_mini/City \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/City/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City_prediction.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_original/plain/City \
    --device "cuda:0";

echo "city end";
# 空行を除いて上書き保存
echo "空行削除"
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City_prediction.json ;
#    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_original/plain/City \