from django.http.response import Http404, HttpResponseForbidden
from rest_framework import generics, status
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer, StaffSerializer, AuthCustomTokenSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Customer, Staff, User


class CreateCustomer(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

class CreateStaff(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StaffSerializer
    

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': token.key,
        }

        return Response(content)

class ProfileView(APIView):
    
    queryset = User.objects.all()
    
    def get(self, request, format=None):
        serializer = None
        user = request.user
        if user.is_superuser:
            serializer = UserSerializer
        elif user.is_staff:
            serializer = StaffSerializer
            user = Staff.objects.get(user=user)
        else:
            serializer = CustomerSerializer
            user = Customer.objects.get(user=user)
        
        if user and serializer:
            return Response(serializer(user).data)
        else:
            return Http404("User not found")
        
class LogoutView(APIView):
    
    def get(self, request):
        user = request.user
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            user.auth_token.delete()
            return Response(status=status.HTTP_200_OK, data="success")