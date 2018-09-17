from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import  User,Blog,Comment
from .forms import CommentForm,UpdateProfile,AddBlog,PostForm
from .. import db,photos
from . import main
import markdown2


@main.route('/')
def index():
    return render_template('index.html',title='tasha')

@main.route('/bloged/comment/<int:id>', methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    blog = Blog.get_blog(id)
    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comment(blog_id=id, comment_content=comment, user_id=current_user.id)
        new_comment.save_comment()
    comment = Comment.get_comments(id)

    return render_template('new_comment.html', comment_form=form, blog=blog, comment=comment)

@main.route('/bloged', methods=['GET', 'POST'])
def post():
    form = AddBlog()
    if form.validate_on_submit():
        new_blog = Blog(blog_content=form.blog.data,blog_category=form.category.data)
        db.session.add(new_blog)
        db.session.commit()
    blog=Blog.query.all()
    return render_template('bloged.html',form=form, blog=blog)

@main.route('/Fashion', methods=['GET', 'POST'])
def fashion():
    fashion = Blog.query.filter_by(blog_category="fashion").all()
    print(fashion)
    return render_template('fashion.html', blog=fashion)
@main.route('/Political', methods=['GET', 'POST'])
def political():
    political = Blog.query.filter_by(blog_category="political").all()
    print(political)
    return render_template('political.html', blog=political)
@main.route('/Vehicle', methods=['GET', 'POST'])
def vehicle():
    vehicle = Blog.query.filter_by(Blog_category="vehicle").all()
    print(vehicle)
    return render_template('vehicle.html', blog=vehicle)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():

        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST','GET'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.update_profile',uname=uname))
@main.route('/writer/dashboard', methods=['GET','POST'])
@login_required
def writer_dashboard():
   Blog_form = BlogForm()
   form_comment = CommentForm()
   if post_form.validate_on_submit():
       user = current_user
       new_post = Post(title = post_form.title.data,post_content=post_form.post.data,category = post_form.category.data,user = user)
       db.session.add(new_post)
       db.session.commit()
       return redirect(url_for('main.writer_dashboard',PostForm=post_form,form_comment=form_comment))
   posts = Post.query.all()
   return render_template('dashboard.html',PostForm=post_form,type='post',posts=posts,form_comment=form_comment)