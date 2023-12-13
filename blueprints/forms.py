import wtforms
from wtforms.validators import Length, EqualTo
from models import UserModel

class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3,max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6,max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])
    # 自定义验证：
    # 1. 用户名是否已经被注册
    def validate_username(self, field):
        username = field.data
        user = UserModel.query.filter_by(username=username).first()
        if user:
            raise wtforms.ValidationError(message="该用户名已经被注册！")

    # # 2. 密码是否正确
    # def validate_password(self, field):
    #     password = field.data
    #     username = self.username.data
    #     password_model = UserModel.query.filter_by(username=username, password=password).first()
    #     if password_model is not None:
    #     # 找到了匹配的用户记录，执行相关操作
    #     else:
    #     # 没有找到匹配的用户记录，执行相应的处理
    #
    #     if not password_model:
    #         raise wtforms.ValidationError(message="用户名或密码错误！")
    #     # else:
    #     #     # todo：可以删掉captcha_model
    #     #     db.session.delete(captcha_model)
    #     #     db.session.commit()



class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3,max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])