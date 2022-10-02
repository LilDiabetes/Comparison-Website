from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm
from src.models.user_models import User, BaseModel
from flask_login import login_user, login_required, logout_user, current_user

auth_blueprint = Blueprint('auth',
                           __name__,
                           template_folder='templates')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def sign_up():
    myform = RegisterForm()

    if myform.validate_on_submit():
        hashed_password = generate_password_hash(myform.password.data, method='sha256')
        register = User(username=myform.username.data, email=myform.email.data, password=hashed_password,
                        gender=myform.gender.data, age=myform.age.data,)
        register.save()

        return redirect(url_for('auth.dashboard'))
    return render_template("sign_up.html", form=myform)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def log_in():
    myform = LoginForm()

    if myform.validate_on_submit():
        user = User.query.filter_by(email=myform.email.data).first()
        if user:
            if check_password_hash(user.password, myform.password.data):
                login_user(user)
                flash(f"{user.username} logged in succesfully")
                return redirect(url_for('auth.dashboard'))
            else:
                flash("Incorrect Credentials")
        else:
            flash("User by that email does not exist")

    return render_template("log_in.html", form=myform)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    flash("Succesfully logged out")
    return redirect(url_for('auth.dashboard'))

@auth_blueprint.route('/profile_page', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = UserProfile()
    user_id = current_user.id
    name_to_update = User.query.get_or_404(user_id)
    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.about = request.form['about']

        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            pic_name = str(uuid.uuid1()) + '_' + pic_filename
            saver = request.files['profile_pic']
            name_to_update.profile_pic = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(application.config['UPLOAD_FOLDER'], pic_name))
                flash('Profile Updated')
                return render_template('profile_page.html',
                                       form=form,
                                       name_to_update=name_to_update)
            except:
                flash('Error!  Looks like there was a problem...try again!')
                return render_template("profile_page.html",
                                       form=form,
                                       name_to_update=name_to_update)
        else:
            db.session.commit()
            flash('Profile Updated')
            return render_template('profile_page.html',
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template('profile_page.html',
                               form=form,
                               name_to_update=name_to_update,
                               user_id=user_id)
    return render_template('profile_page.html')


@auth_blueprint.route('/')
def dashboard():
    return render_template("index.html")
