# books/urls.py
from django.urls import path
from .views import LoginView,RegisterView,DashboardView,UserView,UserUpdateView,UserUpdatePasswordView,UserSearchView,UserDeleteView,UserDeleteBatchView,UserFindView,BookView

urlpatterns = [
    path('user/login', LoginView.as_view(), name='user_login'),
    path('user/register', RegisterView.as_view(), name='user_register'),
    path('dashboard', DashboardView.as_view(), name='get_dashboard'),
    path('user/', UserView.as_view(), name='user_create'),  # 创建用户
    path('user/update', UserUpdateView.as_view(), name='user_update'),  # 更新用户信息
    path('user/password', UserUpdatePasswordView.as_view(), name='user_update_password'),  # 更新密码
    path('user/deleteBatch', UserDeleteBatchView.as_view(), name='user_delete_batch'),  # 批量删除
    path('user/<int:id>', UserDeleteView.as_view(), name='user_delete'),  # 删除用户
    path('user/find/', UserFindView.as_view(), name='user_find'),  # 查询用户
    path('user/usersearch', UserSearchView.as_view(), name='user_search'),  # 自定义查询
    path('book', BookView.as_view(), name='book_manage'), 
]
