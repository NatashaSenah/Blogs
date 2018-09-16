from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import  User,Blog,Comment
from .forms import CommentForm,UpdateProfile,AddPitch
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

# @main.route('/pick', methods=['GET', 'POST'])
# def pickup():
#     pickup = Pitch.query.filter_by(pitch_category="pick-up-lines").all()
#     print(pickup)
#     return render_template('pickup.html', pitch=pickup)
# @main.route('/Interview', methods=['GET', 'POST'])
# def interview():
#     interview = Pitch.query.filter_by(pitch_category="interview").all()
#     print(interview)
#     return render_template('interview.html', pitch=interview)
# @main.route('/Product', methods=['GET', 'POST'])
# def product():
#     product = Pitch.query.filter_by(pitch_category="product").all()
#     print(product)
#     return render_template('product.html', pitch=product)

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
