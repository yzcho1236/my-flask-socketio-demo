from flask_login import UserMixin
from peewee import Model, CharField
from itsdangerous import TimedJSONWebSignatureSerializer





@login_manager.request_loader
def load_user_by_request(web_request):
    jwt = TimedJSONWebSignatureSerializer(secret_key=app.secret_key)
    auth = web_request.headers.get("Authorization")
    if auth:
        user_id = str(jwt.loads(auth))
        return User.query.filter_by(alternative_id=user_id).first()

    else:
        return None


class User(UserMixin,Model):
    id = CharField(max_length=32,primary_key=True,help_text='id')
    nickname = CharField(max_length=100,null=True,help_text='昵称')
    username = CharField(max_length=100,null=True,help_text='用户名')
    password = CharField(max_length=255,null=True,help_text='密码')
    alternative_id = CharField(max_length=32,null=True,help_text='备用替代ID')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_table"

    def get_id(self):
        jwt = TimedJSONWebSignatureSerializer(secret_key=app.secret_key)
        return jwt.dumps(str(self.all_inheritable)).decode()
