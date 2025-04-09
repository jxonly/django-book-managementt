from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import User,LendRecord,Book
from books.utils.TokenUtils import TokenUtils  # 导入我们定义的 TokenUtils
from books.utils.Result import Result  # 导入 Result 类
from books.utils.login_user import LoginUser
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q  # 用于多条件查询
from books.serializers import UserSerializer,BookSerializer

#分页
class UserPagination(PageNumberPagination):
    page_size = 10  # 每页显示10个用户
    page_size_query_param = 'pageSize'  # 允许客户端通过查询参数指定每页记录数
    max_page_size = 500  # 设置最大分页大小

#登录
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # 查找用户
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            # 用户不存在时，返回错误信息
            return Response(Result.error("-1", "用户名或密码错误").to_dict(), status=status.HTTP_200_OK)

        # 生成 Token 
        token = TokenUtils.gen_token(user=user)
    
        LoginUser.add_visit_count()
         # 返回包含所有用户信息和 token 的成功响应
        user_data = {
            "id": user.id,
            "username": user.username,
            "nick_name": user.nick_name,  # 假设模型字段为 `nick_name`
            "password": user.password,  # 如果需要返回密码，可以包含它（但通常不推荐）
            "sex": user.sex,  # 假设模型字段为 `sex`
            "address": user.address,  # 假设模型字段为 `address`
            "phone": user.phone,  # 假设模型字段为 `phone`
            "token": token,
            "role": user.role  # 假设模型字段为 `role`
        }
 
        # 返回成功响应
        return Response(Result.success(user_data).to_dict(),status=status.HTTP_200_OK)

#注册
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response(Result.error("-1", "用户名已存在").to_dict(), status=status.HTTP_200_OK)

        # 创建新的用户并保存到数据库
        user = User.objects.create(username=username, password=password,role=role)

        # 返回成功响应
        return Response(Result.success({"user": {"username": user.username, "id": user.id}}).to_dict(), status=status.HTTP_200_OK)

#新建一个用户
class UserView(APIView):
    def post(self, request):
        # 提取用户数据
        user_data = request.data

        # 如果密码为空，设置默认密码
        if 'password' not in user_data or not user_data['password']:
            user_data['password'] = "abc123456"

        # 创建用户并保存
        user = User.objects.create(**user_data)

        # 返回成功的响应
        return Response(Result.success().to_dict(), status=status.HTTP_200_OK)
#更新用户信息
class UserUpdateView(APIView):
    def put(self, request):
        user_data = request.data
        print(user_data)  # 调试用，打印请求数据

        # 获取用户信息
        user = user_data.get('user')
        if not user:
            return Response(Result.error("-1", "缺少用户数据").to_dict(), status=status.HTTP_400_BAD_REQUEST)

        user_id = user.get('id')
        if not user_id:
            return Response(Result.error("-1", "缺少必要的用户ID").to_dict(), status=status.HTTP_400_BAD_REQUEST)

        # 获取用户对象
        existing_user = User.objects.filter(id=user_id).first()
        if not existing_user:
            return Response(Result.error("-1", "用户未找到").to_dict(), status=status.HTTP_404_NOT_FOUND)

        # 只更新特定字段
        updated_fields = ['nick_name', 'phone', 'sex', 'address']
        for field in updated_fields:
            if field in user_data:  # 仅当字段存在时更新
                setattr(existing_user, field, user_data.get(field))

        existing_user.save()  # 保存更新后的用户对象

        return Response(Result.success().to_dict(), status=status.HTTP_200_OK)

#更新密码
class UserUpdatePasswordView(APIView):
    def put(self, request):
        user_id = request.data.get('id')
        new_password = request.data.get('password')

        if not user_id or not new_password:
            return Response(Result.error("-1", "缺少必要参数").to_dict(), status=status.HTTP_400_BAD_REQUEST)

        # 查找用户并更新密码
        user = User.objects.filter(id=user_id).first()
        if user:
            user.password = new_password
            user.save()
            return Response(Result.success().to_dict(), status=status.HTTP_200_OK)
        else:
            return Response(Result.error("-1", "用户未找到").to_dict(), status=status.HTTP_404_NOT_FOUND)


#删除单个用户
class UserDeleteView(APIView):
    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response(Result.success().to_dict(), status=status.HTTP_200_OK)
        else:
            return Response(Result.error("-1", "用户未找到").to_dict(), status=status.HTTP_404_NOT_FOUND)

#批量删除用户
class UserDeleteBatchView(APIView):
    def post(self, request):
        user_ids = request.data.get('ids')

        if not user_ids:
            return Response(Result.error("-1", "没有提供要删除的用户ID").to_dict(), status=status.HTTP_400_BAD_REQUEST)

        # 批量删除用户
        User.objects.filter(id__in=user_ids).delete()
        return Response(Result.success().to_dict(), status=status.HTTP_200_OK)
    
#查找单个用户
class UserFindView(APIView):
    def get(self, request):
        search = request.query_params.get('search', '')
        page_size = request.query_params.get('page_size', 10)
        page_num = request.query_params.get('page', 1)

        users = User.objects.filter(nick_name__icontains=search, role=2)  # 模糊查询
        paginator = UserPagination()
        result_page = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(result_page)
#根据条件查询用户
class UserSearchView(APIView):
    def get(self, request):
        page_num = int(request.query_params.get('pageNum', 1))
        page_size = int(request.query_params.get('pageSize', 10))

        search1 = request.query_params.get('search1', '')
        search2 = request.query_params.get('search2', '')
        search3 = request.query_params.get('search3', '')
        search4 = request.query_params.get('search4', '')

        

         # 构建查询条件
        filters = Q(role=2)  # 默认只查询 role=2 的用户
        if search1:
            filters &= Q(id=search1)  # 模糊匹配 id
        if search2:
            filters &= Q(nick_name__icontains=search2)  # 模糊匹配昵称
        if search3:
            filters &= Q(phone__icontains=search3)  # 模糊匹配手机号
        if search4:
            filters &= Q(address__icontains=search4)  # 模糊匹配地址

        # 获取符合条件的用户
        users = User.objects.filter(filters)
        # 分页
        paginator = UserPagination()
        paginator.page_size = page_size  # 动态设置每页显示的数据条数
        
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)

        res_data = {
            "records":serializer.data,
            "total":len(serializer.data)
        }
        return Response(Result.success(res_data).to_dict(), status=status.HTTP_200_OK)  # 返回分页后的响应

#看板
class DashboardView(APIView):
    def get(self, request): 
        # 获取访问次数
        visit_count = LoginUser.get_visit_count() 

        # 获取用户数量
        user_count = User.objects.count()

        # 获取借阅记录数量
        lend_record_count = LendRecord.objects.count()

        # 获取书籍数量
        book_count = Book.objects.count()

        # 构造结果数据
        data = {
            "visitCount": visit_count,
            "userCount": user_count,
            "lendRecordCount": lend_record_count,
            "bookCount": book_count
        }
    
        return Response(Result.success(data).to_dict(), status=status.HTTP_200_OK)

#书籍管理
class BookView(APIView):
    # 创建新书籍
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 保存新书籍
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 更新现有书籍
    def put(self, request):
        book_id = request.data.get('id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 使用序列化器更新书籍数据
        serializer = BookSerializer(book, data=request.data, partial=True)  # partial=True 表示部分更新
        if serializer.is_valid():
            serializer.save()  # 保存更新后的书籍
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

