from flask import Flask, render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mytodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()
class mytodo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    todo_time= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"
@app.route("/", methods= ["GET","POST"])
def home_page():
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo= mytodo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo= mytodo.query.all()
    return  render_template("index.html" , alltodo=alltodo)
@app.route("/update/<int:sno>", methods=["GET","POST"]) 
def update(sno ):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = mytodo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = mytodo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)
@app.route("/delete/<int:sno>") 
def delete_todo(sno):
    todo = mytodo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
# @app.route("/addtodo")
# def addtodo():
#     return render_template("addtodo.html")
# @app.route("/aboutus")
# def aboutus():
#     return render_template("aboutus.html")
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")
# @app.route("/todo")
# def todos():
#     return render_template("todos.html")
if  __name__=="__main__":
    app.run(debug=True)