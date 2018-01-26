from qiniu import Auth

def get_token():
    #需要填写你的 Access Key 和 Secret Key
    access_key = 'yFZl4V8ZlCg8j4-EDV_KLfx1JEi8mMTcvfQnGfBo'
    secret_key = 'wooC5JykXfoKIEhYdxQYsNV1FjZ2EFttes_NR83l'

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'blogimage'

    #上传到七牛后保存的文件名
    key = ''

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    return token


