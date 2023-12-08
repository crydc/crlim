# 基于星火大模型的RAG开发
## 一个使用flask编写的个人知识库问答系统
1.本项目由登录，注册，上传文档，查看和删除文档，个人中心，AI对话与使用文档以及联系我们模块构成。


2.目前使用sqlite数据库储存数据，可自行链接数据库修改，个人中心尚未开放。


3.支持上传txt，pdf，md格式的文档。                              
# 关键技术
1.星火大模型API  


2.m3e embedding   


3.chroma向量数据库


4.flask      
# 本地运行部署方式
1.打开命令行或者虚拟环境shell。 


2.进入该文件夹目录，运行windows.bat程序，直接将windows.bat打在命令行上即可 。  

3.在弹出运行地址后点击地址用浏览器访问即可。
# 友情提示
1.代码很多地方待优化，在进入使用AI和与机器人聊天时反应非常慢，请耐心等待回复，切勿重复点击，会卡死的哦。

2.建议运行前删除vecbd文件夹与uploads文件夹下的所有内容，在运行时重新上传自己的文件，避免受到作者测试时上传的文件与创建的数据库影响。

3.如果有优化建议或者方法欢迎联系作者。

4.如果遇到网络链接问题，windows用户请在C:\Users\<你自己的电脑名>目录下创建名为.cache的文件夹，（linux用户请在/root/下创建）之后将代码文件中的chroma，huggingface，torch三个文件夹复制在.cache的文件夹下

例如:C:\Users\crlim目录下
```
├─.cache
│  ├─chroma
│  ├─huggingface
│  │  └─hub
│  └─torch
│      └─sentence_transformers
│          └─moka-ai_m3e-base
│              └─1_Pooling
```
## 最后如果有意见建议以及不合适或者错误的地方欢迎联系作者！！！谢谢，作者也很喜欢交朋友。最后希望大鲸鱼给我一个优秀学员！！！！
