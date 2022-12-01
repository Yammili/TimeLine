from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
from werkzeug.utils import secure_filename

posts = Blueprint('posts', __name__)

UPLOAD_FOLDER = 'website/static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@posts.route('/')
def timeline():
    Post = Note.query.order_by(Note.date.desc()).all()
    return render_template('timeline.html', Post=Post, user=current_user)


@posts.route('/list')
@login_required
def list():
    if current_user.posts:
        Post = Note.query.order_by(Note.date.desc()).all()
        return render_template("list.html", Post=Post, user=current_user)
    else:
        flash('You need to publish at least one post to visit this page!', category='error')
        return redirect('/create')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['note']
        info = request.form['info']
        text = request.form['text']
        file = request.files['file']
    
        if len(title) < 1:
            flash('Title is too short!', category='error')
        elif len(info) < 2:
            flash('Intro is too short!', category='error')
        elif len(text) < 20:
            flash('The main info is too short!', category='error')
        else:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Image successfully uploaded and displayed below')
            else:
                filename = "hole.jpg"

            new_post = Note(title=title, info=info, text=text, data=filename, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')

    return render_template("create.html", user=current_user)


@posts.route('/delete-post/<int:id>')
def delete_post(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('posts.gallery'))
    except:
        return "При видаленні статі з'явилась помилка"


@posts.route('/gallery')
@login_required
def gallery():
    if current_user.posts:
        Post = Note.query.order_by(Note.date.desc()).all()
        return render_template('gallery.html', Post=Post, user=current_user)
    else:
        flash('You need to publish at least one post to visit this page!', category='error')
        return redirect('/create')

@posts.route('/post/post-id:<int:id>')
@login_required
def post(id):
    Post = Note.query.get(id)
    return render_template('post.html', Post=Post, user=current_user)