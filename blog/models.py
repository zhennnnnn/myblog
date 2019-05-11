from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	def publish(self):
		self.published_date = timezone.now()
		self.save()
	def __str__(self):
		return self.title

class Tag(models.Model):
	contact = models.ForeignKey(Post,on_delete=models.CASCADE)
	name    = models.CharField(max_length=50)

	def __str__(self): 
		return self.name

class Course(models.Model):
    name = models.CharField(max_length=255,verbose_name='課程名稱')
    teacher = models.CharField(max_length=255,verbose_name='授課教授')
    code=models.IntegerField()
    class_time=models.CharField(max_length=255,verbose_name='修課時間')
    grade=models.DecimalField(max_digits=2,decimal_places=1)
    comment=models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    #token = models.UUIDField(db_index=True, default=uuid.uuid4)


class Appeal(models.Model):
    name = models.CharField(max_length=255,verbose_name='授課名稱')
    code=models.IntegerField(verbose_name='選課代碼')
    number=models.IntegerField(verbose_name='編號')
    depiction =models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    #token = models.UUIDField(db_index=True, default=uuid.uuid4)

class gamee(models.Model):
    cAuthor = models.CharField(max_length=50, blank=True) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    cContent = models.CharField(max_length=9999,blank=True, default='')
    cTitle = models.CharField(max_length=100,blank=True, default='')#blank=True 欄位可空白
    cLink = models.CharField(max_length=100,blank=True, default='')
 
    #每一筆資料在管理介面顯示的內容以下列程式定義
    def __str__(self):
        return self.cTitle #表示顯示cTitle欄位


import ast

class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
        
class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    name = models.CharField(max_length=128, unique = True) #唯一，不可有相同姓名
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="男")
    ctime = models.DateTimeField(auto_now_add=True)
    clove = ListField(blank=True)

    def __str__(self):
        return self.name
