from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import NotFound

from drf_spectacular.utils import extend_schema

from .models import User,DeliveryLocation
from .serializers import ( UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    DeliveryLocationSerializer,
)
from .pagination import get_paginated_queryset
from .utils import get_tokens_for_user,get_age_group,plot_age_groups
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



###user view

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



###deliverylocation view

class DeliveryLocationCreateView(APIView):
    permission_classes = [IsAuthenticated,]
    def dispatch(self,request,*args,**kwargs):
        self.model = DeliveryLocation
        self.serializer_class = DeliveryLocationSerializer
        return super().dispatch(request,*args,**kwargs)

    @extend_schema(
        request = DeliveryLocationSerializer,
        responses={200:DeliveryLocationSerializer},
    )
    def get(self,request,**kwargs):
        user_id = kwargs.get('id')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(f"User with the id: {user_id} not found.")
        else:
            user = request.user
        queryset = self.model.objects.filter(user=user)

        data = get_paginated_queryset(queryset,request,self.serializer_class)
        return data


    @extend_schema(
        request = DeliveryLocationSerializer,
        responses={201:DeliveryLocationSerializer},
    )
    def post(self,request,**kwargs):
        requested_data = request.data
        serializer = self.serializer_class(data=requested_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            context = {
                'status':201,
                'message':'Delivery Address added Successfully!!!',
                'data': serializer.data
            }

            return Response(context,status=201)
        else:
            context = {
                'status':400,
                'message':'Error while creating delivey location',
                'error': serializer.errors
            }
            return Response(context,status=400)



class LocationUpdateView(APIView):

    def patch(self,request,id):
        try:
            instance = DeliveryLocation.objects.get(id=id)
        except DeliveryLocation.DoesNotExist:
            raise NotFound(f'Delivery Location with the id: {id} not found')
        serializer = DeliveryLocationSerializer(instance=instance,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                'status':200,
                'message':'Delivery location updated successfully!!!',
                'data':serializer.data
            }
            return Response(context,status=200)
        else:
            context = {
                'status':400,
                'message':'Error while updating the delivery location',
                'error':serializer.errors
            }
            return Response(context,status=400)


class LocationDeleteView(APIView):
    permission_classes = [IsAuthenticated,]

    def delete(self,request,id):
        try:
            delivery_location = DeliveryLocation.objects.get(id=id)
            delivery_location.delete()
            context = {
                'status':200,
                'message': 'Delivery Location Deleted Successfully!!!'
            }
            return Response(context,status=200)
        except:
            context={
                'status':404,
                'message':'Delivery Location not found'
            }
            return Response(context,status=404)



## user age group

class AgeGroupDistributionView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self,request):
        age_distribution = get_age_group()

        context = {
            'status':200,
            'message':'Data reterived successfully!!!',
            'data': age_distribution
        }
        return Response(context,status=200)



class MatplotlibView(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):
        img_base64 = plot_age_groups()
        context = {
            'status':200,
            'message':'Data reterived successfully!!!',
            'data': img_base64
        }
        return Response(context,status=200)
