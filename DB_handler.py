import pyrebase
import json
import uuid


class DBModule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db=firebase.database()

    def login(self, uid, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[uid]
            if userinfo["pwd"] == pwd:
                return True
            else:
                return False
        except:
            return False

    #
    def signin_verification(self, uid):
        users = self.db.child("users").get().val()
        for i in users:
            if uid == i:
                return False
        return True
    #
    def signin(self, _id_, pwd, name, email):
        information = {
            "pwd":pwd,
            "name":name,
            "email":email
        }
        if self.signin_verification(_id_):
            self.db.child("users").child(_id_).set(information)
            return True
        else:
            return False

    #
    def write_post(self, title, contents, uid):
        pid = str(uuid.uuid4())[:12]
        information = {
            "title":title,
            "contents":contents,
            "uid":uid
        }
        self.db.child("posts").child(pid).set(information)

    def edit_post(self, title, contents, pid):
        changed_info = {"title": title, "contents": contents}
        self.db.child("posts").child(pid).update(changed_info)

    def post_list(self):
        post_lists = self.db.child("posts").get().val()
        return post_lists
    #
    def post_detail(self, pid):
        post = self.db.child("posts").get().val()[pid]
        post_id = pid
        return post, post_id

    def delete_post(self, pid):
        self.db.child("posts").child(pid).set({})

    def get_user(self, uid):
        post_lsit = []
        users_post = self.db.child("posts").get().val()
        for post in users_post.items():
            if post[1]["uid"] == uid:
                post_lsit.append(post)
        return post_lsit
