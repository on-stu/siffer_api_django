from rest_framework import status, viewsets
from rest_framework import response

from api.Size import Size, Musinsa
from .models import Site, User
from .serializers import SiteSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer


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
            command = 'global thisSite; thisSite = {0}(url="{1}", match="{2}")'.format(
                classname, pureUrl, match)
            exec(command)
            result = thisSite.run()
            return Response(data={"result": result})

        except Site.DoesNotExist:
            site = Size(url=url)
            result = site.run()

            return Response(data={"result": result})
    return Response(data={"bye": "hi"})
