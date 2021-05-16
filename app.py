from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# create DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self,id,content,completed,dateCreated):
    #     self.id = id
    #     self.content = content
    #     self.completed = completed
    #     self.dateCreated = dateCreated
    
    def __repr__(self):
        return "<Task %r>" % self.id    

@app.route("/", methods=["POST", "GET"])

def index(): 
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except: 
            return "Cannot post the new message!!!"

    else:
        tasks = Todo.query.order_by(Todo.dateCreated).all()
        return render_template("index.html", tasks=tasks)


#delete Route
@app.route("/delete/<id>")

#delete function
def delete(id):
    delete_task = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    
    except: 
        return "There was an Error when deleting the Task"
    
#Update Task Function
@app.route("/update/<id>", methods=["POST","GET"])

def update(id):
    update_task = Todo.query.get_or_404(id)

    if request.method == "POST":
        update = request.form["update"]   
        update_task.content = update   #update the content prop of the update_task obj
        try:
            db.session.commit()    #remember to commit whenever you change anything in the db.          
            return redirect("/")
        except: 
            return "Cannot update the task!!!"
    else:
        return render_template("update.html", task=update_task)


if __name__ == "__main__":
    app.run(debug=True)
