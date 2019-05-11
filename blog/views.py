from django.shortcuts import redirect,render
from django.utils import timezone
from .models import Post
from blog.models import gamee,User
from . import models
from django.http import HttpResponse
from django import forms
from blog.form import UserForm,RegisterForm
import hashlib
import requests
from bs4 import BeautifulSoup
import urllib
import re
import html

# Create your views here.


def post_list(request):
	if request.method == "POST":
		new_title = request.POST.get('title')
		new_text = request.POST.get('text')
		new_post = Post(title=new_title, text=new_text)
               
		new_post.save()

		new_post.publish()        
		return redirect('post_list')

	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})


def post_create(request):
    return render(request, 'blog/post_create.html', {})

def crawler(request):  #爬蟲程式
    global titles,links,at,ct,t,l
    url = 'https://forum.gamer.com.tw/B.php?bsn=31406'   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")

    title = sp.findAll('td',{"class":"b-list__main"})
    titles = []
    for titlee in title:
        titles.append(titlee.text.strip('\n'))

    links = []
    ll = 'https://forum.gamer.com.tw/'
    link = sp.find("table",{"class":"b-list"}).findAll("a", href = re.compile('C.php?'))
    for linkk in link:
        page = re.compile(r'^((?!page).)*$')  ##不匹配page
        last = re.compile(r'^((?!last).)*$')  ##不匹配last
        m = page.match(linkk['href'])  ##設定變數m來排除page
        if m != None:  ##若不為None (None會跳出例外)
            n = last.match(m.group(0)) ## 設定變數n來排除last
            if n != None: ##若不為None (None會跳出例外)
                links.append(ll+n.group(0))

    for t,l in zip(titles,links):
        print(t,l)
        content(l) #使用爬蟲出來的網址進行文章內容的爬蟲
        sql()  #將爬出的內容進行與資料庫的連接
    return redirect('/index/')



def content(aa):
    global titles,links,at,ct,t,l
    url = aa   #選擇網址
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15' #偽裝使用者
    headers = {'User-Agent':user_agent}
    data_res = urllib.request.Request(url=url,headers=headers)
    data = urllib.request.urlopen(data_res)
    data = data.read().decode('utf-8')  
    sp = BeautifulSoup(data, "html.parser")

    authors = sp.find('div',{"class":"c-post__header__author"}).findAll("a",{"class":"username"})
    for author in authors:
        at = author.text
        print(at)

    contents = sp.find('div',{"class":"c-article__content"})
    ct = html.escape(str(contents))#html編碼轉譯
    print(ct)

def sql():
    global titles,links,at,ct,t,l

    cAuthor = at    
    cContent = ct
    cTitle = t
    cLink = l
    try:
        if gamee.objects.get(cTitle=t):
            print('已有重複資料')
            
    except:
        unit = gamee.objects.create(cAuthor=cAuthor, cContent=cContent, cTitle=cTitle, cLink=cLink) 
        unit.save()                      #寫入資料庫
        print('成功儲存一筆資料')
 

def hash_code(s, salt='ivan'): #密碼加密
    h = hashlib.sha256()
    s = s + salt
    h.update(s.encode())
    return h.hexdigest()

def login(request):

    if request.session.get('is_login',None): #檢查session確定是否登入，不允許重複登入
        return redirect("/index/")  #若已登入則導向主頁
    if request.method == 'POST':    #接收POST訊息，若無則讓返回空表單
        login_form = UserForm(request.POST)   #導入表單模型
        if login_form.is_valid(): #驗證表單
            username = login_form.cleaned_data['username']  #從表單的cleaned_data中獲得具體值
            password = login_form.cleaned_data['password'] 
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password): #密文處理
                    #使用session寫入登入者資料
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    message = "登入成功"
                    return redirect('/index/')
                else:
                    message = "密碼不正確"
            except:
                message = "該用戶不存在"
    login_form = UserForm(request.POST) #返回空表單
    return render(request,"blog/login.html",locals())

def logout(request):
    if not request.session.get('is_login',None): #如果原本未登入，就不需要登出
        return redirect('/index/')
    request.session.flush() #一次性將session內容全部清除
    return redirect('/index/') 
 
def register(request):
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		message = '請檢察填寫的內容!'
		if register_form.is_valid(): #驗證數據，提取表單內容
			username = register_form.cleaned_data['username'] 
			password1 = register_form.cleaned_data['password1']
			password2 = register_form.cleaned_data['password2']
			email = register_form.cleaned_data['email']
			sex = register_form.cleaned_data['sex']
			if password1 != password2: #若兩次密碼不同
				message = "兩次輸入的密碼不同!"
				return render(request, 'register.html', locals())
			else:
				same_name_user = models.User.objects.filter(name=username) #比對資料庫是否有相同用戶名
				if same_name_user:
					message = "該用戶名稱已存在!"
					return render(request, 'register.html', locals())
				same_email_user = models.User.objects.filter(email=email)  #比對資料庫是否有相同信箱
				if same_email_user:
					message = "信箱已被使用!"
					return render(request, 'register.html', locals())
			#若上面條件皆通過，則創建新的用戶
				new_user = models.User()
				new_user.name = username
				new_user.password = hash_code(password1)
				new_user.email = email
				new_user.sex = sex
				new_user.save()
				return redirect('/login/') #自動跳轉到登入頁面
	register_form = RegisterForm(request.POST)
	return render(request, 'blog/register.html', locals())

def index(request):
    unit = gamee.objects.all().order_by( '-id' ) 
    return render(request,"blog/index.html",locals())

def detail(request, detailid=None):
    timg2 = timg1
    unit = gamee.objects.get(id=detailid)
    cTitle = unit.cTitle
    cAuthor = unit.cAuthor
    cContent = html.unescape(unit.cContent).replace("data-src","src") 

    #cContent反轉譯，且由於巴哈有延遲載入，因此src屬性名稱不同需替換
    return render(request,"blog/detail.html",locals())

