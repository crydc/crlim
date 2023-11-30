from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import re
from flask_wtf import CSRFProtect
from loginform import LoginForm
from registerform import RegisterForm
from uploadform import UploadForm
import os
import glob
import SparkApi
from langchain.embeddings import HuggingFaceEmbeddings
from pdfhandle import DocumentLoader
from vecdb import VECDB
from userbd import users_data #用于模拟的数据表

embedding = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
app = Flask(__name__ , template_folder= 'templates' )
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'mrsoft'
app.config['UPLOAD_FOLDER'] = 'uploads'
#以下密钥信息从控制台获取
appid = "af921eeb"     #填写控制台中获取的 APPID 信息
api_secret = "NjAwYTIxNzg2NzdmMWMxZWY4YzllYjJh"   #填写控制台中获取的 APISecret 信息
api_key ="fad1c4ea7725ad8c10da7ae8daa535ba"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
#domain = "general"   # v1.5版本
domain = "generalv2"    # v2.0版本
#云端环境的服务地址
#Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

chat_history = []
text =[]

# 要查看的文件夹路径
folder_path = './uploads'


# 获取文件夹下的文件列表
def get_file_list():
    return os.listdir(folder_path)

# 删除文件
def delete_file(filename):
    try:
        os.remove(os.path.join(folder_path, filename))
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def check_pdf_files_pdf(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            return True
    return False

def check_pdf_files_md(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            return True
    return False

def check_pdf_files_txt(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            return True
    return False

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


#判断是否email函数
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

#主页面
@app.route('/')
def index():
    return render_template('index.html')

#注册页面
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        uesrname = form.username.data
        password = form.pwd.data
        if uesrname in users_data:
            flash('用户名已存在，请选择其他用户名', 'error')
        else:
            users_data[uesrname] = {'username': uesrname, 'password': password}
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
    return render_template('register.html',form=form)

#登录页面
@app.route('/login', methods=['GET','POST'])
def login():
    #登录界面
    form = LoginForm()
    if form.validate_on_submit(): 
        uesrname = form.name.data
        user = users_data.get(uesrname)
        password = form.password.data
        if user is None:
            flash('你还没有注册','error')
        elif password == user['password']:
            flash('登录成功', 'success')
            return redirect(url_for('home'))
            session['logged_in'] = True
        else:
            flash('登录失败，请检查用户名和密码', 'error')
    return render_template('login.html',form=form)


#上传文件页面
@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'logged_in' not in session :
        return redirect(url_for('index'))
    else:
        form = UploadForm()
        if form.validate_on_submit():
            file = form.file.data
            if file == None:
                flash('你没有上传文件')
            else:
                file.save(os.path.join('uploads', file.filename))
                flash('上传成功')
            return redirect(url_for('home'))
        return render_template('upload.html',form=form)


#查看文件与删除文件页面
@app.route('/files', methods=['GET', 'POST'])
def files():
    if 'logged_in' not in session :
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            file_to_delete = request.form.get('file_to_delete', '')
            if file_to_delete:
                success = delete_file(file_to_delete)
                file_list = get_file_list()
                return render_template('files.html', files=file_list, delete_success=success)

    file_list = get_file_list()
    return render_template('files.html', files=file_list)


#登陆后进入的功能页面
@app.route('/home')
def home():
    if 'logged_in' not in session :
        return redirect(url_for('index'))
    return render_template('home.html')


#个人中心页面
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    if 'logged_in' not in session :
        return redirect(url_for('index'))
    else:

        user = users_data.get(username)

        if request.method == 'POST':
            new_password = request.form.get('new_password')

            if new_password:
                # 更新用户密码
                user['password_hash'] = new_password
                flash('密码修改成功', 'success')

        return render_template('profile.html', user=user)


#AI功能使用页面
@app.route('/ai',methods=['GET','POST'])
def ai():
    if 'logged_in' not in session :
        return redirect(url_for('index'))
    else:
            Input = request.form.get('user_message', '你好')
            documentLoader = DocumentLoader()
            File = './uploads/*.pdf'
            if check_pdf_files_pdf('./uploads'):
                doc = documentLoader.pdf(File)
                sp = documentLoader.split(doc)
                vecdb = VECDB(sp, embedding)
                resultf = vecdb.search(Input)
            else:
                resultf = ''
            File = './uploads/*.md'
            if check_pdf_files_md('./uploads'):
                doc = documentLoader.md(File)
                sp = documentLoader.split(doc)
                vecdb = VECDB(sp, embedding)
                results = vecdb.search(Input)
            else:
                results = ''
            File = './uploads/*.txt'
            if check_pdf_files_txt('./uploads'):
                doc = documentLoader.txt(File)
                sp = documentLoader.split(doc)
                vecdb = VECDB(sp, embedding)
                resultt = vecdb.search(Input)
            else:
                resultt = ''
            result = str(resultf)+str(results)+str(resultt)
            prompt="已知条件："+str(result)+"问题需求："+str(Input)
            question = checklen(getText("user", prompt))
            SparkApi.answer = ""
            #print("星火:", end="")
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            getText("assistant", SparkApi.answer)
            answer = str(text[-1]['content'])
            #print(text)
            # 将用户和机器人的消息添加到聊天记录中
            chat_history.append(f"用户: {Input}")
            chat_history.append(f"机器人: {answer}")

    return render_template('ai.html',messages=chat_history)


#使用文档页面
@app.route('/docs')
def docs():
    return render_template('docs.html')


#联系我们页面
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
