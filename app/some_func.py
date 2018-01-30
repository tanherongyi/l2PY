from flask import current_app
import requests, re

class OAuthMethod():
    def git_path(self):
        path = current_app.config['GITHUB_AUTHORIZE_URL'] + '?client_id=' + current_app.config[
            'GITHUB_CLIENT_ID'] + '&scope=user' + '&state=' + 'asdas89d789as7d98as456'
        return path

    def git_userinfo(self, code):
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

    def weibo_path(self):
        path = current_app.config['WEIBO_AUTHORIZE_URL'] + '?client_id=' + current_app.config[
            'WEIBO_CLIENT_ID'] + '&response_type=code' + '&redirect_uri=' + 'https://www.l2py.com/weibo/oauth/callback'
        return path

    def weibo_userinfo(self, code):
        # 通过传入client_id、client_secret、code三个参数向 'https://api.weibo.com/oauth2/access_token' 发送POST请求，获取access_token
        url = 'https://api.weibo.com/oauth2/access_token'
        params = {
            'client_id': current_app.config['WEIBO_CLIENT_ID'],
            'client_secret': current_app.config['WEIBO_CLIENT_SECRET'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'https://www.l2py.com/weibo/oauth/callback',
        }
        r = requests.post(url, params=params)
        r.encoding = r.content
        result = r.json()
        access_token = result['access_token']
        uid = result['uid']

        # 将access_token、uid 传入'https://api.weibo.com/2/users/show.json'，发送GET请求，获取用户信息
        url = 'https://api.weibo.com/2/users/show.json'
        params = {
            'access_token': access_token,
            'uid': uid,
        }
        r = requests.get(url, params)
        result = r.json()
        return result

oauthmethod = OAuthMethod()

def ch_content(content):
    ch_rule = re.compile(r'<[^>]+>', re.S)
    ch_content = ch_rule.sub('', content)
    return ch_content

