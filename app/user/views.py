from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile
from .serializers import UserSerializer

@api_view(["GET"])
# @permission_classes([AllowAny])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_all_users(request):
    try:
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    try:
        if not request.data: return Response({"errors": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['is_staff'] = False
        request.data['is_superuser'] = False

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    try:
        if not request.data: return Response({"errors": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.get(email=request.data['email'])

        if not user.check_password(request.data['password']):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
    except UserProfile.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_user(data, user):
    data['is_staff'] = False
    data['is_superuser'] = False

    serializer = UserSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def user_details(request):
    try:
        user = UserProfile.objects.get(email=request.user.email)
    
        if request.method == 'GET':
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        if request.method == "PUT":
            if not request.data: return Response({"detail": "No data"}, status=status.HTTP_400_BAD_REQUEST)
            return update_user(request.data, user)

        if request.method == "DELETE":
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
    
    except UserProfile.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
