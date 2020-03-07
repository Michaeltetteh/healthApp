import base64
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token


from accounts.helper import utils as helper_utils
from accounts.models import UserProfile
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        label="Email Address"
    )

    password = serializers.CharField(
        required=True,
        label="Password",
        style={'input_type': 'password'}
    )

    password_2 = serializers.CharField(
        required=True,
        label="Confirm Password",
        style={'input_type': 'password'}
    )

    first_name = serializers.CharField(
        required=True
    )

    last_name = serializers.CharField(
        required=True
    )

    gender = serializers.CharField(
        required=True
    )

    class Meta(object):
        model = User
        fields = ['first_name', 'last_name','username', 'email','gender', 'password', 'password_2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):

        user_data = {
            'username': validated_data.get('username'),
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name')
        }



        user = UserProfile.objects.create_user_profile(
                data=user_data,
                is_active=False,
                site=get_current_site(self.context['request']),
                send_email=True
            )

        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=False,allow_blank=True,write_only=True)

    email = serializers.EmailField(required=False,allow_blank=True,write_only=True,label="Email Address")

    token = serializers.CharField(allow_blank=True,read_only=True)

    password = serializers.CharField(required=True,write_only=True,style={'input_type': 'password'})

    class Meta(object):
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login.")

        user = User.objects.filter(
            Q(email=email) | Q(username=username)
        ).exclude(
            email__isnull=True
        ).exclude(
            email__iexact=''
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            token, created = Token.objects.get_or_create(user=user_obj)
            data['token'] = token
        else:
            raise serializers.ValidationError("User not active.")

        return data


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )

    def validate_email(self, value):
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):

    token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        uidb64, token = context.get('uidb64'), context.get('token')
        if uidb64 and token:
            uid = base_utils.base36decode(uidb64)
            self.user = self.get_user(uid)
            self.valid_attempt = self.token_generator.check_token(self.user, token)
        super(PasswordResetConfirmSerializer, self).__init__(*args, **kwargs)

    def get_user(self, uid):
        try:
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        label="New Password",
        write_only=True
    )

    new_password_2 = serializers.CharField(
        style={'input_type': 'password'},
        label="Confirm New Password",
        write_only=True
    )

    def validate_new_password_2(self, value):
        data = self.get_initial()
        new_password = data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate(self, data):
        if not self.valid_attempt:
            raise serializers.ValidationError("Operation not allowed.")
        return data


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'has_email_verified']

