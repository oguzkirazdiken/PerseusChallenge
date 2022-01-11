
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import UserSerializer, CourseSerializer, CertificateSerializer



@api_view(['POST'])
def user_create(request):
    user_serializer = UserSerializer(data=request.data, many=True)
    if user_serializer.is_valid():
        user_serializer.save()

    return Response(user_serializer.data)


@api_view(['POST'])
def course_create(request):
    course_serializer = CourseSerializer(data=request.data, many=True)
    if course_serializer.is_valid():
        course_serializer.save()

    return Response(course_serializer.data)


@api_view(['POST'])
def certificate_create(request):
    certificate_serializer = CertificateSerializer(data=request.data, many=True)
    if certificate_serializer.is_valid():
        certificate_serializer.save()

    return Response(certificate_serializer.data)
