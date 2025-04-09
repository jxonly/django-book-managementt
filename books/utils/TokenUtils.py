import jwt
import datetime
from django.conf import settings
from books.models import User  # 假设 User 模型在 books 应用中

class TokenUtils:
    @staticmethod
    def gen_token(user: User):
        """
        生成 JWT Token 
        :param user: User 对象
        :return: Token 字符串
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 设置过期时间（1天）
            'aud': str(user.id),  # 用户ID
        }
        # 使用用户密码的 HMAC256 加密算法生成 Token
        token = jwt.encode(payload, user.password, algorithm='HS256')
        return token

    @staticmethod
    def get_user_from_token(token: str):
        """
        从 Token 获取用户信息
        :param token: JWT Token
        :return: User 对象或 None
        """
        try:
            # 解码 Token，获取用户 ID
            payload = jwt.decode(token, options={"verify_exp": False})  # 不验证过期时间
            user_id = int(payload.get('aud'))
            user = User.objects.get(id=user_id)  # 查找对应用户
            return user
        except jwt.ExpiredSignatureError:
            print("Token 已过期")
            return None
        except jwt.InvalidTokenError:
            print("无效的 Token")
            return None
        except User.DoesNotExist:
            print("用户不存在")
            return None
