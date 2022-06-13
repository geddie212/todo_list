from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os

SQL = os.environ.get('DATABASE_URL').split('postgres')
SQL[0] += 'postgresql'
updated_SQL = f'{SQL[0]}{SQL[1]}'

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = updated_SQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRET KEY SETUP
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)



class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), unique=True, nullable=False)
    completed = db.Column(db.Boolean(), nullable=False)
    editable = db.Column(db.Boolean(), nullable=False)


db.create_all()
db.session.commit()


@app.route('/finish_task/<int:task_id>')
def finish_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.completed:
        task.completed = False
    elif not task.completed:
        task.completed = True
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/convert_task/<int:task_id>')
def convert_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.editable = True
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    content = request.form['task']
    task = Task.query.filter_by(id=task_id).first()
    task.task = content
    task.editable = False
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    query = Task.query.filter(Task.task == task).all()
    if len(query) == 0:
        db.session.add(Task(task=task, completed=False, editable=False))
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/')
def home():
    all_tasks = Task.query.all()
    return render_template('index.html', tasks=all_tasks)


if __name__ == "__main__":
    app.run(debug=True)
