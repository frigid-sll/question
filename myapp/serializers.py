from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):

    class Meta:
        model=User
        fields='__all__'

class Question_Classify_Serializer(ModelSerializer):
    
    class Meta:
        model=Question_Classify
        fields='__all__'

class Question_Catalogue_Serializer(ModelSerializer):
    
    class Meta:
        model=Question_Catalogue
        fields='__all__'

class Question_Serializer(ModelSerializer):
    
    class Meta:
        model=Question
        fields='__all__'

class Solve_Question_Serializer(ModelSerializer):
    
    class Meta:
        model=Solve_Question
        fields='__all__'

class Solve_Catalogue_Serializer(ModelSerializer):
    
    class Meta:
        model=Solve_Catalogue
        fields='__all__'

class Solve_Classify_Serializer(ModelSerializer):
    
    class Meta:
        model=Solve_Classify
        fields='__all__'
