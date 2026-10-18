from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired,URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)


class TaskForm(FlaskForm):
    task=StringField("To Do :",validators=[DataRequired()])

    submit=SubmitField("Submit")

class ToDoTask(db.Model):
    __tablename__="task"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    task:Mapped[str]=mapped_column(String(100))
    is_task_complete:Mapped[bool]=mapped_column(Boolean,default=False)




@app.route("/")
def home():
    tasks=db.session.execute(db.select(ToDoTask)).scalars().all()
    return render_template("index.html",tasks=tasks)

@app.route("/add",methods=["GET","POST"])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task=ToDoTask(
            task=form.task.data,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html",form=form)


@app.route("/done/<int:task_id>")
def done(task_id):
    task = db.get_or_404(ToDoTask, task_id)
    task.is_task_complete=not bool(task.is_task_complete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit/<int:task_id>",methods=["GET","POST"])
def edit(task_id):
    task = db.get_or_404(ToDoTask, task_id)
    form=TaskForm()
    if request.method == "GET":
        form.task.data=task.task
    if form.validate_on_submit():
        task.task=form.task.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html",form=form)


@app.route("/delete/<int:task_id>")
def delete(task_id):
    task_to_delete=db.get_or_404(ToDoTask,task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

# with app.app_context():
#     db.create_all()

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    app.run(debug=True)

