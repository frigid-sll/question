# Generated by Django 3.2 on 2021-05-14 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1)),
                ('ask', models.CharField(max_length=500, primary_key=True, serialize=False, verbose_name='题目')),
                ('answer', models.CharField(max_length=1000, verbose_name='答案')),
            ],
            options={
                'verbose_name_plural': '问题表',
            },
        ),
        migrations.CreateModel(
            name='Question_Catalogue',
            fields=[
                ('catalogue_name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='目录名')),
            ],
            options={
                'verbose_name_plural': '问题目录表',
            },
        ),
        migrations.CreateModel(
            name='Question_Classify',
            fields=[
                ('class_name', models.CharField(max_length=30, primary_key=True, serialize=False, verbose_name='题目类型')),
            ],
            options={
                'verbose_name_plural': '问题类型表',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(db_index=True, max_length=15, primary_key=True, serialize=False, verbose_name='账号'),
        ),
        migrations.CreateModel(
            name='Solve_Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=15, verbose_name='密码')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1)),
                ('answer', models.CharField(max_length=1000, verbose_name='答案')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
                ('ask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question')),
                ('catalogue_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_catalogue')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_classify')),
            ],
            options={
                'verbose_name_plural': '完成问题表',
            },
        ),
        migrations.CreateModel(
            name='Solve_Classify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=15, verbose_name='密码')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_classify')),
            ],
            options={
                'verbose_name_plural': '完成类型表',
            },
        ),
        migrations.CreateModel(
            name='Solve_Catalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=15, verbose_name='密码')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], max_length=1)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
                ('catalogue_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_catalogue')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_classify')),
            ],
            options={
                'verbose_name_plural': '完成目录表',
            },
        ),
        migrations.AddField(
            model_name='question_catalogue',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_classify'),
        ),
        migrations.AddField(
            model_name='question',
            name='catalogue_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_catalogue'),
        ),
        migrations.AddField(
            model_name='question',
            name='class_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.question_classify'),
        ),
    ]
