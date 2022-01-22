from rest_framework import status, viewsets
from rest_framework import response

from api.Size import Size, Musinsa, Xexymix, Leelin
from .models import Product, Site, User
from .serializers import ProductSerializer, SiteSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView

from rest_framework.exceptions import AuthenticationFailed
from api.serializers import UserSerializer

import jwt
import datetime


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': "success",
            'token': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


@api_view(['GET', 'POST'])
def site_list(request):
    # get all articles
    if (request.method == 'GET'):
        articles = Site.objects.all()
        serializer = SiteSerializer(articles, many=True)
        return Response(serializer.data)
    elif(request.method == 'POST'):
        serializer = SiteSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def getSize(request):
    if(request.method == 'POST'):
        url = request.data['url']
        pureUrl = url
        getUrlNum = 0
        for i in range(0, len(url)-1):
            if(url[i] == '/'):
                getUrlNum += 1
                if(getUrlNum == 3):
                    url = url[0: i]
                    break

        try:
            site_object = Site.objects.get(url=url)
            class_object = Site._meta.get_field('classname')
            classname = class_object.value_from_object(site_object)
            if len(classname) == 0:
                classname = 'Size'
            match_object = Site._meta.get_field('match')
            match = match_object.value_from_object(site_object)
            encoding_object = Site._meta.get_field('encoding')
            encoding = encoding_object.value_from_object(site_object)

            command = 'global thisSite; thisSite = {0}(url="{1}", match="{2}", encoding="{3}")'.format(
                classname, pureUrl, match, encoding)
            exec(command)
            result = thisSite.run()
            return Response(data={"result": result})

        except Site.DoesNotExist:
            site = Size(url=url)
            result = site.run()

            return Response(data={"result": result})
    return Response(data={"bye": "hi"})
