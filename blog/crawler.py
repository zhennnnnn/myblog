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
 