from . import admin
from .. import db
from ..models import Admin, Article, Category, User, Comment, Reply
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..some_func import ch_content


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        admin = Admin.query.filter_by(name=request.form['username']).first()
        if admin is not None and admin.password == str(request.form['password']):
            login_user(admin)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('请输入正确的用户名或密码')
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

@admin.route('/index')
@login_required
def index():
    articles = len(Article.query.all())
    comments = len(Comment.query.all()) + len(Reply.query.all())
    users = len(User.query.all())
    return render_template('admin/index.html', articles=articles, comments=comments, users=users)

@admin.route('/article')
@login_required
def article():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.created_time.desc()).paginate(
        page, per_page=15)
    articles = pagination.items
    return render_template('admin/article.html', articles=articles, pagination=pagination, idx='.article')

@admin.route('/add/article', methods=['GET', 'POST'])
@login_required
def add_article():
    categorys = Category.query.all()
    if request.method == "POST" and request.form['title'] and request.form['content'] != '':
        new_article = Article(title=request.form['title'], content=request.form['content'].replace('class=""','class="img-responsive center-block"'), abstract=ch_content(request.form['content'])[:137]+'...',
                              category_id=request.form['category'])
        db.session.add(new_article)
        return redirect(url_for('admin.article'))
    return render_template('admin/addarticle.html', categorys=categorys)

@admin.route('/edit/article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    categorys = Category.query.all()
    article = Article.query.get_or_404(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.content = request.form['content'].replace('class=""','class="img-responsive center-block"')
        article.abstract = ch_content(request.form['content'])[:137]+'...'
        article.category_id = request.form['category']
        db.session.add(article)
        return redirect(url_for('admin.article'))
    return render_template('admin/editearticle.html', categorys=categorys, article=article)

@admin.route('/delete/article/<int:id>')
@login_required
def del_article(id):
    article = Article.query.get_or_404(id)
    article_comments = Comment.query.filter_by(article_id=id).all()
    for each_comment in article_comments:
        comment_replys = Reply.query.filter_by(comment_id=each_comment.id).all()
        for each_reply in comment_replys:
            db.session.delete(each_reply)
        db.session.delete(each_comment)
    db.session.delete(article)
    return redirect(url_for('admin.article'))

@admin.route('/article/<int:id>/comments')
@login_required
def article_comments(id):
    title = Article.query.get_or_404(id).title
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(article_id=id).paginate(
        page, per_page=10)
    comments = pagination.items
    return render_template('admin/comment.html', comments=comments, title=title, pagination=pagination, idx='.article_comments', id=id)

@admin.route('/shield/comment/<int:id>')
@login_required
def shield_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.status = False
    db.session.add(comment)
    article = Article.query.filter_by(id=comment.article_id).first()
    title = article.title
    id = article.id
    comments = Comment.query.filter_by(article_id=comment.article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=id))

@admin.route('/unshield/comment/<int:id>')
@login_required
def unshield_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.status = True
    db.session.add(comment)
    article = Article.query.filter_by(id=comment.article_id).first()
    title = article.title
    id = article.id
    comments = Comment.query.filter_by(article_id=comment.article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=id))

@admin.route('/shield/reply/<int:id>')
@login_required
def shield_reply(id):
    reply = Reply.query.get_or_404(id)
    reply.status = False
    db.session.add(reply)
    article_id = Comment.query.filter_by(id=reply.comment_id).first().article_id
    title = Article.query.filter_by(id=article_id).first().title
    comments = Comment.query.filter_by(article_id=article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=article_id))

@admin.route('/unshield/reply/<int:id>')
@login_required
def unshield_reply(id):
    reply = Reply.query.get_or_404(id)
    reply.status = True
    db.session.add(reply)
    article_id = Comment.query.filter_by(id=reply.comment_id).first().article_id
    title = Article.query.filter_by(id=article_id).first().title
    comments = Comment.query.filter_by(article_id=article_id).all()
    return redirect(url_for('admin.article_comments', title=title, comments=comments, id=article_id))


@admin.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == 'POST' and request.form['category']:
        new_category = Category(name=request.form['category'])
        db.session.add(new_category)
        return redirect(url_for('admin.category'))
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(Category.id).paginate(
        page, per_page=15)
    categorys = pagination.items
    return render_template('admin/category.html', categorys=categorys, pagination=pagination, idx='.category')

@admin.route('/delete/category/<int:id>')
@login_required
def del_category(id):
    category = Category.query.get_or_404(id)
    if category.name != '其它':
        db.session.delete(category)
        return redirect(url_for('admin.category'))

@admin.route('/user')
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page, per_page=20)
    users = pagination.items
    return render_template('admin/user.html', users=users, pagination=pagination, idx='.user')