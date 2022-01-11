from rest_framework import serializers, fields
from api.models import User, Course, Certificate


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class CourseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    publishedAt = serializers.DateTimeField()

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        return Course.objects.create(**validated_data)


class CertificateSerializer(serializers.Serializer):
    course = serializers.CharField()
    user = serializers.CharField()
    completedDate = serializers.DateTimeField()
    startDate = serializers.DateTimeField()

    class Meta:
        model = Certificate
        fields = '__all__'

    def create(self, validated_data):
        return Certificate.objects.create(**validated_data)
