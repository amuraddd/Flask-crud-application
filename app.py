from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 backslashes are relative reference 4 are absolute
db = SQLAlchemy(app)

#create a database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#notes on decorators: https://realpython.com/primer-on-python-decorators/
@app.route('/', methods=['POST', 'GET']) #define methods to receive and send data
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        #using the db model set up above
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') #redirect back to the index page
        except:
            return 'There was an issue.'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #query the db and grab all records, order by date created and return all
        return render_template('index.html', tasks=tasks) #since we defined the directory above we don't need to specify the whole path here

#delete functionality
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

#Update functionality
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task."
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True, port=5000) #setting debug=True will pop errors on the screen
