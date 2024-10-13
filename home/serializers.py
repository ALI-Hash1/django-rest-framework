from rest_framework import serializers
from .models import Question, Answer
from .custom_related_fields import UserEmailNameRelationalField


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    age = serializers.EmailField()
    email = serializers.CharField()


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    user = UserEmailNameRelationalField(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

    def get_answer(self, obj):
        answers = obj.answers.all()
        return AnswerSerializer(instance=answers, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
