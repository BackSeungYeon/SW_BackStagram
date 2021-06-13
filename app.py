from DB_handler import DBModule
from flask import Flask, redirect, render_template, url_for, request, flash, session

app = Flask(__name__)
app.secret_key="sdfsdfvklkjwekng"
DB = DBModule()

@app.route("/")
def index():
    if "uid" in session:
        user = session["uid"]
    else:
        user="Login"
    return render_template("index.html", user=user)
    post_lists = DB.post_list()
    return redirect(url_for(post_list))

@app.route("/list")
def post_list():
    post_list = DB.post_list()
    if "uid" in session:
        user = session["uid"]
    else:
        user="Login"
    if post_list==None:
        length = 0
    else:
        length = len(post_list)
    return render_template("post_list.html", post_list=post_list.items(), length=length)

@app.route("/post/<string:pid>")
def post(pid):
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    post, post_id = DB.post_detail(pid)
    return render_template("post_detail.html", post=post, post_id=post_id, user=user)

@app.route("/logout")
def logout():
    if "uid" in session:
        session.pop("uid")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/login")
def login():
    if "uid" in session:
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/login_done",methods=["get"])
def login_done():
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.login(uid, pwd):
        session["uid"] = uid
        return redirect(url_for("index"))
    else:
        flash("아이디나 비밀번호가 틀립니다.")
        return redirect(url_for("login"))


@app.route("/signin")
def signin():
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    return render_template("signin.html", user=user)

@app.route("/signin_done", methods=["get"])
def signin_done():
    email = request.args.get("email")
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    name = request.args.get("name")
    if DB.signin(email=email, _id_=uid,pwd= pwd,name= name):
        return redirect(url_for("index"))
    else:
        flash("이미 등록된 아이디 입니다.")
        return redirect(url_for("signin"))


# @app.route("/user/<uid>")
# def user(uid):
#     pass

@app.route("/write")
def write():
    if "uid" in session:
        return render_template("write_post.html")
    else:
        return redirect(url_for("login"))

@app.route("/write_done", methods=["get"])
def write_done():
    title=request.args.get("title")
    contents=request.args.get("contents")
    uid = session.get("uid")
    DB.write_post(title,contents,uid)
    return redirect(url_for("index"))

@app.route("/user/<string:uid>")
def user_posts(uid):
    u_post = DB.get_user(uid)
    if u_post==None:
        length = 0
    else:
        length = len(u_post)
    return render_template("user_detail.html", post_list=u_post, length=length, uid=uid)

@app.route("/edit_post/<string:pid>")
def edit_post(pid):
    if "uid" in session:
        user = session["uid"]
    else:
        user = "Login"
    post, post_id = DB.post_detail(pid)
    if user == post["uid"]:
        return render_template("edit_post.html", post=post, post_id=post_id, user=user)
    else:
        return redirect(url_for("post", pid=post_id))

@app.route("/edit_done/<string:pid>", methods=["get"])
def edit_done(pid):
    title = request.args.get("title")
    contents = request.args.get("contents")
    DB.edit_post(title,contents,pid)
    return redirect(url_for("post_list"))

@app.route("/delete_post/<string:pid>")
def delete_post(pid):
    post, post_id = DB.post_detail(pid)
    if session["uid"] == post["uid"]:
        DB.delete_post(pid)
        return redirect(url_for("post_list"))
    else:
        return redirect(url_for("post", pid=pid))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)