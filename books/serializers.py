from rest_framework import serializers
from books.models import User,Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nick_name', 'password', 'sex', 'address', 'phone', 'role']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'price', 'publisher','isbn','borrownum','create_time','status'] 