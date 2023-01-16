from rest_framework import serializers

from app.models.answer import Answer
from app.models.question import Question

from app.serializers.answer import AnswerSerializer


class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "question_index", "text", "multi", "answers", "explanation")

    def create(self, validated_data):
        answer_data = validated_data.pop("answers")
        question = Question.objects.create(**validated_data)

        for data in answer_data:
            Answer.objects.create(question=question, **data)

        return question
