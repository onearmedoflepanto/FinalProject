from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
User = get_user_model()
import requests
from django.conf import settings
from django.shortcuts import redirect, render

from .serializers import UserSerializer, SavedFinancialProductSerializer, NotificationSubscriptionSerializer, FinancialProductSerializer # Import FinancialProductSerializer
from .models import SavedFinancialProduct, FinancialProduct # Import FinancialProduct model
from rest_framework import generics # For ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny # AllowAny for public product listing

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
            {"error": "이미 존재하는 사용자명입니다."}, status=status.HTTP_400_BAD_REQUEST
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_financial_product(request):
    serializer = SavedFinancialProductSerializer(data=request.data, context={'request': request})
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unsave_financial_product(request, product_pk): # product_pk is the ID of the SavedFinancialProduct instance
    try:
        saved_product = SavedFinancialProduct.objects.get(pk=product_pk, user=request.user)
        saved_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except SavedFinancialProduct.DoesNotExist:
        return Response({"detail": "Saved product not found or permission denied."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_product_notification(request, saved_product_pk):
    """
    Toggles the 'notify_on_rate_change' status for a specific SavedFinancialProduct.
    Expects {'notify_on_rate_change': true/false} in the request body.
    """
    try:
        saved_product = SavedFinancialProduct.objects.get(pk=saved_product_pk, user=request.user)
    except SavedFinancialProduct.DoesNotExist:
        return Response({"detail": "Saved product not found or you do not have permission to modify it."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = NotificationSubscriptionSerializer(instance=saved_product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinancialProductListView(generics.ListAPIView):
    """
    API view to list financial products.
    Can be filtered by product_type query parameter (e.g., ?product_type=deposit)
    """
    serializer_class = FinancialProductSerializer
    permission_classes = [AllowAny] # Publicly accessible list

    def get_queryset(self):
        queryset = FinancialProduct.objects.prefetch_related('options').all()
        product_type = self.request.query_params.get('product_type', None)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        return queryset.order_by('kor_co_nm', 'fin_prdt_nm')


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
