#!/usr/bin/env python
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import Admin, User, Category, Article, Comment, Reply

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Admin=Admin, User=User, Category=Category, Article=Article, Comment=Comment, Reply=Reply)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def add_original_settings():
    print("请在下方输入要添加的admin账号信息:")
    admin_name = input("用户名:")
    while admin_name == '':
        print("用户名不能为空,请重新输入!")
        admin_name = input("用户名:")
    admin_password = input("密码:")
    while admin_password == '':
        print("密码不能为空,请重新输入!")
        admin_password = input("密码:")
    admin = Admin(name=admin_name, password=admin_password)
    db.session.add(admin)
    db.session.commit()
    print(r"admin账号已添加完毕，请使用此账号登录后台进行管理操作，登录地址为http://hostname:port/admin/login")
    print("接下来添加其它分类，请不要删除该分类哦!")
    category = Category(name='其它')
    db.session.add(category)
    db.session.commit()
    print("其它分类已经添加完毕,请愉快玩耍项目!")


if __name__ == '__main__':
    manager.run()