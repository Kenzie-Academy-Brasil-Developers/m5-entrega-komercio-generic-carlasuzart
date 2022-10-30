from rest_framework import serializers


from accounts.models import Account

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    id = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    
    class Meta:
        model = Account
        fields = ['id','username', 'password', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_superuser', 'is_active']
        ready_only_fields = ['id','is_active', 'is_superuser', 'date_joined']
        
        
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class IsAdmAccountSerializer(serializers.ModelSerializer):

    is_superuser = serializers.BooleanField(read_only=True)
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_seller = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Account
        fields = ['id','username', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_superuser', 'is_active']
       
        
        
    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
