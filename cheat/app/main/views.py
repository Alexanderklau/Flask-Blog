from flask import render_template,flash,redirect,url_for
from . import main
from ..models import *
from flask import abort
from flask_login import login_user, logout_user, login_required, \
    current_user
from .forms import EditProfileForm
@main.route('/')
def index():
    return render_template('index.html')
@main.route('/user/<username>')
def user(username):
    user = User.quert.fileter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html',user=user)
@main.route('/edit-profile',method = ['GET','POST'])
@login_manager
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.about_me = current_user.about_me
    form.location.data = current_user.location
    return render_template('edit_profile.html',form=form)