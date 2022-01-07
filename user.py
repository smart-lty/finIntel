from database.create_dataset import *
from database.manage_data import connect, update_stock
from database.word_cloud import draw_wordcloud
from main import *
import torchtext.data as data
import torch
import warnings
from torchtext.data import Dataset
from torchtext.data.example import Example


warnings.filterwarnings('ignore')
class d(Dataset):
    def __init__(self, examples, fields, filter_pred=None):
        super().__init__(examples, fields, filter_pred=filter_pred)

def update():
    print("=" * 20 + "更新数据库" + "=" * 20)
    print("1: 手动输入股票代码 2：中证1000")
    try:
        op = int(input())
        if op not in [1, 2]:
            raise Exception
        if op == 1:
            print("请输入股票代码：")
            stock_code = input()
            connect()
            try:
                update_stock(stock_code)
            except:
                print("股票已更新")
        else:
            update_database()
            
    except Exception as e:
        print(e)
        print("非法输入！")

if __name__ == "__main__":
    print("=" * 20 + "财经智能分析大作业" + "=" * 20)
    print("操作提示：")
    print("1: 更新数据库 2: 训练模型 3: 股价预测 4: 绘制词云")
    print("=" * 58)
    
    # try:
    op = int(input())
    if op not in [1, 2, 3, 4]:
        raise Exception
    if op == 1:
        update()
    elif op == 2:
        model_train()
    elif op == 3:
        print("请输入新闻：")
        s = input()
        
        model = torch.load("snapshot/best_model.pth", map_location="cpu")
        x = text_field.preprocess(s)
        fields = [("id", None),("text", text_field), ("label", label_field)]
        y = Example.fromlist([None, s, None], fields)
        ds = d([y], fields)
        tmp = data.Iterator(ds, 1)
        pred = 0
        for i in tmp:
            pred = torch.softmax(model(i.text.t()).squeeze(), 0)
        if pred[0] >= pred[1]:
            print("预测结果：涨 (%.4f)" % pred[0])
        else:
            print("预测结果：跌 (%.4f)" % pred[1])
    
    elif op == 4:
        try:
            draw_wordcloud()
        except:
            print("There is not enough news for plot. Please update the database first!")
        
        
    # except Exception as e:
    #     print(e)
    #     print("非法输入！")
    