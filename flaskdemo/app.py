from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////test.db'
db = SQLAlchemy(app)
import json
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    data_created = db.Column(db.DateTime,default=datetime.utcnow())
    def __repr__(self):
        return '<Task %i>' % self.id


@app.route('/',methods=['POST','GET'])
def index():
    # return 'Fuck World!'
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return  " THis is Error"
    else:
        return render_template('index.html')

    return render_template("index.html")

@app.route('/f',methods=['POST'])
def login():
    data = request.get_data()
    data = json.loads(data)
    username = data['username']
    password = data['password']

    return  json({"login": (username, password)})

@app.route('/b',methods=['POST','get'])
def send():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)

        result = json_data.get("password")
        # result = picture_recognition(img_url)
        _dickt ={}
        _dickt['Me'] = result
        _dickt['You'] = 'dick'
        # print(json.dumps(result))
        print(json.dumps(_dickt))
        return json.dumps(_dickt)


@app.route('/bb',methods=['POST','get'])
def send1():
    if request.method == 'POST':
        data = request.get_data()
        # print(data)
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)

        result = json_data.get("username")
        print("result: "+ result)
        # result = picture_recognition(img_url)
        _dickt ={}
        _dickt['Me'] = result
        _dickt['You'] = 'dick'
        # print(json.dumps(result))
        # print(json.dumps(_dickt))
        return json.dumps(_dickt)

#sudo pip3 download -r requiere.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5000)
