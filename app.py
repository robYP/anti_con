from flask import Flask, render_template, request
# from flask_ngrok import run_with_ngrok
import joblib
from transformers import BertTokenizerFast, BertModel
from sklearn import svm
import torch
import gdown
import os

# 初始化 Flask app
app = Flask(__name__)

# Check if "bert_model/pytorch_model.bin" doesn't exist, if so, download the necessary files
if not os.path.exists("./bert_model/pytorch_model.bin"):
    # create a folder named "bert_model" if it doesn't exist
    if not os.path.exists("bert_model"):
        os.makedirs("bert_model")

    # Download models from googleDrive using gdown
    bert_config_id = '1rGlxtTxFJni1YVQrbRVVo7WGvzK6tIm9'
    bert_model_id = '1VyY3JgyZztj45iJFN8B14s2aY1-l0bkx'
    svm_model_id = '1Tu67bWlC9ekg6_KKJ8Cz3hUHwXOZWk8e'

    gdown.download(id=bert_config_id, output="./bert_model/config.json", quiet=False)
    gdown.download(id=bert_model_id, output="./bert_model/pytorch_model.bin", quiet=False)
    gdown.download(id=svm_model_id, output="svm_model.pkl", quiet=False)

# 1. 加載模型和其他資源
tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
# bert = BertModel.from_pretrained('bert-base-chinese')
bert = BertModel.from_pretrained('bert_model/')
clf = joblib.load('svm_model.pkl')

# 2. 定義預測函數
def predict(input_text):
    with torch.no_grad():
        inputs = tokenizer([input_text], padding=True, truncation=True, return_tensors="pt")
        input_ids = inputs["input_ids"]
        attention_masks = inputs["attention_mask"]
        features = bert(input_ids, attention_mask=attention_masks)[1].detach().numpy()
        prediction = clf.predict(features)
        if bool(prediction[0]) == True:
          return "有詐騙的可能性，請聯絡165進行確認"
        else:
          return "詐騙的可能性較低，若有疑慮請聯絡165進行確認"

# 3. 定義 Flask 路由
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/predict_route', methods=['POST'])
def predict_route():
    user_input = request.form['predict']
    message = predict(user_input)
    user_input_record = str(user_input)

    return render_template('result.html', message=message, user_input_record=user_input_record)

# 啟動 Flask 應用
if __name__ == '__main__':
    app.run()


# import torch
# x = torch.rand(5, 3)
# print(x)