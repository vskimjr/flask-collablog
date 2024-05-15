"""Collablog application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///collablog')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sUp37$EcREtK3Y-c0lL@bLOG'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.get('/')
def root():
    """Homepage redirects to list of users"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Display 404 NOT FOUND page"""

    return render_template("404.html"), 404


################################################################################
# Users Route
################################################################################

@app.get('/users')
def users_index():
    """Displays page with information on all Collablog users"""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users/users_index.html', users=users)


@app.get('/users/new')
def users_new():
    """Displays page with form to create a new Collablog user"""

    return render_template('users/new_user.html')


@app.post('/users/new')
def users_new_submit():
    """Handles form submission for creating a new Collablog user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None,
        about=request.form['about'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {new_user.first_name} added")

    return redirect("/users")


@app.get('/users/<int:user_id>')
def users_display_user(user_id):
    """Displays page for specific user information"""

    user = User.query.get_or_404(user_id)

    return render_template('users/user_profile.html', user=user)


@app.get('/users/<int:user_id>/edit')
def users_edit_user(user_id):
    """Displays edit page for specific user"""

    user = User.query.get_or_404(user_id)

    return render_template('users/edit_user.html', user=user)


@app.post('/users/<int:user_id>/edit')
def users_edit_user_submit(user_id):
    """Handles user edit form submission, returns user to their page"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    user.about = request.form['about']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect(f'/users/{user_id}')


@app.post('/users/<int:user_id>/delete')
def users_delete_user(user_id):
    """Handles user edit form delete submission, returns user to /users page"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    for post in posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users")


################################################################################
# Posts Route
################################################################################

@app.get('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Displays a form to create a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts/new_post.html', user=user, tags=tags)


@app.post('/users/<int:user_id>/posts/new')
def posts_add_post(user_id):
    """Handles form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form['post_title'],
        content=request.form['post_content'],
        blurb=request.form['post_blurb'],
        user=user,
        tags=tags
    )

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post {new_post.title} added!")

    return redirect(f"/users/{user_id}")


@app.get('/posts/<int:post_id>')
def posts_display_post(post_id):
    """Displays a page with a specific post"""

    post = Post.query.get_or_404(post_id)

    return render_template('posts/display_post.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def posts_edit_post(post_id):
    """Displays edit page for specific user"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('posts/edit_post.html', post=post, tags=tags)


@app.post('/posts/<int:post_id>/edit')
def posts_edit_post_submit(post_id):
    """Handles post edit form submission, returns user to the edited post page"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.blurb = request.form['blurb']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"{post.title} edited.")

    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def posts_delete_post(post_id):
    """Handles post delete submission from edit form, returns user to user's
    profile page"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


################################################################################
# Tags Route
################################################################################

@app.get('/tags')
def tags_index():
    """Displays a page with all avaiilable tags"""

    tags = Tag.query.all()
    return render_template('tags/tags_index.html', tags=tags)


@app.get('/tags/<int:tag_id>')
def tags_display_tag(tag_id):
    """Displays a page with information on a tag and posts with that tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/tag_page.html', tag=tag)


@app.get('/tags/new')
def tags_new_form():
    """Displays a form to create a new tag"""

    return render_template('tags/new_tag.html')


@app.post('/tags/new')
def tags_add_tag():
    """Handles form submission for creating a new tag"""

    new_tag  = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag {new_tag.name} added")

    return redirect("/tags")

@app.get('/tags/<int:tag_id>/edit')
def tags_edit_tag_form(tag_id):
    """Displays a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/edit_tag.html', tag=tag)

@app.post('/tags/<int:tag_id>/edit')
def tags_edit_tag(tag_id):
    """Handles tag edit submission, returns user to the tag page"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    db.session.add(tag)
    db.session.commit()
    flash(f"{tag.name} edited.")

    return redirect(f'/tags/{tag_id}')

@app.post('/tags/<int:tag_id>/delete')
def tags_delete_tag(tag_id):
    """Handles tag delete submission from edit form, returns user to tags
    index page"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")