import json
import redis
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser  # 解析器

from api import models
from api.utils.response import BaseResponse


CONN = redis.Redis(host='192.168.11.142', port='6379')  # 连接 redis
USER_ID = 2  # 设置用户固定ID


class ShoppingCarView(ViewSetMixin, APIView):
    # parser_classes = [JSONParser]
    # parser_classes = [JSONParser, FROMParer]

    def list(self, request, *args, **kwargs):
        """
        查看购物车信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 接受用户选中的课程ID和价格策略ID
        2. 判断合法性
            - 课程是否存在？
            - 价格策略是否合法？
        3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        注意：用户ID=1
        """
        ret = {"code": 10000, "data": None, "error": None}  # 设置状态码
        try:
            shopping_car_course_list = []
            # pattern = "shopping_car_%s_*"%(USER_ID)
            pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, "*")  # redis最外面的键

            user_key_list = CONN.keys(pattern)
            for key in user_key_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                shopping_car_course_list.append(temp)
            ret['data'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 10005
            ret['error'] = '获取购物车数据失败'

        return Response(ret)

    def create(self, request, *args, **kwargs):
        """
        加入购物车
        1. 接受用户选中的课程ID和价格策略ID
        2. 判断合法性
            - 课程是否存在？
            - 价格策略是否合法？
        3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        注意：用户ID=1
        """
        # 1.接受用户选中的课程ID和价格策略ID
        course_id = request.data.get('courseid')  # 从data中拿到courseid
        policy_id = request.data.get('policyid')  # 从data中拿到policyid
        # 2,判断合法性
        #   -- 判断课程是否存在 ？
        #   -- 价格是否合法 ？

        # 2.1 课程是否存在?
        course = models.Course.objects.filter(id=course_id).first()  # 从数据库中得到课程的id
        if not course:
            return Response({'code': 10001, 'error': '课程不存在'})

        # 2.2 价格策略是否合法?
        price_policy_queryset = course.price_policy.all()  # 得到课程id 对应的所有价格策略
        price_policy_dict = {}  # 建一个空的 价格策略字典
        for item in price_policy_queryset:  # 循环得到的价格策略
            temp = {  # 把价格策略循环创建temp字典中
                'id': item.id,
                'price': item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp   # 把价格策略的id 对应循环的价格策略temp
        if policy_id not in price_policy_dict:  # 判断价格策略是否存在
            return Response({'code': 10002, 'error': '二笔, 价格策略不存在'})

        # 3, 把商品和价格策略信息放入购物车 SHOPPING_CAR
        """
        {
        shopping_car_用户ID_课程ID:{
        id: 课程ID,
        name: 课程名称,
        img: 课程图片,
        default: 默认选中的价格策略,
        price_list: 所有的价格策略
        
        }
        }
        """
        pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, "*")
        keys = CONN.keys(pattern)
        if keys and len(keys) >= 1000:
            return Response({'code': 10010, 'error': '请先去结算,再来购买'})
        # key = "shopping_car_%s_%s" % (USER_ID, course_id)
        key = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*')
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'default_price_id', policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))

        CONN.expire(key, 30*60)

        return Response({'code': 10000, 'data': '购买成功'})

    def update(self, request, *args, **kwargs):
        """更改
        1, 获取课程的ID, 要修改的价格策略的ID
        2, 校验合法性(去redis中)
        """
        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None
            # key = 'shopping_car_%s_%s' % (USER_ID, course_id)
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id)

            if not CONN.exists(key):
                response.code = 10007
                response.error = '课程不存在'
                return Response(response.dict)
            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
            if policy_id not in price_policy_dict:
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)
            CONN.hset(key, 'default_price_id', policy_id)
            CONN.expire(key, 20*60)  # 设定时间 消失
            response.data = '修改成功'
        except Exception as e:
            response.code = 10009
            response.error = '修改失败'
        return Response(response.dict)

    def destroy(self, request, *args, **kwargs):
        """
        删除购物车里某个课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()
        try:
            courseid = request.GET.get('courseid')
            # key = "shopping_car_%s_%s" % (USER_ID, courseid)
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid)

            CONN.delete(key)
            response.data = '删除成功'
        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
        return Response(response.dict)


