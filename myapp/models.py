from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class User(models.Model):
    '''用户表'''

    #account db_index=True设置索引，primary=True设置主键
    account=models.CharField(verbose_name='账号',max_length=15,db_index=True,primary_key=True)
    password=models.CharField(verbose_name='密码',max_length=15)
    #sex choices 设置单选，元组前面的值为真是存储值，后面的值为展示值
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
    class Meta:
        verbose_name_plural='用户表'
    def __str__(self):
        return self.account


class Question_Classify(models.Model):
    '''问题类型表'''

    class_name=models.CharField(max_length=30,verbose_name='题目类型',primary_key=True)
    class Meta:
        verbose_name_plural='问题类型表'
    def __str__(self):
        return self.class_name

class Question_Catalogue(models.Model):
    '''问题目录表'''

    #ForeignKey设置外键
    class_name=models.ForeignKey(Question_Classify,on_delete=CASCADE)
    catalogue_name=models.CharField(max_length=30,verbose_name='目录名',primary_key=True)
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')],default='男')
    class Meta:
        verbose_name_plural='问题目录表'
    def __str__(self):
        return self.catalogue_name

class Question(models.Model):
    '''问题表'''
    class_name=models.ForeignKey(Question_Classify,on_delete=CASCADE)
    catalogue_name=models.ForeignKey(Question_Catalogue,on_delete=CASCADE)
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
    ask=models.CharField(max_length=500,verbose_name='题目',primary_key=True)
    answer=models.CharField(max_length=1000,verbose_name='答案',null=True,blank=True)
    class Meta:
        verbose_name_plural='问题表'
    def __str__(self):
        return self.ask

class Solve_Question(models.Model):
    '''完成问题表'''

    account=models.ForeignKey(User,on_delete=CASCADE)
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
    class_name=models.ForeignKey(Question_Classify,on_delete=CASCADE)
    catalogue_name=models.ForeignKey(Question_Catalogue,on_delete=CASCADE)
    ask=models.ForeignKey(Question,on_delete=CASCADE)
    answer=models.CharField(max_length=1000,verbose_name='答案')
    class Meta:
        verbose_name_plural='完成问题表'
    def __str__(self):
        return str(self.account)+"--->"+str(self.ask)

class Solve_Catalogue(models.Model):
    '''完成目录表'''

    account=models.ForeignKey(User,on_delete=CASCADE)
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
    catalogue_name=models.ForeignKey(Question_Catalogue,on_delete=CASCADE)
    class_name=models.ForeignKey(Question_Classify,on_delete=CASCADE)
    class Meta:
        verbose_name_plural='完成目录表'
    def __str__(self):
        return str(self.account)+"--->"+str(self.catalogue_name)

class Solve_Classify(models.Model):
    '''完成类型表'''

    account=models.ForeignKey(User,on_delete=CASCADE)
    sex=models.CharField(max_length=1,choices=[('男','男'),('女','女')])
    class_name=models.ForeignKey(Question_Classify,on_delete=CASCADE)
    class Meta:
        verbose_name_plural='完成类型表'
    def __str__(self):
        return str(self.account)+"--->"+str(self.class_name)
