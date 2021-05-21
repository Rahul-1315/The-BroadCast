from application import app, db
from flask import render_template, url_for, request, redirect, flash, session
from application.models import User, News, Admin, Log_file
import datetime
import random


objects = list()


@app.route('/')
def home():
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False
    return render_template('base.html', name=name)


@app.route('/news')
def news():
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False
    news = News.objects.all()
    return render_template('news.html', news=True, objects=news, name=name)


@app.route('/newsform', methods=['GET', 'POST'])
def news_form():
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False

    def random_id():
        return random.randint(1000, 999999)
    if session.get('user_email') or session.get('admin_email'):
        if request.method == 'POST':
            news_id = random_id()
            if News.objects(news_id=news_id).first():
                news_id = random_id()
            headline = request.form.get('headline')
            description = request.form.get('description')
            author = request.form.get('author')
            category = request.form.get('category')
            timestamp = str(datetime.datetime.now())
            timestamp = timestamp[11:19]
            news_object = News(news_id=news_id, headline=headline, description=description,
                               author=author, category=category, timestamp=timestamp)
            news_object.save()
            if session.get('user_email'):
                email = session.get('user_email')
                new_log = Log_file(email=email, news_id=news_id)
                new_log.save()
            flash('Successfully added news', 'success')
            return redirect(url_for('home'))
        return render_template('newsform.html', name=name)
    flash('Please login first to add news', 'warning')
    return redirect(url_for('home'))


@ app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if session.get('user_email'):
        session.pop('user_email', False)
        session.pop('user_name', False)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.objects(email=email).first()
        if admin and admin.get_password(password):
            flash(admin.first_name+' You have successfully Logged In!', 'success')
            session['admin_email'] = admin.email
            session['admin_name'] = admin.first_name
            return redirect(url_for('home'))
        # print(email, password)
        else:
            flash('Email/Password Incorrect, Try Again!', 'danger')
    return render_template('login.html', user=False)


@ app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if session.get('admin_email'):
        session.pop('admin_email', False)
        session.pop('admin_name', False)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            flash(user.first_name+' You have successfully Logged In!', 'success')
            # print(email, password)
            session['user_email'] = user.email
            session['user_name'] = user.first_name
            return redirect(url_for('home'))
        else:
            flash('Email/Password Incorrect, Try Again!', 'danger')
    return render_template('login.html', user=True)


@ app.route('/admin_registration', methods=['GET', 'POST'])
def admin_registration():
    if request.method == 'POST':
        # print('Hello')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email, password)
        if Admin.objects(email=email).first():
            print('Not Saving....')
            flash('Oops! Email already existing.', 'danger')
            return redirect(url_for('admin_registration'))
        else:
            new_admin = Admin(first_name=first_name,
                              last_name=last_name, email=email)
            new_admin.set_password(password)
            new_admin.save()
            # print('Saving....')
            flash('Successfully Registered!', 'success')
            return redirect(url_for('admin_login'))
    return render_template('registration.html', user=False)


@ app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        print('Hello')
        user_id = User.objects.count()+1
        # print(user_id)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email, password, user_id)
        if User.objects(email=email).first():
            # print('Not Saving....')
            flash('Oops! Email already existing.', 'danger')
            return redirect(url_for('user_registration'))
        else:
            new_user = User(
                user_id=user_id, first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            new_user.save()
            flash('Successfully Registered!', 'success')
            return redirect(url_for('user_login'))
    print('Starting')
    return render_template('registration.html', user=True)


@app.route('/contactus')
def contactus():
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False
    return render_template('contactus.html', name=name)


@app.route('/logFile')
def log_file():
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False
    if session.get('admin_email'):
        users = list(User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'log_file',
                    'localField': 'email',
                    'foreignField': 'email',
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'news',
                    'localField': 'r1.news_id',
                    'foreignField': 'news_id',
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2',
                    'preserveNullAndEmptyArrays': False
                }
            }
        ]))

        return render_template('logFile.html', users=users, name=name)
    else:
        flash('Sorry, your not authorized for this request!', 'warning')
        return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
def delete_news():
    if request.method == 'POST':
        news_id = request.form.get('news_id')
        News.objects(news_id=news_id).delete()
        flash('Successfully deleted!', 'success')
        return redirect(url_for('log_file'))
    else:
        flash("There was a problem while deleting, Try again!", 'danger')
        return redirect(url_for('log_file'))


@app.route('/update/<int:news_id>', methods=['GET', 'POST'])
def update_news(news_id):
    if session.get('user_email'):
        name = session.get('user_name')
    elif session.get('admin_email'):
        name = session.get('admin_name')
    else:
        name = False
    news = News.objects(news_id=news_id).first()
    if request.method == 'POST':
        headline = request.form.get('headline')
        if News.objects(news_id=news.news_id).update(headline=headline):
            flash('Successfully updated!', 'success')
            return redirect(url_for('log_file'))
        else:
            flash("There was a problem while updating, Try again!", 'danger')
            return redirect(url_for('log_file'))
    return render_template('newsformupdate.html', news=news, name=name)


@app.route('/logout')
def logout():
    if session.get('admin_email'):
        session.pop('admin_email', False)
        session.pop('admin_name', False)
        return redirect(url_for('home'))
    if session.get('user_email'):
        session.pop('user_email', False)
        session.pop('user_name', False)
        return redirect(url_for('home'))
