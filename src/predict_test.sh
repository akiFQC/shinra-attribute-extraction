python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_tohoku_bert/tohoku_bert/JP-5/City \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/City/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_mini/plain/City \
    --device "cuda:0";

echo "city end";
# 空行を除いて上書き保存
echo "空行削除"
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/City.json ;

python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_tohoku_bert/tohoku_bert/JP-5/Company \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/Company/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/Company.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/JP-5_mini/plain/Company\
    --device "cuda:0";

echo "空行削除"
# 空行を除いて上書き保存
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/JP-5/prediction_test/Company.json