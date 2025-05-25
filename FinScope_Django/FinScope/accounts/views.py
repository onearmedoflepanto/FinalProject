from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.conf import settings
from django.shortcuts import redirect, render

from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response


# View to render the login page
def login_page(request):
    return render(request, 'login.html')

# View to render the signup page
def signup_page(request):
    return render(request, 'sign_up.html')

@api_view(["POST"])
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    nickname = request.data.get("nickname")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "이미 존재하는 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        username=username,
        password=make_password(password),
        email=email,
        nickname=nickname,
    )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": f"{nickname}님 가입을 환영합니다!",
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )
    else:
        return Response(
            {"error": "유효하지 않은 로그인 시도입니다"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["GET", "PUT"])
def mypage(request):
    user = get_object_or_404(User, pk = request.user.pk)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def delete(request):
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def follow(request, pk):
    user = request.user
    target = get_object_or_404(User, pk=pk)
    if target == user:
        return Response(
            {"message": "자기 자신은 팔로우 할 수 없습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user in target.followers.all():
        target.followers.remove(user)
        message = "팔로우 취소 완료!"
    else:
        target.followers.add(user)
        message = "팔로우 완료!"
    return Response({"message": message}, status=status.HTTP_200_OK)

@api_view(['GET'])
def google_login(request):

    try:
        code = request.GET.get('code')
        if not code:
            return Response({"error": "api 요청 코드가 없습니다. 다시 시도해 주세요."}, status=400)
        
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        token_res = requests.post(token_url, data=data)
        token_json = token_res.json()
        access_token = token_json.get('access_token')

        userinfo_res = requests.get(
            'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo = userinfo_res.json()


        email = userinfo.get('email')
        if not email:
            return Response({"error": "Google 계정에서 이메일 정보를 가져올 수 없습니다.", "details": userinfo}, status=400)
        userinfo = userinfo_res.json()

        email = userinfo['email']
        nickname = userinfo.get('name', '구글유저')
        user, _ = User.objects.get_or_create(email=email, defaults={
            'username': email.split('@')[0],
            'nickname': nickname,
            'password': User.objects.make_random_password()
        })

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh_token =  str(refresh)
        redirect_url = f"http://localhost:8000/login-success/?access={access}&refresh={refresh_token}"
        return redirect(redirect_url)

    except Exception as e:
        return Response({"error": str(e)}, status=400)