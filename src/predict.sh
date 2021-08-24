python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/inputs/tohoku_bert/JP-5/City \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/City/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/outputs/tohoku_bert/JP-5/Submission/City.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/test_for_leaderboard/target_data/plain/City ;  \

echo "city end";
# 空行を除いて上書き保存
echo "空行削除"
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/outputs/tohoku_bert/JP-5/Submission/City.json

python predict.py \
    --input_path /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/inputs/tohoku_bert/JP-5/Company \
    --model_path /home/afukuchi/Codes/shinra-attribute-extraction/models/20210820/Company/best.model \
    --output_path /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/outputs/tohoku_bert/JP-5/Submission/Company.json \
    --plain_path /home/afukuchi/Codes/shinra-attribute-extraction/test_for_leaderboard/target_data/plain/Company ;\
echo "空行削除"
# 空行を除いて上書き保存
sed -i '/^$/d' /home/afukuchi/Codes/shinra-attribute-extraction/for_leaderbord_JP-5/outputs/tohoku_bert/JP-5/Submission/Company.json