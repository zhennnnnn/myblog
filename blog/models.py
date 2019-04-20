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
