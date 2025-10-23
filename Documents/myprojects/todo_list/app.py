from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# database model
class Task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    done = db.Column(db.Boolean, default = False)
    due_date = db.Column(db.String(20))     
    priority = db.Column(db.Integer, default=1)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks)

@app.route('/add', methods = ['POST'])
def add():
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority', 1)
    if title:
        new_task = Task(title=title, due_date=due_date, priority=int(priority))
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    task= Task.query.get(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    new_title = request.form.get('title')
    if new_title:
        task.title = new_title
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)


