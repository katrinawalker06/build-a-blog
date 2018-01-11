from flask import Flask,request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app= Flask(__name__)
app.config['DEBUG']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db=SQLAlchemy(app)

class Blog (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(1500))

    def __init__(self,title,body):
        self.title=title
        self.body=body



@app.route("/blog",methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template("/main.html",blogs=blogs)


@app.route("/newpost",methods=['POST', 'GET'])
def home():
    blogtitle_error=""
    newblog_error=""
    blogtitle=request.form['blogtitle']
    newblog=request.form['newblog']
    
    if request.method == "POST":
        return render_template('/base.html', blogtitle=blogtitle,newblog=newblog)
    else:
        if blogtitle == "":
            blogtitle_error = "enter title"

        if newblog == "":
            newblog_error = "enter blog"

        if blogtitle_error != "" or newblog_error != "" :
            return render_template('/base.html',blogtitle_error=blogtitle_error, newblog_error=newblog_error, blogtitle=blogtitle,newblog=newblog)
        else:
            new_blog = Blog(blogtitle, newblog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog={0}".format(title.id))
      
@app.route("/")
def root():
    return render_template ('/base.html')


@app.route("/detail", methods=["GET"])
def blogpostnew():
    blogspot= Blog.query.get("title.id")
    blog_post=request.args.get("blog")
    return render_template("/blog.html",blog=blog_post,title=title)


if __name__=='__main__':
    app.run()
