from rest_framework import serializers
from api import models


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CourseModelSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedetail.course_slogan')
    # recommend_courses = serializers.CharField(source='coursedetail.recommend_courses.all')

    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'level_name', 'hours', 'course_slogan', 'recommend_courses']

    def get_recommend_courses(self,row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [ {'id': item.id, 'name': item.name} for item in recommend_list]