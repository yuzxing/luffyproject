from django.shortcuts import render, HttpResponse
from django.views import View
import json
from api.models import CourseCategory, CourseSubCategory, \
    DegreeCourse, Teacher, Scholarship, Course, CourseDetail, OftenAskedQuestion, \
    CourseOutline, CourseChapter, CourseSection, CourseSection, CourseSection


# Create your views here.


class CheckView(View):
    """
    练习题相关
    """
    def get(self, request):
        """
        .....
        :param request: 请求相关的数据
        :return: 给浏览器响应的内容
        """
        # a.查看所有学位课并打印学位课名称以及授课老师
        # degree_list = DegreeCourse.objects.all().values('name', 'teachers__name')
        # queryset = DegreeCourse.objects.all()
        # for row in queryset:
        #     row.name,row.teachers.all()


        # b.查看所有学位课并打印学位课名称以及学位课的奖学金
        # c_obj=DegreeCourse.objects.all()
        # for i in c_obj:
        #     print(i.name)
        #     print(i.degreecourse_price_policy.all().values('price'))

        # degree_list = DegreeCourse.objects.all()
        # for row in degree_list:
        #     print(row.name)
        #     scholarships = row.scholarship_set.all()
        #     for item in scholarships:
        #         print('------>',item.time_percent,item.value)


        # c. 展示所有的专题课
        # c_obj=Course.objects.filter(degree_course__isnull=True)
        # print(c_obj)
        # d. 查看id=1的学位课对应的所有模块名称

        # a_obj=DegreeCourse.objects.filter(id=1).values('course__name')
        # print(a_obj)

        # obj = DegreeCourse.objects.get(id=1)
        # course_list = obj.course_set.all()
        # print(course_list)
        #
        # course_list = Course.objects.filter(degree_course_id=1)
        # print(course_list)
        #

        #  e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
        # c_obj =Course.objects.filter(id=1)
        # print(c_obj.values('name'))
        # print(c_obj.first().get_level_display())
        # print(c_obj.values('coursedetail__why_study'))
        # print(c_obj.values('coursedetail__what_to_study_brief'))
        # print(c_obj.values('coursedetail__recommend_courses'))

        # obj = Course.objects.get(id=1)
        # print(obj.name)
        # print(obj.brief)
        # print(obj.get_level_display() )
        # print(obj.coursedetail.hours )
        # print(obj.coursedetail.why_study )
        # print(obj.coursedetail.recommend_courses.all() )



        # f.获取id = 1的专题课，并打印该课程相关的所有常见问题
        # c_obj = Course.objects.filter(id=1).first()
        # print(c_obj.asked_question.all().values('question'))

        # obj = Course.objects.get(id=1)
        # ask_list = obj.asked_question.all()
        # for item in ask_list:
        #     print(item.question,item.answer)


        # g.获取id = 1的专题课，并打印该课程相关的课程大纲
        # c_obj = Course.objects.filter(id=1)
        # print(c_obj.values('coursedetail__courseoutline__title'))

        # obj = Course.objects.get(id=1)
        # outline_list = obj.coursedetail.courseoutline_set.all()
        # for item in outline_list:
        #     print(item.title,item.content)
        #

        # h.获取id = 1的专题课，并打印该课程相关的所有章节
        # c_obj = Course.objects.filter(id=1)
        # print(c_obj.values('coursechapters__name'))

        # obj = Course.objects.get(id=1)
        # chapter_list = obj.xxxxx.all() # 默认obj.表名_set.all()
        # for item in chapter_list:
        #     print(item.name)

        # i.获取id = 1的专题课，并打印该课程相关的所有课时
        # 第1章·Python 介绍、基础语法、流程控制
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
        # 第1章·Python介绍、基础语法、流程控制
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
            # 01 - 课程介绍（一）
        # c_obj = Course.objects.filter(id=1)
        # for i in c_obj.values('coursechapters__chapter','coursechapters__name'):
        #     print(i.get('coursechapters__chapter'),i.get('coursechapters__name'))
        #     a_obj=CourseChapter.objects.filter(name=i.get('coursechapters__name'))
        #     for j in a_obj.values('coursesections__name'):
        #         print(j.get('coursesections__name'))



        # obj = Course.objects.get(id=1)
        # chapter_list = obj.xxxxx.all()
        # for chapter in chapter_list:
        #     print(chapter.name,chapter.coursesections.all())


        # 补充
        # section_list = CourseSection.objects.filter(chapter__course_id=1).values('id','name','chapter_id','chapter__name')
        # for item in section_list:
        #     print(item)

        """
        [
            {'chapter_id':1,'chapter__name':'美丽俏佳人','children':[ {'id':1, 'name':'课时1'}, {'id':1, 'name':'课时2'} ]},
            {'chapter_id':2,'chapter__name':'美丽俏佳狗','children':[]}
        ]
        """

        # i.获取id = 1的专题课，并打印该课程相关的所有的价格策略
        # c_obj = Course.objects.filter(id=1).first()
        # print(c_obj.price_policy.all())
        return HttpResponse('ok')
