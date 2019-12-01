from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=24)
    visit = models.IntegerField(default=0)

    owner = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="group")

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=24)  # 제목
    content = models.TextField()  # 내용

    visit = models.IntegerField(default=0)  # 방문자 수
    recommend = models.IntegerField(default=0)  # 추천 수

    owner = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="post")  # 글 주인
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # 소속 그룹

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()  # 내용

    owner = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="comment")  # 댓글 주인
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 소속 포스트

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.username
