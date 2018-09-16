from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,RadioField
from wtforms.validators import Required

class CommentForm(FlaskForm):
 comment = TextAreaField('Comment title')

 submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class AddBlog(FlaskForm):
    blog = TextAreaField('Write your blog',validators =[Required()])
    category = RadioField('Pick Category',
                            choices=[('interview', 'interview'),
                                  ('product', 'product'),
                                     ('pick-up-lines', 'pick-up-lines')],
                            validators=[Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
   category = StringField('Blog category',validators=[Required()])
   content = TextAreaField(Blog, validators=[Required()])

   submit = SubmitField('Submit')