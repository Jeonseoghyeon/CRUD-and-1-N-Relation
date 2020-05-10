```python
class Article(models.Model):
	title = models.TextField()
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()

```



관계 설정이라는 건 양쪽 모델을 이어준다는 것입니다.

위의 코드에서 보면 Article 모델과 Comment 모델을 연결 했는데

이 과정에서 ForeignKey를 사용하였습니다.

그렇기 때문에 Article에서 Comment를 참조할때 자동으로 생성되는 comment_set을 사용합니다.

실제 코드에서는 안보이지만 아래와 같다고 볼 수 있습니다.



```python
class Article(models.Model):
	title = models.TextField()
    # comment_set = 
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()

```



그런데 이때 related_name를 적용한다면 아래와 같이 설정이 된다고 볼 수 있습니다.



```python
class Article(models.Model):
	title = models.TextField()
    # comments = 
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

```



따라서 related_name은 내가 설정하지 않은 반대편 모델에서 관계설정을 한 모델에 어떻게 참조할지에 대한 설정이라고 볼 수 있습니다.



그럼 여기서 User M:N설정에서의 모델관계를 보면 아래와 같습니다.



```python
class User(models.Model):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
```



User 모델을 연결하려는 모델이 자기 자신이 되는 형태인데 

위에서 설명했던 원리로 사실은 아래와 같이 코드가 생성된다고 보시면 됩니다.



```python
class User(models.Model):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # user_set = 
```

그럼 여기서 결국 followers에는 내가 팔로우 하는 사람을 저장하고

user_set에는 나를 팔로우 하는 사람이 저장될 수 있습니다.

따라서 지금의 코드에서는 related_name이 없어도 정상적으로 코드가 동작합니다. 

단순히 이름을 부르기 편하게 만들기 위하여 설정한 값입니다.



문제가 발생하는 부분은 다음과 같습니다.



```python
class User(models.Model):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
class Article(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User)

```



이렇게 코드를 작성한 것을 적용한다면 



```python
class User(models.Model):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # article_set = ForeignKey로 연결
    # article_set = ManyToMany로 연결
    
class Article(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User)
```



위와 같이 user모델에 두개의 칼럼이 중복생성된다고 생각할 수 있습니다.

그렇기 때문에 두개 중 하나의 이름을 바꿔주기 위하여 related_name을 사용해야만 한다고 보면 됩니다.



```python
class User(models.Model):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    # article_set = ForeignKey로 연결하여 자동으로 생성
    # like_articles = ManyToMany로 연결하여 related_name으로 생성
    
class Article(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User)
    like_users = models.ManyToManyField(User, related_name='like_articles')
```

