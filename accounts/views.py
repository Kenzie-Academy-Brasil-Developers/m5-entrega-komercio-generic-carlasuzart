
from rest_framework.views import APIView, Request, Response, status
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView
from accounts.models import Account
from accounts.permissions import OwnerAccount
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from accounts.serializers import AccountSerializer, IsAdmAccountSerializer, LoginSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

class LoginView(APIView):
    def post (self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user =authenticate(**serializer.validated_data)

        if not user:
            return Response ({"detail": "Invalid username or password"}, status.HTTP_400_BAD_REQUEST)

        token,_ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class AccountView(ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

class ListOrdersUsersView(ListAPIView):
    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[:num]
    
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class UpdateAccountView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [OwnerAccount]

    serializer_class = AccountSerializer

    queryset= Account.objects.all()

class IsAdmUpdateAccountView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminUser]

    serializer_class = IsAdmAccountSerializer

    queryset= Account.objects.all()


    