"""
Serializers for the user API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    # Meta class is used to define the configuration of the serializer
    class Meta:
        model = get_user_model()
        # fields to be included in the serializer
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # validated_data refers to the data that has been validated by the
    # serializer per rules in Meta class
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # overrides the default create method and uses the create_user method
        # from the UserManager class
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and returning it"""
        # password is optional, so we need to check if it's in
        # the validated_data
        password = validated_data.pop('password', None)
        # updates the user with the validated data
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        # added style to hide password when typing (optional)
        style={'input_type': 'password'},
        # added trim_whitespace to prevent trailing
        # whitespace (allows spaces in password)
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            # context is a dictionary of data passed to the serializer (header)
            request=self.context.get('request'),
            # authenticate() expects username
            # to be passed in; we use email instead
            username=email,
            password=password,
        )
        # if user is not authenticated, raise an error (wrong credentials)
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
