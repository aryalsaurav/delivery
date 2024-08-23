from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import User,DeliveryLocation



## serializers

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields = ['email','username','password','password2','full_name','dob','ph_number']
        extra_kwargs = {
            'password': {'write_only':True},
            'username':{'required':False}
        }


    def validate(self,validated_data):
        password = validated_data.get('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password does not match.')
        return validated_data

    def create(self,data):
        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','dob','ph_number','full_name']





class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self,validated_data):
        try:
            email = validated_data['email']
            password = validated_data['password']
        except Exception as e:
            print(str(e))
            raise serializers.ValidationError('Email and Password is required')

        user = authenticate(email=email,password=password)
        if not user:
            raise serializers.ValidationError({
                'not found':'User not found'
            })
        validated_data['user'] = user
        return validated_data




class DeliveryLocationSerializer(serializers.ModelSerializer):

    class Meta:
        pass
