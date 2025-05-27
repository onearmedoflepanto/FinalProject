from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()
from .serializers import (
    UserSerializer,
    SavedFinancialProductSerializer,
    BookmarkedVideoSerializer,
    SavedAiRecommendationSerializer, # Import new serializer
)
from .models import SavedFinancialProduct, BookmarkedVideo, SavedAiRecommendation # Import new model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

import requests
from decouple import config


@api_view(["POST"])
def sign_up(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    nickname = request.data.get("nickname")

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "이미 존재하는 사용자명입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "이미 사용중인 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
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
    user = get_object_or_404(User, pk=request.user.pk)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_financial_product(request):
    serializer = SavedFinancialProductSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        # Check for duplicates manually if needed, though unique_together should handle it
        # fin_co_no = serializer.validated_data.get('fin_co_no')
        # fin_prdt_cd = serializer.validated_data.get('fin_prdt_cd')
        # product_type = serializer.validated_data.get('product_type')
        # if SavedFinancialProduct.objects.filter(user=request.user, fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd, product_type=product_type).exists():
        #     return Response({"detail": "Product already saved."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_ai_recommendation(request):
    serializer = SavedAiRecommendationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # recommendation_data is expected to be a JSON string from the frontend
        # user_profile_at_recommendation is expected to be a JSON object (dict)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def unsave_financial_product(
    request, product_pk
):  # product_pk is the ID of the SavedFinancialProduct instance
    try:
        saved_product = SavedFinancialProduct.objects.get(
            pk=product_pk, user=request.user
        )
        saved_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except SavedFinancialProduct.DoesNotExist:
        return Response(
            {"detail": "Saved product not found or permission denied."},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST", "OPTIONS"])
def social_login(request):
    access_token = request.data.get("token")  # Google ID 토큰, Kakao/Naver 인증 코드
    provider = request.data.get("provider")
    state = request.data.get("state")  # Naver 로그인 시 필요

    if not access_token or not provider:
        return Response(
            {"error": "Token and provider are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if provider == "google":
        # Google의 경우 access_token이 ID 토큰임
        google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={access_token}"
        response = requests.get(google_url)

        if response.status_code != 200:
            return Response({"error": "Invalid Google token"}, status=400)

        user_info = response.json()
        email = user_info.get("email")
        username = user_info.get("name") or email.split("@")[0]
        if not email:
            return Response({"error": "Google user email not found"}, status=400)

    elif provider == "kakao":
        token_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": config("KAKAO_REST_API_KEY"),
            "redirect_uri": "http://localhost:5173/login",  # 프론트엔드 로그인 페이지 URI
            "code": access_token,  # Kakao의 경우 access_token이 인증 코드임
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        token_response = requests.post(token_url, data=data, headers=headers)

        token_json = token_response.json()
        if token_response.status_code != 200:
            print(token_json)
            return Response(
                {
                    "error": f"Kakao token exchange failed: {token_json.get('error_description', '')}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        kakao_access_token = token_json.get("access_token")

        user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {kakao_access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        user_info = user_info_response.json()
        if user_info_response.status_code != 200:
            print(user_info)
            return Response(
                {"error": "Invalid Kakao token"}, status=status.HTTP_400_BAD_REQUEST
            )

        kakao_account = user_info.get("kakao_account", {})
        email = kakao_account.get("email")
        profile = kakao_account.get("profile", {})
        username = profile.get("nickname")
        kakao_id = str(user_info.get("id"))

        if not username:  # 닉네임 동의 안했을 경우
            username = f"kakao_{kakao_id}"
        if not email:  # 이메일 동의 안했을 경우
            email = f"{username}@kakao.com"  # 임시 이메일

    elif provider == "naver":
        # Naver의 경우 access_token이 인증 코드임
        naver_client_id = config("NAVER_CLIENT_ID")
        naver_client_secret = config("NAVER_CLIENT_SECRET")

        token_url = "https://nid.naver.com/oauth2.0/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": naver_client_id,
            "client_secret": naver_client_secret,
            "code": access_token,
            "state": state,  # CSRF 방지를 위해 전달받은 state 값 사용
        }
        token_response = requests.post(token_url, data=data)

        token_json = token_response.json()
        if token_response.status_code != 200:
            print(token_json)
            return Response(
                {
                    "error": f"Naver token exchange failed: {token_json.get('error_description', '')}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        naver_access_token = token_json.get("access_token")

        user_info_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {naver_access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        user_info = user_info_response.json()
        if user_info_response.status_code != 200 or user_info.get("resultcode") != "00":
            print(user_info)
            return Response(
                {"error": "Failed to get Naver user info"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_data = user_info.get("response", {})
        email = response_data.get("email")
        username = response_data.get("nickname") or response_data.get("name")
        naver_id = response_data.get("id")

        if not username:  # 닉네임 정보가 없을 경우
            username = f"naver_{naver_id}"
        if not email:  # 이메일 정보가 없을 경우
            email = f"{username}@naver.com"  # 임시 이메일

    else:
        return Response(
            {"error": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = None
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
    elif User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)

    if not user:
        user = User.objects.create(username=username, email=email)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_video_bookmark(request):
    serializer = BookmarkedVideoSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # Check if already bookmarked to prevent duplicates, though unique_together handles DB level
        video_id = serializer.validated_data.get('video_id')
        if BookmarkedVideo.objects.filter(user=request.user, video_id=video_id).exists():
            # Optionally, return a different response or update existing timestamp
            return Response({"detail": "Video already bookmarked."}, status=status.HTTP_409_CONFLICT)
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
