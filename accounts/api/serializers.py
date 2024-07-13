from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.core.mail import send_mail
from django.conf import settings
from services.generator import CodeGenerator
from django.urls import reverse_lazy

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("email", "password")

    def get_user(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        return authenticate(email=email, password=password)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError({"error": "User not found"})

        if not user:
            raise serializers.ValidationError({"error": "Email or password is wrong"})

        if not user.is_active:
            raise serializers.ValidationError({"error": "This account is not activated"})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Password is wrong"})

        return super().validate(attrs)

    def create(self, validated_data):
        return self.get_user()

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return repr_


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "password_confirm")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Account with this email already exists"})

        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords should match"})

        if len(password) < 6:
            raise serializers.ValidationError({"error": "Password should contain 6 symbols at least"})

        return super().validate(attrs)

    def create(self, validated_data):
        password_confirm = validated_data.pop("password_confirm")

        user = User.objects.create(
            **validated_data, is_active=False,
            activation_code=CodeGenerator().create_activation_link_code(size=6, model_=User)
        )
        user.set_password(password_confirm)
        user.save()

        # sending verification mail
        message = f"Activation Code : {user.activation_code}"
        send_mail(
            "Jobify | Activation Mail",
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return user

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        uuid = urlsafe_base64_encode(smart_bytes(instance.id))
        repr_["uuid"] = uuid
        return repr_


class ActivationSerializer(serializers.ModelSerializer):
    activation_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("activation_code",)

    def validate(self, attrs):
        activation_code = attrs.get("activation_code")
        user = self.instance
        if not user.activation_code == activation_code:
            raise serializers.ValidationError({"error": "Wrong code."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.activation_code = None
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_


class CheckEmailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "There is no user with this e-mail address"})

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request")
        user_email = validated_data.get("email")
        user = User.objects.get(email=user_email)

        uuid = urlsafe_base64_encode(smart_bytes(user.id))

        link = request.build_absolute_uri(reverse_lazy("accounts:reset_password_complete", kwargs={"uuid": uuid}))

        message = f'You can reset password by clicking the link below: \n {link}'

        send_mail(
            "Dpopfood | Reset Password",
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({"error": "Passwords should match"})

        if len(password) < 6:
            raise serializers.ValidationError({"error": "Password should contain 6 symbols at least"})

        return attrs

    def validator_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"error": "Old password is not correct"})

        return value

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        tokens = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(tokens),
            "access": str(tokens)
        }
        return repr_


class ResetPasswordCompleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "password",
            "password_confirm"
        )

    def validate(self, attrs):
        user = self.instance
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if user.check_password(password):
            raise serializers.ValidationError({"error": "You used this password."})

        if password != password_confirm:
            raise serializers.ValidationError({"error": "Passwords should match"})

        if len(password) < 6:
            raise serializers.ValidationError({"error": "Password should contain 6 symbols at least"})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.get("password")
        instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        tokens = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(tokens),
            "access": str(tokens)
        }
        return repr_
