# 财经智能数据分析 大作业

# 作业情况

### 小组成员

| 姓名   | 学号       | 贡献度 |
| ------ | ---------- | ------ |
| 刘天宇 | 2018312387 | 30%    |
| 王博远 | 2018312406 | 25%    |
| 刘国卿 |            | 20%    |
| 顾安   | 2018312388 | 15%    |



# 代码运行

按照以下指示运行即可：

1. 创建虚拟环境

   `conda create -n text_cnn python=3.5`

2. 激活虚拟环境

   `conda activate text_cnn`

3. 安装相关依赖

   `pip install -r requirements.txt`

4. 运行

   `python user.py`

   

## 效果展示与分析

如图所示，本系统具有如下四个功能：

![image-20220107112034294](https://s2.loli.net/2022/01/07/RyaXMDp75IxgEwL.png)

本文档将对各个功能依次进行展示

###  更新数据库

在本模块中具有两种具体的功能，一是手动输入股票代码进行数据更新，二是默认对数据库中所有股票进行更新，由于更新全部数据与单个股票数据原理一致，仅展示功能一：

![image-20220107112940855](https://s2.loli.net/2022/01/07/l3HwVMYfziIDyLr.png)

如图所示，以000012.sz为例完成了数据更新。

### 训练模型

输入数字2即可进行模型训练（基于已经获取的数据），此时控制台会反馈batch训练结果和一些关键参数，由于batch量过多此处只展示部分训练结果：

![image-20220107113500014](https://s2.loli.net/2022/01/07/8RVjGedXkHvUsK9.png)

### 股价预测

输入数字3可进行股价预测，首先进入我们存取的新闻数据库：

![image-20220107114129867](https://s2.loli.net/2022/01/07/lw1sNM6XjYaBZ7I.png)

任意选取一条新闻，例如图中第五条关于建投能源的新闻，将其输入到功能框中：

![image-20220107114558149](https://s2.loli.net/2022/01/07/mp8IRz4XlgBGYkd.png)

如图所示，建投能源对应的是积极面新闻，系统给出了上涨的预测，符合逻辑。

### 绘制词云

输入数字4后可以进行词云的绘制，利用本地新闻数据库中的高频词进行分析与绘制：

![image-20220107115633972](https://s2.loli.net/2022/01/07/mHvkq4KCVLyfIeJ.png)

如图所示，以上就是我们数据获取与分析系统的全部功能展示。