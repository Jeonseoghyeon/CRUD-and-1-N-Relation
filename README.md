# 5/6 혼자 하면서 막힌 부분

> 코드 작성을 진행할 때 기존 코드 참고 한 부분 or 새로 알게된 부분들만 군더더기 없이 작성

### 1. Accounts

1. login 함수 구현

   ![image-20200506201643874](CRUD 혼자 하면서 막힌 부분.assets/image-20200506201643874.png)

   - AuthenticationForm에 들어가는 parameter들을 놓쳤다.
   - login할 때 auth_login에 들어가는 `form.get_user`를 놓쳤다.

2. signup 한 뒤 바로 login 시켜버리기

   ```python
   from django.contrib.auth import authenticate # 일단 authenticate를 import
   ```

   ```python
   if form.is_valid():
               new_user = form.save() # form의 정보를 new_user에 저장해주고
               authenticated_user = authenticate(username=new_user.username, password=request.POST['password1']) # authenticate에 필요한 파라미터인 username, password를 넣어준다. 이 때 password1은 회원가입시 첫번째에 작성하는 비밀번호임(password1=password2이라 둘 다 써도 무방)
               auth_login(request,authenticated_user) # 기존 form.get_user()로 form에 있는 정보를 login함수에 넣어줬었는데, 우리는 현재 authenticated_user에 넣었으므로 이렇게 작성
               return redirect('articles:index')
   ```



3. __회원정보 업데이트 가능?__

4. login_required 적절히 써주기

   ```python
   # 일단 login_required import
   from django.contrib.auth.decorators import login_required
   ```

   ```python
   # 그 다음엔 login 함수 내에 이 코드를 넣어준다.
   return redirect(request.GET.get('next') or 'community:review_list')
   # 단축평가를 이용한 코드임!
   ```





### 2. Articles

1. Article 작성을 위한 Model 정의시 user 가져오기

   ```python
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   ```

   ```python
   # get_user_model 활용법
   ```

2. __form에서 exclude?__

3. Article 작성할 때 이런 오류가 나면 create함수 내 commit=False하는 부분 추가해줘야 한다.

   - 이유 : 해당 article에 user가 누구인지 저장하기 위해서

   ![image-20200506211737466](CRUD 혼자 하면서 막힌 부분.assets/image-20200506211737466.png)

   ```python
   if form.is_valid():
               article = form.save(commit=False)
               article.user = request.user
               article.save()
   ```



4. detail 페이지 불러올 때 하는 법

   ```python
   from django.shortcuts import render, redirect, get_object_or_404
   # 일단 get_object_or_404 추가
   ```

   ```python
   # html에 보내주자
   def detail(request,article_id):
       article = get_object_or_404(Article, id = article_id)
       context = {
           'article':article
       }
       return render(request,'articles/detail.html',context)
   ```

5. update 함수 구현 / detail.html 구현

   ```python
   # update 함수!
   def update(request,article_id):
       article = get_object_or_404(Article, id = article_id)
       if request.method == "POST":
           form = ArticleForm(request.POST, instance = article)
           if form.is_valid():
               form.save()
               return redirect('articles:detail',article_id)
       else:
           form = ArticleForm(instance = article)
       context = {
           'form' : form
       }
       return render(request, 'articles/form.html', context)
   ```

   ```html
   <!-- detail.html -->
   <!-- POST로 하면 안됨!!! -->
   <form action="{% url 'articles:update' article.id%}">
       <input type="submit" value="글 수정">
   </form>
   ```



### 3. Comments

1. 댓글 create 부분 .. 여기 완전 털림.. 공부할것!!!!!!!!!

   ```python
   @login_required
   def comment_create(request,article_id):
       article = get_object_or_404(Article, id = article_id)
       if request.method == 'POST':
           form = CommentForm(request.POST)
           if form.is_valid():
               comment = form.save(commit=False)
               comment.article = article
               comment.user = request.user
               comment.save()
       return redirect('articles:detail', article_id)
   ```

2. __데이터 스키마에 있는 attribute만 값을 줄 수 있나?__

   - 안되는듯?

3. __코멘트 업데이트 그 위치에서 하기__

