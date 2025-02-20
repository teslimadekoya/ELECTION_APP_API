from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        validate_password(data['password'])
        return data
    
    def create(self, validated_data):
        try:
            validated_data.pop('password2', None)
            
            user = User.objects.create_user(
                username= validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                middle_name=validated_data['middle_name'],
                last_name=validated_data['last_name'],
                state_of_origin=validated_data['state_of_origin'],
                address=validated_data['address'],
                occupation=validated_data['occupation'],
                gender=validated_data['gender'],
                phone_number=validated_data['phone_number'],
                role=validated_data['role']
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})


