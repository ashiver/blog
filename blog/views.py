from flask import render_template, request, redirect, url_for, flash
import mistune
from flask.ext.login import login_user, login_required, current_user, logout_user
from flask.ext.mail import Message
from werkzeug.security import check_password_hash, generate_password_hash


from blog import app
from .database import session
from .models import Post, User, Comment


@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Post).count()
    
    start = page_index * paginate_by
    end = start + paginate_by
    
    total_pages = (count -1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0
    
    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]
    
    comments = session.query(Comment)
    comments = comments.order_by(Comment.datetime.asc())
    comments = comments[start:end]
    
    for post in posts:
        post.comment_num = 0
        for comment in comments:
            if comment.post_id == post.id:
                post.comment_num += 1 
        
    user = current_user
    
    return render_template("posts.html",
                          posts=posts,
                          has_next=has_next,
                          has_prev=has_prev,
                          page=page,
                          total_pages=total_pages,
                          user=user,
                          comments=comments
                          )




@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    if current_user.id != 1:
        flash("Sorry, you aren't authorized to add posts.", "danger")
        return redirect(url_for("posts"))
    else:
        return render_template("add_post.html")




@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    if current_user.id != 1:
        flash("Sorry, you aren't authorized to add posts.", "danger")
        return redirect(url_for("posts"))
    else:
        post = Post(
            title=request.form["title"],
            content=mistune.markdown(request.form["content"]),
            author=current_user
        )
        session.add(post)
        session.commit()
        return redirect(url_for("posts"))





@app.route("/post/<id>", methods=["GET"])
def post_id_get(id):
    post = session.query(Post).get(id)
    user = current_user
    
    comments = session.query(Comment)
    comments = comments.order_by(Comment.datetime.asc())
    
    post.comment_num = 0
    
    for comment in comments:
        if comment.post_id == post.id:
            post.comment_num += 1
    
    return render_template("view_post.html",
                          post=post,
                          user=user,
                          comments=comments
                          )


@app.route("/post/<id>", methods=["POST"])
@login_required
def post_id_postcomment(id):
    comment = Comment(
        post=session.query(Post).get(id),
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(comment)
    session.commit()
    
    message = Message("A comment was posted on AnthonyDevBlog",
                  sender="anthony.lee.shiver@gmail.com",
                  recipients=["anthony@anthonyshiver.com"])
    
    mail.send(message)
    flash("Your comment posted successfully", "info")
    return redirect(url_for("posts") + "post/" + str(id))



@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    user = current_user
    post = session.query(Post).get(id)
    if user.id == post.author_id:
        return render_template("edit_post.html",
                          post=post
                          )
    else:
        flash("Cannot modify other users' posts", "danger")
        return redirect(url_for("posts"))

@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post = session.query(Post).get(id)
    post.title = request.form["title"],
    post.content = content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))


@app.route("/comment/<id>/edit", methods=["GET"])
@login_required
def edit_comment_get(id):
    user = current_user
    comment = session.query(Comment).get(id)
    if user.id == comment.author_id or user.id == 1:
        return render_template("edit_comment.html",
                          comment=comment  
                          )
    else:
        flash("Cannot modify other users' comments", "danger")
        return redirect(url_for("posts"))
    
@app.route("/comment/<id>/edit", methods=["POST"])
@login_required
def edit_comment_post(id):
    comment = session.query(Comment).get(id)
    comment.content = content=mistune.markdown(request.form["content"])
    session.commit()
    flash("You successfully edited your comment.", "info")
    return redirect(url_for("posts"))



@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post_get(id):
    user = current_user
    post = session.query(Post).get(id)
    if user.id == post.author_id or post.author_id == None:
        return render_template("delete_post.html",
                          post=post
                          )
    else:
        flash("Cannot modify other users' posts", "danger")
        return redirect(url_for("posts"))




@app.route("/post/<id>/delete", methods=["POST"])
@login_required
def delete_post_delete(id):
    post = session.query(Post).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/comment/<id>/delete", methods=["GET"])
@login_required
def delete_comment_get(id):
    user = current_user
    comment = session.query(Comment).get(id)
    if user.id == comment.author_id or user.id == 1:
        return render_template("delete_comment.html",
                          comment=comment
                          )
    else:
        flash("Cannot modify other users' comments", "danger")
        return redirect(url_for("posts"))

    
@app.route("/comment/<id>/delete", methods=["POST"])
@login_required
def delete_comment_delete(id):
    comment = session.query(Comment).get(id)
    session.delete(comment)
    session.commit()
    flash("You successfully deleted your comment.", "info")
    return redirect(url_for("posts") + "post/" + str(comment.post_id))





@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")





@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    flash("You are now logged in.", "info")
    return redirect(request.args.get('next') or url_for("posts"))




@app.route("/logout", methods=["GET"])
def logout_get():
    return render_template("logout.html")



@app.route("/logout", methods=["POST"])
def logout_post():
    logout_user()
    flash("You are now logged out. Log in again to post or edit comments.", "info")
    return redirect(url_for("posts"))




@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")




@app.route("/signup", methods=["POST"])
def signup_post():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    password_2=request.form["repassword"]
    
    if session.query(User).filter_by(email=email).first():
        flash("User with that email address already exists", "danger")
        return redirect(url_for("signup_get"))
        
    if not (password and password_2) or password != password_2:
        flash("Passwords did not match", "danger")
        return redirect(url_for("signup_get"))
    
    user = User(name=name, email=email, password=generate_password_hash(password))
    
    session.add(user)
    session.commit()
    login_user(user)
    flash("Success! You may now login and start commenting", "info")
    return redirect(url_for("posts"))