import os
from . import main
from .. import db
from ..models import Article, Category, User, Comment, Reply
from flask import render_template, redirect, url_for, request, session, Response, current_app
from qiniu import Auth, put_file
from ..some_func import oauthmethod

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.created_time.desc()).paginate(
        page, per_page=10)
    articles = pagination.items
    return render_template('index.html', articles=articles, pagination=pagination, idx='.index')

#登录页面
@main.route('/login')
def login():
    session['return_id'] = request.args.get('return_id')
    session['return_type'] = request.args.get('return_type')
    return render_template('login.html')

#github第三方登录
@main.route('/github/login')
def github_login():
    path = oauthmethod.git_path()
    if session.get('return_type'):
        return redirect(path)
    else:
        session['return_id'] = request.args.get('return_id')
        session['return_type'] = request.args.get('return_type')
    return redirect(path)

#github第三方回调地址处理
@main.route('/github/oauth/callback')
def github_oauth():
    # 判断回调地址中是否拿到code
    if 'code' not in request.args:
        return redirect(url_for('main.login'))
    code = request.args.get('code')
    result = oauthmethod.git_userinfo(code)

    username = result['login']
    avatar_url = result['avatar_url'].split('?')[0]

    #判断用户是否在USER表中是否注册，没有则注册后给到登录SESSION，有则直接给道登录SESSION
    user = User.query.filter_by(username=username).filter_by(social_type='github').first()
    #如果用户已经注册
    if user:
        session['login'] = user.id
        return_type = session.get('return_type')
        return_id = session.get('return_id')
        if return_type:
            del session['return_type'], session['return_id']
            if return_type == 'comment':
                return redirect(url_for('main.reply_comment', id=return_id))
            elif return_type == 'reply':
                return redirect(url_for('main.reply_reply', id=return_id))
            else:
                return redirect(url_for('main.article', id=return_id))
        else:
            return redirect(url_for('main.index'))
    user = User(username=username, avatar_url=avatar_url, social_type='github')
    db.session.add(user)
    session['login'] = User.query.filter_by(username=username).filter_by(social_type='github').first().id
    return_type = session.get('return_type')
    return_id = session.get('return_id')
    if return_type:
        del session['return_type'], session['return_id']
        if return_type == 'comment':
            return redirect(url_for('main.reply_comment', id=return_id))
        elif return_type == 'reply':
            return redirect(url_for('main.reply_reply', id=return_id))
        else:
            return redirect(url_for('main.article', id=return_id))
    else:
        return redirect(url_for('main.index'))

#微博第三方登录
@main.route('/weibo/login')
def weibo_login():
    path = oauthmethod.weibo_path()
    if session.get('return_type'):
        return redirect(path)
    else:
        session['return_id'] = request.args.get('return_id')
        session['return_type'] = request.args.get('return_type')
    return redirect(path)

#微博第三方回调地址处理
@main.route('/weibo/oauth/callback')
def weibo_oauth():
    # 判断回调地址中是否拿到code
    if 'code' not in request.args:
        return redirect(url_for('main.login'))
    code = request.args.get('code')
    result = oauthmethod.weibo_userinfo(code)

    username = result['name']
    avatar_url = result['profile_image_url']

    # 判断用户是否在USER表中是否注册，没有则注册后给到登录SESSION，有则直接给道登录SESSION
    user = User.query.filter_by(username=username).filter_by(social_type='weibo').first()
    # 如果用户已经注册
    if user:
        session['login'] = user.id
        return_type = session.get('return_type')
        return_id = session.get('return_id')
        if return_type:
            del session['return_type'], session['return_id']
            if return_type == 'comment':
                return redirect(url_for('main.reply_comment', id=return_id))
            elif return_type == 'reply':
                return redirect(url_for('main.reply_reply', id=return_id))
            else:
                return redirect(url_for('main.article', id=return_id))
        else:
            return redirect(url_for('main.index'))
    user = User(username=username, avatar_url=avatar_url, social_type='weibo')
    db.session.add(user)
    session['login'] = User.query.filter_by(username=username).filter_by(social_type='weibo').first().id
    return_type = session.get('return_type')
    return_id = session.get('return_id')
    if return_type:
        del session['return_type'], session['return_id']
        if return_type == 'comment':
            return redirect(url_for('main.reply_comment', id=return_id))
        elif return_type == 'reply':
            return redirect(url_for('main.reply_reply', id=return_id))
        else:
            return redirect(url_for('main.article', id=return_id))
    else:
        return redirect(url_for('main.index'))

@main.route('/logout')
def logout():
    del session['login']
    return redirect(url_for('main.index'))

@main.route('/others')
def others():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.category_id==1).order_by(Article.created_time.desc()).paginate(
        page, per_page=10)
    articles = pagination.items
    return render_template('others.html', articles=articles, pagination=pagination, idx='.others')

@main.route('/tutorial')
def tutorial():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.category_id!=1).order_by(Article.created_time.desc()).paginate(
        page, per_page=10)
    articles = pagination.items
    categorys = Category.query.filter(Category.id!=1).all()
    return render_template('tutorial.html', articles=articles, categorys=categorys, pagination=pagination, idx='.tutorial')

@main.route('/tutorial/<int:id>')
def select_tutorial(id):
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.filter(Article.category_id==id).order_by(Article.created_time.desc()).paginate(
        page, per_page=10)
    articles = pagination.items
    return render_template('index.html', articles=articles, pagination=pagination, idx='.select_tutorial')

@main.route('/article/<int:id>', methods=['GET', 'POST'])
def article(id):
    article = Article.query.get_or_404(id)
    article.add_reading_time()
    last = Article.query.filter(Article.id<id).order_by(Article.created_time.desc()).first()
    next = Article.query.filter(Article.id>id).order_by(Article.created_time).first()
    comment_page = request.args.get('page', 1, type=int)
    comments_pagination = Comment.query.filter_by(article_id=id).order_by(Comment.created_time).paginate(
        comment_page, per_page=10)
    comments = comments_pagination.items
    times = article.comments_times()
    user_id = session.get('login')
    if request.method == 'POST' and request.form['comment']:
        user = User.query.filter_by(id=user_id).first()
        comment = Comment(author=user.username, author_id=user_id, avatar_url=user.avatar_url,
                          content=request.form['comment'], article_id=id)
        db.session.add(comment)
        return redirect(url_for('main.article', id=id))
    return render_template('article.html', article=article, last=last, next=next, comments=comments,  times=times,
                           comments_pagination=comments_pagination, idx='.article', user_id=user_id)

@main.route('/reply/comment/<int:id>', methods=['GET', 'POST'])
def reply_comment(id):
    if session.get('login'):
        comment = Comment.query.get_or_404(id)
        user_id = session.get('login')
        if request.method == 'POST' and request.form['reply']:
            user = User.query.filter_by(id=user_id).first()
            reply = Reply(author=user.username, author_id=user_id, to_author=comment.author, avatar_url=user.avatar_url,
                          content=request.form['reply'], comment_id=comment.id)
            db.session.add(reply)
            return redirect(url_for('main.article', id=comment.article_id))
        return render_template('reply.html', comment=comment)
    return redirect(url_for('main.comment_login', return_type='comment', return_id=id))

@main.route('/reply/reply/<int:id>', methods=['GET', 'POST'])
def reply_reply(id):
    if session.get('login'):
        comment = Reply.query.get_or_404(id)
        user_id = session.get('login')
        if request.method == 'POST' and request.form['reply']:
            article_id = Comment.query.filter_by(id=comment.comment_id).first().article_id
            user = User.query.filter_by(id=user_id).first()
            reply = Reply(author=user.username, author_id=user_id, to_author=comment.author, avatar_url=user.avatar_url,
                          content=request.form['reply'], comment_id=comment.comment_id)
            db.session.add(reply)
            return redirect(url_for('main.article', id=article_id))
        return render_template('reply.html', comment=comment)
    return redirect(url_for('main.reply_login', return_type='reply', return_id=id))

@main.route('/delete/comment/<int:id>')
def del_comment(id):
    comment = Comment.query.get_or_404(id)
    article_id = comment.article_id
    comment_replys = Reply.query.filter_by(comment_id=comment.id).all()
    for each in comment_replys:
        db.session.delete(each)
    db.session.delete(comment)
    return redirect(url_for('main.article', id=article_id))

@main.route('/delete/reply/<int:id>')
def del_reply(id):
    reply = Reply.query.get_or_404(id)
    article_id = Comment.query.filter_by(id=reply.comment_id).first().article_id
    db.session.delete(reply)
    return redirect(url_for('main.article', id=article_id))

@main.route('/ImageUpdate', methods=['POST'])
def getimage():
    file = request.files['wangEditorH5File']
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        filename = file.filename
        if file and '.' in filename and filename.split('.')[1] in current_app.config['ALLOWED_EXTENSIONS']:
            access_key = current_app.config['QINIU_ACCESS_KEY']
            secret_key = current_app.config['QINIU_SECRET_KEY']
            q = Auth(access_key, secret_key)
            bucket_name = 'blogimage'
            key = filename
            token = q.upload_token(bucket_name, key, 3600)
            with open(filename, 'wb') as f:
                f.write(file.read())
            localfile = filename
            put_file(token, key, localfile)
            os.remove(filename)
            image_url = "http://oq39ef5bt.bkt.clouddn.com/%s" % filename
            res = Response(image_url)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res

@main.route('/search')
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.whoosh_search(keyword).order_by(Article.created_time.desc()).paginate(
        page, per_page=10)
    results = pagination.items
    return render_template('search.html', results=results, pagination=pagination, idx='.search', keyword=keyword)
