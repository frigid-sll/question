import enum
from typing import AnyStr
from django.db.models import Q
from myapp.serializers import *
from myapp import models
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
import os
from Question import settings
import re
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
import docx
import time

#download
from django.utils.encoding import escape_uri_path
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from rest_framework import status

# Create your views here.

ip='192.168.0.126'


class Handle(GenericViewSet):
    '''对数据库进行操作'''
    queryset=''
    @action(methods=["POST"],detail=False)
    def solve_question(self,request):
        '''添加完成的问题'''
        account=request.session.get('account')
        class_name=request.data.get('question_classify')
        sex=request.data.get('sex')
        catalogue_name=class_name+'#'+request.data.get('catalogue')
        answer=request.POST.get('solvue_question')[1:-1].split(',')
        

        mes={'code':200}
        
        for index,value in enumerate(answer):
            answer[index]='' if value=='""' else answer[index][1:-1]

        question_list=[x.ask for x in models.Question.objects.filter(Q(class_name=class_name)&Q(catalogue_name=catalogue_name))]
        
        for index,value in enumerate(question_list):
            problem=models.Question.objects.filter(ask=value).first()
            account=models.User.objects.filter(account=account).first()
            is_exist=models.Solve_Question.objects.filter(Q(ask=problem)&Q(account=account))
            if answer[index]:
                if is_exist:
                    is_exist.update(answer=answer[index])
                else:
                    models.Solve_Question.objects.create(
                        account=account,
                        sex=sex,
                        class_name=models.Question_Classify.objects.filter(class_name=class_name).first(),
                        catalogue_name=models.Question_Catalogue.objects.filter(catalogue_name=catalogue_name).first(),
                        ask=problem,
                        answer=answer[index]
                    )
            else:
                if is_exist:
                    is_exist.delete()
        
        return Response(mes)

class Acquire(GenericViewSet):
    """获取数据"""
    queryset=''

    def get_new(self,index_list,a):
        _list,_list2,_list3=[],[],[]
        for index,value in enumerate(index_list):
            if index%2==0:
                _list.append([x for x in range(value,index_list[index+1]+1)])
        for x in _list:
            for y in x:
                _list2.append(y)
        for index,value in enumerate(a):
            if index not in _list2:
                _list3.append(value)
        for x in _list:
            start,end=x[0],x[len(x)-1]
            _list3.insert(x[0],[y for y in a[start:end+1]])
        return _list3

    @action(detail=False)
    def question_classify(self,request):
        '''获取所有问题类型'''
        self.queryset=models.Question_Classify.objects.all()
        res=Question_Classify_Serializer(self.queryset,many=True)
        mes={'code':200,'res':res.data}
        return Response(mes)
    
    @action(methods=["POST"],detail=False)
    def catalogue(self,request):
        '''获取某问题类型的所有问题目录'''
        # Manage_User.add_data()
        # models.Question.objects.filter(ask='名一医学调查问卷#社会心理*男&9%8：请勾选您的压力来源:+ ').update(
        #     ask='名一医学调查问卷#社会心理*男&9%8：请勾选您的压力来源:+')
        # models.Question.objects.filter(catalogue_name=models.Question_Catalogue.objects.filter(
        #     catalogue_name='名一医学调查问卷#睡眠质量*男').first()).delete()
        
        account=request.session.get('account')
        question_classify=request.data.get('question_classify')
        sex=request.data.get('sex')
        self.queryset=models.Question_Catalogue.objects.filter(Q(class_name=question_classify)&Q(sex=sex))
        catalogue_list=[x.catalogue_name.split('#')[1] for x in self.queryset]
        all_question=[x.ask.split('#')[1].split('&')[0] for x in models.Question.objects.filter(class_name=question_classify)]
        question_count=[all_question.count(x) for x in catalogue_list]
        solve_question=[str(x.catalogue_name).split('#')[1] for x in models.Solve_Question.objects.filter(Q(account=account)&Q(class_name=question_classify))]
        solve_question_count={x:0 for x in catalogue_list}
        for key in solve_question_count.keys():
            solve_question_count[key]=solve_question.count(key)
        solve_question_count=[x for x in solve_question_count.values()]
        mes={'code':200,'catalogue_list':catalogue_list,'question_count':question_count,'solve_question_count':solve_question_count,'ip':ip}
        return Response(mes)
    
    @action(methods=["POST"],detail=False)
    def question(self,request):
        '''获取某类型的某目录的所有问题以及做过的答案'''

        # a,b=[x.ask for x in models.Question.objects.filter(catalogue_name=models.Question_Catalogue.objects.filter(
        #     catalogue_name='名一医学调查问卷#工作习惯*男').first()).all()],[]
       
        # for index,value in enumerate(a):
        #     b.append(value.replace('{}%'.format(index+1),''))

        # for index,value in enumerate(a):
        #     models.Question.objects.filter(ask=value).update(ask=b[index])

        account=request.session.get('account')
        class_name=request.data.get('question_classify')
        catalogue_name=class_name+'#'+request.data.get('catalogue')
        sex=request.data.get('sex')
        question_all=models.Question.objects.filter(Q(class_name=class_name,sex=sex,catalogue_name=catalogue_name))
        question_list=[
            str(x.ask).split('&')[1] for x in question_all
        ]
        answer_list=[
            x.answer for x in question_all
        ]
        for index,value in enumerate(answer_list):
            if value:
                answer_list[index]=str(answer_list[index]).split(',')
        #设置每个问题的id
        question_id=['a'+str(index) for index,value in enumerate(question_list)]
        # print(question_id)
        ###获取问题答案
        solve_question_answer=[]
        for x in question_all:
            is_solve=models.Solve_Question.objects.filter(Q(ask=x)&Q(account=account))
            res=is_solve.first().answer if is_solve else ''
            result=res.split('#') if '#' in res else res
            solve_question_answer.append(result)
        
        
        index_list=[]
        for index,value in enumerate(answer_list):
            if value:
                for x,y in enumerate(value):
                    if '|' in y:
                        index_list.append(index)
                        if answer_list[index][x]=='|':
                            answer_list[index]=None
                        else:
                            answer_list[index][x]=answer_list[index][x][1:]

             
        for index,value in enumerate(question_list):
            is_letter=re.findall('([a-z]+其他)',value)
            if is_letter:
                question_list[index]=is_letter[0][is_letter[0].find('其他'):]
        
        new_answer_list,new_question_list,new_question_id,new_solve_question_answer,is_show=[],[],[],[],''
        

        if index_list:
            for index,value in enumerate(index_list):
                if index%2==0:
                    new_answer_list=self.get_new(index_list,answer_list)
                    new_question_list=self.get_new(index_list,question_list)
                    new_question_id=self.get_new(index_list,question_id)
                    new_solve_question_answer=self.get_new(index_list,solve_question_answer)
            
            judge_index=[]
            try:
                for x in new_question_list:
                    if type(x)==list:
                        judge_index.append(x[0][0:x[0].find('%')])
                    else:
                        judge_index.append(x[0:x.find('%')])

                b=sorted(judge_index,key=lambda x:int(x))
                

                res_question_list=[new_question_list[judge_index.index(x)] for x in b]
                res_answer_list=[new_answer_list[judge_index.index(x)] for x in b]
                res_solve_question_answer=[new_solve_question_answer[judge_index.index(x)] for x in b]
                res_question_id=[new_question_id[judge_index.index(x)] for x in b]

                for index,value in enumerate(res_question_list):
                    if type(value)==list:
                        for x,y in enumerate(value):
                            res_question_list[index][x]=res_question_list[index][x][res_question_list[index][x].find('%')+1:]
                    else:
                        res_question_list[index]=res_question_list[index][res_question_list[index].find('%')+1:]
            except:
                res_question_list=new_question_list
                res_answer_list=new_answer_list
                res_solve_question_answer=new_solve_question_answer
                res_question_id=new_question_id
            is_show={index:True for index,value in enumerate(res_question_list) if type(value)==list}
        
        # print(new_question_list)
        # print(new_answer_list)
        # print(new_solve_question_answer)
        # print(new_question_id)
        
        

        if index_list==[]:
            mes={'code':200,'question_list':question_list,'answer_list':answer_list,'question_id':question_id,
                        'solve_question_answer':solve_question_answer,'res_id':question_id,'is_show':''} 
            
        else:
            mes={'code':200,'question_list':res_question_list,'answer_list':res_answer_list,'question_id':res_question_id,
                        'solve_question_answer':res_solve_question_answer,'res_id':question_id,'is_show':is_show}
            
        # print(mes['question_list'])
        
        return Response(mes)
    
    @action(detail=False)
    def all_user(self,request):
        '''获取所有用户'''
        self.queryset=models.User.objects.all()
        res=UserSerializer(self.queryset,many=True)
        mes={'code':200,'all_user':res.data}
        return Response(mes)

    @action(methods=["POST"],detail=False)
    def user_question_classify(self,request):
        '''获取用户做过的问题类型'''
        account=models.User.objects.filter(account=request.data.get('account')).first()
        request.session['account']=account.account
        sex=account.sex
        self.queryset=models.Solve_Question.objects.filter(account=account)
        all_solve_question=Solve_Question_Serializer(self.queryset,many=True)
        question_classify=list(set([x['class_name'] for x in all_solve_question.data])) if all_solve_question.data else []
        mes={'code':200,'user_question_classify':question_classify,'sex':sex}
        return Response(mes)

class Manage_User(GenericViewSet):
    """用户操作"""

    def add_data():
        file=docx.Document("名一医学调查问卷(男性）.docx")
        #输出每一段的内容
        text_list=[para.text.strip() for para in file.paragraphs]
        # print(text_list)
        a=[x[1:] for x in '#'.join(text_list).split('-') if x!='#' and x]
        # print(a)
        for num,x in enumerate(a):
            index=x.find(re.findall('\d[*]+',x)[0])
            # print(x[index])
            big='名一医学调查问卷'
            sex='男'
            small='{}#生活习惯*{}'.format(big,sex)
            class_name=models.Question_Classify.objects.filter(class_name='{}'.format(big)).first()
            catalogue_name=models.Question_Catalogue.objects.filter(catalogue_name='{}'.format(small)).first()
            ask='{}&'.format(small)+x[:index]
            num=x[:index]
            if '|' in x:
                if x[index]=='1':
                    models.Question.objects.create(
                        class_name=class_name,
                        catalogue_name=catalogue_name,
                        sex=sex,
                        ask=ask,
                        answer='|'
                    )
                else:
                    answer=','.join([x for x in x[index+3:].split('#') if x])
                    models.Question.objects.create(
                        class_name=class_name,
                        catalogue_name=catalogue_name,
                        sex=sex,
                        ask=ask,
                        answer=answer
                    )
            else:
                if x[index]=='1':
                    models.Question.objects.create(
                        class_name=class_name,
                        catalogue_name=catalogue_name,
                        sex=sex,
                        ask=ask,
                        answer=''
                    )
                else:
                    answer=','.join([x for x in x[index+2:].split('#') if x])
                    models.Question.objects.create(
                        class_name=class_name,
                        catalogue_name=catalogue_name,
                        sex=sex,
                        ask=ask,
                        answer=answer
                    )

    @action(methods=["POST"],detail=False)
    def login(self,request):
        '''登录'''
        account=request.data.get('account')
        password=request.data.get('password')
        is_exist=models.User.objects.filter(Q(account=account)&Q(password=password))
        if is_exist:
            request.session['account']=account
            mes={'code':200,'sex':is_exist.first().sex,'root':0}
            if account=='root':
                mes['root']=1
        else:
            mes={'code':0}
        return Response(mes)

    @action(methods=["POST"],detail=False)
    def register(self,request):
        '''注册'''
        account=request.data.get('account')
        password=request.data.get('password')
        sex=request.data.get('sex')
        is_exist=models.User.objects.filter(account=account)
        if not is_exist:
            models.User.objects.create(account=account,password=password,sex=sex)
            mes={'code':200}
        else:
            mes={'code':0}
        return Response(mes)

    @action(methods=["POST"],detail=False)
    def img(self,request):
        '''上传图片下载到upload'''
        image = request.FILES.get('file')
        #以防上传图片会覆盖以前的所以我们拼接一个时间戳解决
        image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+image.name
        f = open(os.path.join(settings.UPLOAD_FILE,image_name),'wb')
        #image.chunks() 以二进制流写入文件
        for i in image.chunks():
            f.write(i)
        f.close()
        mes={'code':200,'img_url':'http://{}:8000/upload/'.format(ip)+image_name}
        return Response(mes)
    

    @action(detail=False)
    def del_img(self,request):
        '''删除图片'''
        img_path=os.getcwd().replace('\\','/')+'/upload'
        os.system('cd {}&&del * /s /q'.format(img_path))
        mes={'code':200}
        return Response(mes)
    
    @action(methods=["POST"],detail=False)
    def download(self,request):
        '''导出用户答题记录'''
        mes={'code':200}
        account=models.User.objects.filter(account=request.data.get('account')).first()
        sex=account.sex
        question_classify=models.Question_Classify.objects.filter(class_name=request.data.get('question_classify')).first()
        solve_question=models.Solve_Question.objects.filter(Q(account=account)&Q(class_name=question_classify))
        catalogue=[
            x.catalogue_name.split('#')[1].split('*')[0] for x in models.Question_Catalogue.objects.filter(Q(sex=sex)&Q(class_name=question_classify))
        ]
        catalogue_ask=[
            str(x.ask).replace('/','').split('#')[1].split('*'+sex+'&') for x in solve_question
        ]
        
        ask_catalogue=[x[0] for x in catalogue_ask]
        ask=[x[1] for x in catalogue_ask]
        for index,value in enumerate(ask):
            if ':' in value:
                ask[index]=value.split(':')[1]
            if '+' in ask[index]:
                ask[index]=ask[index][:-1]
            if '，' in ask[index]:
                s=ask[index].split('，')
                ask[index]=s[0]+s[1]
        
        answer=[
            x.answer for x in solve_question
        ]
        solve_catalogue=list(set(ask_catalogue))
        totol_list=[[] for x in solve_catalogue]
        for x,y in enumerate(solve_catalogue):
            ask_array,answer_array=[],[]
            for index,value in enumerate(ask_catalogue):
                if value==y:
                    ask_array.append(ask[index])
                    answer_array.append(answer[index])
            totol_list[x]=np.array([ask_array,answer_array])
       
        # print(solve_catalogue)     #用户答过的目录
        # print(catalogue)           #用户做的类型的所有目录 
        # print(ask_catalogue)       #用户答的每一个题所属的目录
        # print(ask)                 #用户的答题问题
        # print(answer)              #用户的答题答案
        # print(totol_list)          #根据答过的目录分类好答过的题目以及答案转为数组

        #写入excel
        
        res={x:y for x,y in zip(solve_catalogue,totol_list)}
        # print(res)
        excel_path=os.getcwd().replace('\\','/')+'/Excel/'
        name=question_classify.class_name+'-'+sex+'-'+account.account
        excel_name=excel_path+name+'.xlsx'
        # print(excel_name)
        
        writer=pd.ExcelWriter(excel_name)
        for key,value in res.items():
            df=pd.DataFrame(value)
            df.to_excel(writer, sheet_name=key, header=False, index=False)
        writer.save()

        #写入word
        word_path=os.getcwd().replace('\\','/')+'/Word/'

        file_path=word_path+name+'.docx'
        word_total=[]
        for key,value in res.items():
            content={}
            for x,y in enumerate(value[0]):
                content[y[:-1]]=value[1][x]
            word_total.append(content)
        # print(word_total)
        context = {}
        for x in word_total:
            for key,value in x.items():
                context[key]=value
        # print(context)
        tpl=DocxTemplate(word_path+'名一医学调查问卷(女性）.docx')
        tpl.render(context)
        tpl.save(file_path)
        return Response(mes)



class Download(GenericViewSet):
    '''下载文件到本地'''

    @action(methods=["POST"],detail=False)
    def file(self,request):
        filename = request.data.get("filename")
        if filename[-4:]=='docx':
            download_file_path = os.path.join(settings.BASE_DIR, "Word",filename)
        else:
            download_file_path = os.path.join(settings.BASE_DIR, "Excel",filename)
        # print("download_file_path",download_file_path)
 
        response = self.big_file_download(download_file_path, filename)
        if response:
            return response
 
        return JsonResponse({'status': 'HttpResponse', 'msg': 'Excel下载失败'})
 
    def file_iterator(self,file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
 
    def big_file_download(self,download_file_path, filename):
        try:
            response = StreamingHttpResponse(self.file_iterator(download_file_path))
            # 增加headers
            response['Content-Type'] = 'application/octet-stream'
            response['Access-Control-Expose-Headers'] = "Content-Disposition, Content-Type"
            response['Content-Disposition'] = "attachment; filename={}".format(escape_uri_path(filename))
            return response
        except Exception:
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Excel下载失败'},
                                status=status.HTTP_400_BAD_REQUEST)