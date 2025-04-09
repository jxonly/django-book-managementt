# utils/login_user.py
from django.core.cache import cache  # 导入 Django 缓存模块

class LoginUser:
    @staticmethod
    def add_visit_count():
        # 获取当前的访问次数
        visit_count = cache.get('visit_count', 0)  # 从缓存中获取访问次数，如果没有，则默认为0
        visit_count += 1  # 增加访问次数
        cache.set('visit_count', visit_count, timeout=None)  # 将更新后的访问次数保存回缓存

    @staticmethod
    def get_visit_count():
        # 从缓存中获取访问次数
        return cache.get('visit_count', 0)  # 如果没有缓存，返回0
