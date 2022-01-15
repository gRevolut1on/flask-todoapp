from datetime import datetime
from flask import Flask, render_template, request, redirect
from models import UserModel, Todo, db, login
from flask_login import login_required, current_user, login_user, logout_user

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
app.secret_key="LOREM IPSUM"

db.init_app(app)
login.init_app(app)

login.login_view= 'login'

@app.before_first_request
def create_table():
    db.create_all()

#USER MANAGEMENT
@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    
    if request.method== 'POST':
        email= request.form['email']
        user= UserModel.query.filter_by(email= email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')

    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email= request.form['email']
        username= request.form['username']
        password= request.form['password']

        if UserModel.query.filter_by(email=email).first():
            return ('Email already in use')

        if UserModel.query.filter_by(username= username).first():
            return ('Username already in use')

        user= UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/profile') #placeholder for now-change later
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

#APPLICATION PROPER
@app.route('/',methods=['POST','GET'])
@login_required
def index():
    if request.method=='POST':
        task_content= request.form['content']
        new_task= Todo(content=task_content)
        new_task.user= current_user

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR!'
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        tasks_pending= []
        tasks_finished= []
        for task in tasks:
            if(task.is_finished):
                tasks_finished.append(task)
            else:
                tasks_pending.append(task)
        return render_template('index.html', tasks_finished= tasks_finished, tasks_pending=tasks_pending)

@app.route('/finish/<int:id>')
@login_required
def finish(id):
    task_to_finish= Todo.query.get_or_404(id)
    task_to_finish.date_finished= datetime.utcnow()
    task_to_finish.is_finished= True

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR!'

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete= Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR!'

@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
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