from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/notepad", methods=["GET", "POST"])
def notepad():
    #return render_template("notepad.html")
    if request.method == "POST":
        current_task = request.form
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f'ERROR{e}')
            return f'ERROR{e}'
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("notepad.html", tasks=tasks)

@app.route("/learnMore")
def learnMore():
    return render_template("learnmore.html")

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:
        return f'Task {self.id}'





if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)




