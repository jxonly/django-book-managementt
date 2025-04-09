from django.db import models

# Create your models here.
# 书籍表
class Book(models.Model):
    # 自动递增的ID字段
    id = models.AutoField(primary_key=True)
    
    # ISBN 字段
    isbn = models.CharField(max_length=255)
    
    # 书名字段
    name = models.CharField(max_length=255)
    
    # 价格字段
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # 作者字段
    author = models.CharField(max_length=255)
    
    # 借阅数量字段
    borrownum = models.IntegerField()
    
    # 出版商字段
    publisher = models.CharField(max_length=255)
    
    # 创建时间字段，使用Django的DateTimeField，并设置为自动添加当前时间
    create_time = models.DateTimeField(auto_now_add=True)
    
    # 书籍状态字段
    status = models.CharField(max_length=50)

    # 定义模型的字符串表示
    def __str__(self):
        return self.name 
    class Meta:
        db_table = 'book'  # 显式指定表名，确保与数据库中的表一致
# 借阅信息表
class BookWithUser(models.Model):
    # 自动递增的ID字段
    id = models.AutoField(primary_key=True)
    
    # ISBN 字段
    isbn = models.CharField(max_length=255)
    
    # 书名字段
    book_name = models.CharField(max_length=255)
    
    # 用户昵称字段
    nick_name = models.CharField(max_length=255)
    
    # 借书时间字段
    lendtime = models.DateTimeField()
    
    # 还书时间字段
    deadtime = models.DateTimeField()
    
    # 续借次数字段
    prolong = models.IntegerField()

    # 定义模型的字符串表示
    def __str__(self):
        return f'{self.book_name} by {self.nick_name}'
    
    class Meta:
        db_table = 'bookwithuser'  # 显式指定表名
# 借阅记录表
class LendRecord(models.Model):
    # 读者ID字段
    reader_id = models.IntegerField()
    
    # ISBN字段
    isbn = models.CharField(max_length=255)
    
    # 书名字段
    bookname = models.CharField(max_length=255)
    
    # 借书时间字段
    lend_time = models.DateTimeField()
    
    # 还书时间字段
    return_time = models.DateTimeField()
    
    # 状态字段
    status = models.CharField(max_length=50)
    
    # 借阅次数字段
    borrownum = models.IntegerField()

    # 定义模型的字符串表示
    def __str__(self):
        return f'{self.book_name} borrowed by reader {self.reader_id}'
    
    class Meta:
        db_table = 'lend_record'  # 显式指定表名
#用户表
class User(models.Model):
    # 自动递增的ID字段
    id = models.AutoField(primary_key=True)
    
    # 用户名字段
    username = models.CharField(max_length=255)
    
    # 昵称字段
    nick_name = models.CharField(max_length=255)
    
    # 密码字段
    password = models.CharField(max_length=255)
    
    # 性别字段
    sex = models.CharField(max_length=50)
    
    # 地址字段
    address = models.CharField(max_length=255)
    
    # 电话字段
    phone = models.CharField(max_length=20)
    
    # token字段（表中没有此字段，使用`null=True`表示它是可选的）
    # token = models.CharField(max_length=255, null=True, blank=True)
    
    # 角色字段
    role = models.IntegerField()

    # 定义模型的字符串表示
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'  # 显式指定表名