from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskintro.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DATETIME, default=datetime.now(pytz.utc))  # pasang sesuai timezone skrg (self aware)

    def __repr__(self):
        # returns a string everytime we added a task
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    if request.method == 'POST':
        task_content = request.form['task']
        new_todo = Todo(task=task_content)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem while adding your task!"
    else:
        tasks = Todo.query.order_by(Todo.date).all() # query untuk menampilkan seluruh task
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task!'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        to_update.task = request.form['task']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task!'
    else:
        return render_template('update.html', task=to_update)

if __name__ == '__main__':
    app.run()
