from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Question
from permissions import IsOwnerOrReadOnly
from django.core.paginator import Paginator
from rest_framework import status


class Home(APIView):
    """
    Shows all persons
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        persons = Person.objects.all()
        page_number = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('limit', 1)
        paginator = Paginator(persons, page_size)
        ser_data = PersonSerializer(instance=paginator.page(page_number), many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class QuestionListView(APIView):
    """
    Shows all question
    """
    permission_classes = [AllowAny, ]

    def get(self, request):
        questions = Question.objects.all()
        ser_data = QuestionSerializer(instance=questions, many=True).data
        return Response(data=ser_data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """
    Creates a new question
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = QuestionSerializer

    def post(self, request):
        ser_data = QuestionSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    """
    Updates a question
    """
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = QuestionSerializer

    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        ser_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    """
        Deletes a question
    """
    permission_classes = [IsOwnerOrReadOnly, ]

    def delete(self, request, pk):
        Question.objects.get(pk=pk).delete()
        return Response(data={"message": "question was deleted"}, status=status.HTTP_200_OK)
