from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny

from drf_spectacular.utils import extend_schema

from .models import User,DeliveryLocation
from .serializers import ( UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
)
from .pagination import get_paginated_queryset
from .utils import get_tokens_for_user
from .permissions import DeleteUserPermission


# Create your views here.

##login View
class LoginView(APIView):
    permission_classes = [AllowAny,]


    @extend_schema(
        request=LoginSerializer,
        responses={200,LoginSerializer}
    )
    def post(self,request):
        requested_data = request.data
        serializer = LoginSerializer(data=requested_data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_tokens_for_user(user)
            context = {
                'status':200,
                'message':'User Logged in successfully!!!',
                'token': token
            }
            return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'Error While logging in',
                'error':serializer.errors
            }
            return Response(context,status=400)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def dispatch(self,request,*args,**kwargs):
        self.model = User
        self.serializer_class = UserSerializer
        self.queryset = self.model.objects.all()
        return super().dispatch(request,*args,**kwargs)

    @extend_schema(
        request=UserSerializer,
        responses={200:UserSerializer}
    )
    def get(self,request):
        data = get_paginated_queryset(self.queryset,request,self.serializer_class)
        return data



class UserCreateView(APIView):
    permission_classes = [AllowAny,]
    def dispatch(self,request,*args,**kwargs):
        self.model = User
        self.serializer_class = UserSerializer
        return super().dispatch(request,*args,**kwargs)

    @extend_schema(
        request=UserSerializer,
        responses={201:UserSerializer}
    )
    def post(self,request):
        requested_data = request.data
        serializer = self.serializer_class(data=requested_data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status': 201,
                'message':'User Created Successfully!!!',
                'data': serializer.data
            }
            return Response(context,status=201)
        else:
            context = {
                'status':'400',
                'message':'Error while creating user!!!',
                'error':serializer.errors
            }
            return Response(context,status=400)



class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self,request,*args,**kwargs):
        self.model = User
        self.user = self.model.objects.get(id=kwargs['id'])
        self.serializer_class = UserUpdateSerializer
        return super().dispatch(request,*args,**kwargs)



    @extend_schema(
        request=UserUpdateSerializer,
        responses={200:UserUpdateSerializer}
    )
    def patch(self,request,id):
        serializer = self.serializer_class(instance=self.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':200,
                'message':'User updated successsfully!!!',
                'data' : serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'Error while updating user',
                'error':serializer.errors
            }
            return Response(context,status=400)



class UserDeleteView(APIView):

    permission_classes = [DeleteUserPermission,]

    def delete(self,request,id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            context = {
                'status':200,
                'message': 'User Deleted Successfully!!!'
            }
            return Response(context,status=200)
        except:
            context={
                'status':404,
                'message':'User not found'

            }
            return Response(context,status=404)
