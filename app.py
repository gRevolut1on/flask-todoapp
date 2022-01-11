from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import Todo, db

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content= request.form['content']
        new_task= Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR!'
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR!'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task= Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content= request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR!'
    else:
        return render_template('update.html',task=task)

if __name__=="__main__":
    app.run(debug=True)