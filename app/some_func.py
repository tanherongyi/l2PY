from flask import current_app, url_for, redirect, request
import requests

class OAuthMethod():
    def nomal_path(self):
        path = current_app.config['GITHUB_AUTHORIZE_URL'] + '?client_id=' + current_app.config[
            'GITHUB_CLIENT_ID'] + '&scope=user' + '&state=' + 'asdas89d789as7d98as456'
        return path

    def nomal_userinfo(self):
        # 判断回调地址中是否拿到code
        if 'code' not in request.args:
            return redirect(url_for('github_login'))
        code = request.args.get('code')

        # 通过传入client_id、client_secret、code三个参数向 'https://github.com/login/oauth/access_token' 发送POST请求，获取access_token
        url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id': current_app.config['GITHUB_CLIENT_ID'],
            'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
            'code': code
        }
        r = requests.post(url, params=params)
        r.encoding = r.content
        result = r.text
        access_token = result.split('&')[0].split('=')[1]

        # 将access_token 传入'https://api.github.com/user?access_token='，发送GET请求，获取用户信息
        url = 'https://api.github.com/user?access_token=%s' % access_token
        r = requests.get(url)
        r.encoding = r.content
        result = r.json()
        return result

    def comment_path(self):
        path = current_app.config['GITHUB_AUTHORIZE_URL'] + '?client_id=' + current_app.config[
            'GITHUB_CLIENT_ID1'] + '&scope=user' + '&state=' + 'asdas89d789as7d98as456'
        return path

    def comment_userinfo(self):
        # 判断回调地址中是否拿到code
        if 'code' not in request.args:
            return redirect(url_for('github_login'))
        code = request.args.get('code')

        # 通过传入client_id、client_secret、code三个参数向 'https://github.com/login/oauth/access_token' 发送POST请求，获取access_token
        url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id': current_app.config['GITHUB_CLIENT_ID1'],
            'client_secret': current_app.config['GITHUB_CLIENT_SECRET1'],
            'code': code
        }
        r = requests.post(url, params=params)
        r.encoding = r.content
        result = r.text
        access_token = result.split('&')[0].split('=')[1]

        # 将access_token 传入'https://api.github.com/user?access_token='，发送GET请求，获取用户信息
        url = 'https://api.github.com/user?access_token=%s' % access_token
        r = requests.get(url)
        r.encoding = r.content
        result = r.json()
        return result

    def reply_path(self):
        path = current_app.config['GITHUB_AUTHORIZE_URL'] + '?client_id=' + current_app.config[
            'GITHUB_CLIENT_ID2'] + '&scope=user' + '&state=' + 'asdas89d789as7d98as456'
        return path

    def reply_userinfo(self):
        # 判断回调地址中是否拿到code
        if 'code' not in request.args:
            return redirect(url_for('github_login'))
        code = request.args.get('code')

        # 通过传入client_id、client_secret、code三个参数向 'https://github.com/login/oauth/access_token' 发送POST请求，获取access_token
        url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id': current_app.config['GITHUB_CLIENT_ID2'],
            'client_secret': current_app.config['GITHUB_CLIENT_SECRET2'],
            'code': code
        }
        r = requests.post(url, params=params)
        r.encoding = r.content
        result = r.text
        access_token = result.split('&')[0].split('=')[1]

        # 将access_token 传入'https://api.github.com/user?access_token='，发送GET请求，获取用户信息
        url = 'https://api.github.com/user?access_token=%s' % access_token
        r = requests.get(url)
        r.encoding = r.content
        result = r.json()
        return result

