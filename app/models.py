from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from jieba.analyse.analyzer import ChineseAnalyzer

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(18))

    def __repr__(self):
        return '<Admin %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(20))
    username = db.Column(db.String(64), index=True)
    avatar_url = db.Column(db.String(128))
    social_type = db.Column(db.String(30))

    def __repr__(self):
        return '<User %s>' % self.username

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    # 添加到Role模型中的users属性代表这个关系的面向对象视角。对于一个Role类的实例，其users属性将返回与角色相关联的用户组成的列表。
    # db.relationship()的第一个参数表明这个关系的另一端是哪个模型，backref参数则向User模型添加一个role属性，从而定义反向关系。
    # 这一属性可替代role_id访问Role模型，此时获取的是模型对象，而不是外键的值。
    articles = db.relationship('Article', backref='category')

    def __repr__(self):
        return '<Category %s>' % self.name

    def add_others(self):
        category = Category(name='其它')
        db.session.add(category)
        db.session.commit()

# 定义文章类，将在数据库中创建文章的table
class Article(db.Model):
    # __tablename__ 的值作为数据
    __tablename__ = 'articles'
    __searchable__ = ['title', 'content']
    __analyzer__ = ChineseAnalyzer()
    # 文章id，定义primary_key属性为True，表示id为主键
    id = db.Column(db.Integer, primary_key=True)
    # 标题，长度限制为80，并定义unique属性为True，不允许出现重复值
    title = db.Column(db.String(80), unique=True)
    # 发布时间，定义index属性为True，为这列创建索引；定义default属性为datetime.now，设置默认值为提交时间
    created_time = db.Column(db.DateTime, index=True, default=datetime.now)
    # 文章内容，定义nullable属性为Flase，不允许出现空内容
    content = db.Column(db.Text, nullable=False)
    # 文章缩写
    abstract = db.Column(db.String(140), nullable=False)
    # 阅读量
    reading_time = db.Column(db.Integer, default=0)
    # 文章分类
    # role_id列被定义为外键，这个外键连接了roles表中的id列和users表中的role_id列
    # 传给db.ForeignKey()的参数'roles.id'表示这列的值是roles表中id列的值
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    comments = db.relationship('Comment', backref='article')

    def __repr__(self):
        return '<Article %s>' % self.title

    def add_reading_time(self):
        self.reading_time += 1

    def comments_times(self):
        comments = Comment.query.filter_by(article_id=self.id).order_by(Comment.created_time).all()
        times = 0
        for each in comments:
            times += 1
            if each.replys:
                times += len(each.replys)
        return times

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    author_id = db.Column(db.Integer)
    avatar_url = db.Column(db.String(128))
    created_time = db.Column(db.DateTime, index=True, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    replys = db.relationship('Reply', backref='comment')

class Reply(db.Model):
    __tablename__ = 'replys'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=True)
    author_id = db.Column(db.Integer)
    to_author = db.Column(db.String(64), index=True)
    to_author_id = db.Column(db.Integer)
    avatar_url = db.Column(db.String(128))
    created_time = db.Column(db.DateTime, index=True, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))