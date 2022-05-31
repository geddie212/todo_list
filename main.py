from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(500), unique=True, nullable=False)
    completed = db.Column(db.Boolean(), nullable=False)


@app.route('/finish_task/<int:task_id>')
def finish_task(task_id):
    Task.query.filter_by(id=task_id).update({'completed': True})
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
        db.session.add(Task(task=task, completed=False))
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/')
def home():
    all_tasks = Task.query.all()
    return render_template('index.html', tasks=all_tasks)


if __name__ == "__main__":
    app.run(debug=True)
