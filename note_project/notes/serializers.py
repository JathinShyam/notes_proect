from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
            if data['username']:
                if User.objects.filter(username=data['username']).exists():
                    raise serializers.ValidationError("Username already exists")
                
            if data['email']:
                if User.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError("email already exists")
                
            return data
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return validated_data
    

class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
