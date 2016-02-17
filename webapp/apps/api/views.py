# -*- coding: utf-8 -*-s


import datetime
import random
import requests
import hashlib
import re
import traceback
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.conf import settings
from oscar.core.loading import get_model




from webapp.apps.public.send_message import send_message

from webapp.apps.accounts.models import UserProfile, Captcha
from webapp.apps.accounts.forms import local_mobile_phone_validator



Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Basket = get_model('basket', 'Basket')
Line = get_model('basket', 'Line')
Partner = get_model('partner', 'Partner')
ProductOrder = get_model('commission', 'ProductOrder')
OrderInfo = get_model('commission', 'OrderInfo')
app_secret_key = getattr(settings, 'APP_SECRET_KEY', 'aeb11af7b1750854cb6217cf33e1a5e48826369c1e255c33ff655ff3fc938e')


# 验证sign
def check_sign(request):
    device_id = request.data.get('device_id', '')
    sign = request.data.get('sign', '')
    if device_id and sign:
        correct_sign = hashlib.md5(''.join([device_id, app_secret_key, 'lantubaihuo'])).hexdigest()
        if sign == correct_sign:
            return (True, 199, u'签名正确')
        else:
            return (False, 102, u'签名错误')
    return (False, 104, u'缺少关键参数')


# 验证密码
def check_password(password):
    if re.search(r'^(?![^a-zA-Z]+$)(?!\D+$).{6,15}$', password):
        return True
    else:
        return False


# 分页
def paging(total_data_number, page_nubmer, data_number):
    max_page_number = int(total_data_number) / int(data_number)

    if (int(page_nubmer)-1) >= max_page_number:
        current_page_number = max_page_number
    else:
        current_page_number = int(page_nubmer) - 1
    # current_page_number = page_nubmer
    start_data_number = current_page_number * int(data_number)
    end_data_number = start_data_number + int(data_number)
    total_page = max_page_number + 1
    return (current_page_number, start_data_number, end_data_number, total_page)




# 注册前获取验证码
class APIGetsmscodeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            mobile = request.POST.get('mobile', '')
            if not local_mobile_phone_validator(mobile):
                msg = u'手机号码不合法。'
                result['code'] = 234
                result['msg'] = msg
            else:
                try:
                    userprofile = UserProfile.objects.get(mobile_phone=mobile)
                    msg = u'此号码已经被注册。'
                    result['code'] = 233
                    result['msg'] = msg
                except UserProfile.DoesNotExist:
                    new_captcha = random.randint(100000, 999999)
                    current_captcha = Captcha.objects.get_or_create(recipient=mobile)[0]
                    current_captcha.captcha = new_captcha
                    current_captcha.deadline_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                    current_captcha.save()
                    send_content = u'您的验证码是：%s。请不要把验证码泄露给其他人。' % str(new_captcha)
                    if mobile:
                        (response_code, response_msg) = send_message(mobile, send_content)
                        if response_code == '2':
                            result['code'] = 199
                            result['msg'] = u'发送成功'
                            result['validity_time'] = '600'
                        else:
                            result['code'] = 232
                            result['msg'] = u'发送失败'
                    '''
                    result['code'] = 199
                    result['msg'] = u'发送成功'
                    result['validity_time'] = '600'
                    '''
            return Response(result)
        except Exception, e:
            return Response({'msg': u'发送失败', 'code': 232})


# 测试token
class APITestTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        result = {}
        result['code'] = 231
        result['msg'] = u'成功'
        return Response(result)

# 注册
class APIRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            password = request.POST.get('password', '')
            mobile = request.POST.get('mobile', '')
            introducer = request.POST.get('introducer', '')
            verify_code = request.POST.get('verify_code', '')
            if password and mobile and verify_code:
                if not local_mobile_phone_validator(mobile):
                    msg = u'手机号码不合法。'
                    result['code'] = 234
                    result['msg'] = msg
                    return Response(result)
                if not check_password(password):
                    result['code'] = 243
                    result['msg'] = u'密码不符合要求。'
                    return Response(result)
                if User.objects.filter(username=mobile).count() != 0:
                    result['code'] = 233
                    result['msg'] = u'此号码已经被注册。'
                    return Response(result)
                try:
                    userprofile = UserProfile.objects.get(mobile_phone=mobile)
                    result['code'] = 233
                    result['msg'] = u'此号码已经被注册。'
                except UserProfile.DoesNotExist:
                    try:
                        current_mobile_captcha = Captcha.objects.get(recipient=mobile)
                        if current_mobile_captcha.deadline_time < now():
                            result['code'] = 235
                            result['msg'] = u'验证码已过期。'
                            return Response(result)
                        if current_mobile_captcha.captcha != verify_code:
                            result['code'] = 237
                            result['msg'] = u'验证码不正确。'
                        else:
                            new_user = User.objects.create(username=mobile, password=make_password(password))
                            try:
                                current_userprofile = new_user.userprofile
                                current_userprofile.mobile_phone = mobile
                                current_userprofile.introducer = introducer
                            except UserProfile.DoesNotExist:
                                current_userprofile = UserProfile.objects.create(user=new_user, mobile_phone=mobile)
                            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                                current_ip =  request.META['HTTP_X_FORWARDED_FOR']
                            else:
                                current_ip = request.META['REMOTE_ADDR']
                            current_userprofile.register_ip = current_ip
                            current_userprofile.save()
                            result['code'] = 199
                            result['msg'] = u'注册成功。'
                    except Captcha.DoesNotExist:
                        result['code'] = 237
                        result['msg'] = u'验证码不正确。'
            return Response(result)
        except Exception, e:
            print e
            return Response({'msg': u'注册失败', 'code': 236})


# 登录
class APILoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            username = request.data.get('username', '')
            password = request.data.get('password', '')
            # login
            try:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    # get_token
                    http_host = request.get_host()
                    path_url = reverse('api:api_auth')
                    get_token_url = ''.join(['http://', http_host, path_url])
                    get_toekn_params = {'username': username, 'password': password}
                    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
                    res = requests.post(get_token_url, data=get_toekn_params, headers=headers)
                    token_json = res.json()
                    if token_json.has_key('token'):
                        token = token_json.get('token')     # token
                        try:
                            current_userprofile = user.userprofile
                        except UserProfile.DoesNotExist:
                            current_userprofile = UserProfile.objects.create(user=user)
                        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                            current_ip =  request.META['HTTP_X_FORWARDED_FOR']
                        else:
                            current_ip = request.META['REMOTE_ADDR']
                        current_userprofile.register_ip = current_ip
                        current_userprofile.save()

                        mobile = current_userprofile.mobile_phone
                        uid = current_userprofile.uid
                        nickname = current_userprofile.nickname
                        sex = current_userprofile.sex
                        try:
                            avatar = ''.join(['http://', http_host, current_userprofile.avatar.url])
                        except ValueError:
                            avatar = ''
                        email = user.email
                        if current_userprofile.birthday:
                            birthday = current_userprofile.birthday.strftime('%Y%m%d')
                        else:
                            birthday = ''
                        userinfo = {'username': username,
                                    'uid': uid,
                                    'nickname': nickname,
                                    'mobile': mobile,
                                    'sex': sex,
                                    'avatar': avatar,
                                    'email': email,
                                    'birthday': birthday,
                                    'token': token}
                        result['code'] = 199
                        result['msg'] = u'用户登录成功'
                        result['userinfo'] = userinfo
                    else:
                        result['code'] = 223
                        result['msg'] = u'密码错误'
                else:
                    result['code'] = 223
                    result['msg'] = u'密码错误'
            except User.DoesNotExist:
                result['code'] = 222
                result['msg'] = u'用户名不存在'
            return Response(result)
        except Exception, e:
            print e
            return Response({'msg': str(e), 'errcode':1})


# 获取图片验证码
class APIGetimgverifycodeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            mobile = request.POST.get('mobile', '')
            if not local_mobile_phone_validator(mobile):
                msg = u'手机号码不合法。'
                result['code'] = 234
                result['msg'] = msg
                return Response(result)
            else:
                try:
                    userprofile = UserProfile.objects.get(mobile_phone=mobile)
                    current_key = CaptchaStore.generate_key()
                    image_url = captcha_image_url(current_key)
                    http_host = request.get_host()
                    img = ''.join(['http://', http_host, image_url])
                    current_store = CaptchaStore.objects.get(hashkey=current_key)
                    img_value = current_store.challenge

                    result['code'] = 199
                    result['msg'] = u'获取图片验证码成功'
                    result['img'] = img
                    result['imgvalue'] = img_value
                except UserProfile.DoesNotExist:
                    result['code'] = 240
                    result['msg'] = u'不存在使用这个手机号的用户'
            return Response(result)
        except Exception, e:
            traceback.print_exc()
            return Response({'msg': u'获取图片验证码失败', 'code': 238})


# 忘记密码，发送手机短信验证码
class APIFindpwdView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            mobile = request.POST.get('mobile', '')
            if not local_mobile_phone_validator(mobile):
                msg = u'手机号码不合法。'
                result['code'] = 234
                result['msg'] = msg
                return Response(result)
            else:
                try:
                    userprofile = UserProfile.objects.get(mobile_phone=mobile)
                    new_captcha = random.randint(100000, 999999)
                    current_captcha = Captcha.objects.get_or_create(recipient=mobile)[0]
                    current_captcha.captcha = new_captcha
                    current_captcha.deadline_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
                    current_captcha.save()
                    send_content = u'您的验证码是：%s。请不要把验证码泄露给其他人。' % str(new_captcha)
                    (response_code, response_msg) = send_message(mobile, send_content)
                    if response_code == '2':
                        result['code'] = 199
                        result['msg'] = u'状态正常，发送验证码到%s' % mobile
                    else:
                        result['code'] = 239
                        result['msg'] = u'发送失败'
                except UserProfile.DoesNotExist:
                    result['code'] = 240
                    result['msg'] = u'不存在使用这个手机号的用户'
            return Response(result)
        except Exception, e:
            return Response({'msg': str(e), 'errcode':1})


# 重置密码
class APIResetpwdView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            mobile = request.POST.get('mobile', '')
            new_password = request.POST.get('newpwd', '')
            re_password = request.POST.get('repwd', '')
            captcha = request.POST.get('captcha', '')
            if not local_mobile_phone_validator(mobile):
                msg = u'手机号码不合法。'
                result['code'] = 234
                result['msg'] = msg
                return Response(result)
            print new_password,re_password,captcha
            if new_password and re_password and captcha:
                try:
                    if new_password != re_password:
                        result['code'] = 241
                        result['msg'] = u'两次输入的密码不一致。'
                        return Response(result)
                    if not check_password(new_password):
                        result['code'] = 243
                        result['msg'] = u'密码不符合要求。'
                        return Response(result)

                    userprofile = UserProfile.objects.get(mobile_phone=mobile)
                    try:
                        current_mobile_captcha = Captcha.objects.get(recipient=mobile)
                        if current_mobile_captcha.captcha != captcha:
                            result['code'] = 237
                            result['msg'] = u'验证码不正确。'
                            return Response(result)
                        if current_mobile_captcha.deadline_time < now():
                            result['code'] = 235
                            result['msg'] = u'验证码已过期。'
                            return Response(result)
                        else:
                            current_user = userprofile.user
                            password = make_password(new_password)
                            current_user.password = password
                            current_user.save()
                            result['code'] = 199
                            result['msg'] = u'重置密码成功。'
                    except Captcha.DoesNotExist:
                        result['code'] = 237
                        result['msg'] = u'验证码不正确。'
                        return Response(result)
                except UserProfile.DoesNotExist:
                    result['code'] = 240
                    result['msg'] = u'不存在使用这个手机号的用户'
            else:
                result['code'] = 104
                result['msg'] = u'缺少关键参数'
            return Response(result)
        except Exception, e:
            return Response({'msg': u'重置密码异常', 'code': 242})


# 验证用户名唯一性
class APICheckusernameView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            uid = request.POST.get('uid', '')
            username = request.POST.get('username', '')
            if uid and username:
                try:
                    userprofile = UserProfile.objects.get(uid=uid)
                except UserProfile.DoesNotExist:
                    result['code'] = 251
                    result['msg'] = u'不存在这个uid'
                    return Response(result)
                try:
                    user = User.objects.get(username=username)
                    result['code'] = 256
                    result['msg'] = u'该用户名已经被注册过了。'
                except User.DoesNotExist:
                    result['code'] = 199
                    result['msg'] = u'该用户名可用。'
            else:
                result['code'] = 104
                result['msg'] = u'缺少关键参数'
            return Response(result)
        except Exception, e:
            return Response({'msg': str(e), 'errcode':1})


# 修改用户名
class APIUpdateusernameView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg
            return Response(result)
        try:
            uid = request.POST.get('uid', '')
            username = request.POST.get('username', '')
            if uid and username:
                try:
                    userprofile = UserProfile.objects.get(uid=uid)
                    if userprofile.username_checked:
                        result['code'] = 257
                        result['msg'] = u'该用户的用户名已经被修改过了'
                        return Response(result)
                except UserProfile.DoesNotExist:
                    result['code'] = 251
                    result['msg'] = u'不存在这个uid'
                    return Response(result)
                try:
                    user = User.objects.get(username=username)
                    result['code'] = 256
                    result['msg'] = u'该用户名已经被注册过了。'
                except User.DoesNotExist:
                    current_user = userprofile.user
                    current_user.username = username
                    current_user.save()
                    userprofile.username_checked = True
                    userprofile.save()
                    result['code'] = 199
                    result['msg'] = u'更新用户名成功。'
            else:
                result['code'] = 104
                result['msg'] = u'缺少关键参数'
            return Response(result)
        except Exception, e:
            return Response({'msg': str(e), 'errcode':1})


#订单列表            
class APIGetOrdersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg 
            return Response(result)
        try:
            result = {}
            user = request.user
            page_number = request.POST.get('page_number', 1)
            data_number = request.POST.get('data_number', 20)
            status_id = int(request.POST.get('status_id', 0))
            try:
                page_number = int(page_number)
                data_number = int(data_number)
            except ValueError:
                result['code'] = 662
                result['msg'] = u'分页参数异常'
                return Response(result)
            if (page_number <= 0) or (data_number <= 0):
                result['code'] = 662
                result['msg'] = u'分页参数异常。'
                return Response(result)
            all_order = ProductOrder.objects.filter(user=user).order_by('-created_datetime')
            if status_id == 1:
                all_order = all_order.filter(status__in=[0,1,3])
            if status_id == 2:
                all_order = all_order.filter(status__in=[2,6,7])
            total_data_number = len(all_order)
            (current_page_number, start_data_number, end_data_number, total_page) = paging(total_data_number,
                                                                                page_number,
                                                                                data_number)
            current_order_list = all_order[start_data_number: end_data_number]
            datalist = []
            for order in current_order_list:
                STATUS_CHOICES = ((0, u'未支付'), (1, u'支付中'), (2, u'支付成功'),
                      (3, u'支付失败'), (4, u'已关闭'), (5, u'已撤销'), (6, u'未发货'), (7, u'已发货'), (8, u'部分提货'), (9, u'已提货'))
                order_status_id = order.status
                order_status_name = STATUS_CHOICES[order_status_id][1]
                if order.effective == False:
                    order_status_id = 5
                    order_status_name = u"已撤消"
                all_info = order.order_info.all()
                img_list = [info.product.img_url_or_none for info in all_info]
                product_num = sum([info.product_num for info in all_info])
                order_info = {"order_id":order.id,"order_no":order.order_no,"order_status_id":order_status_id,"order_status_name":order_status_name,"detail":order.detail,"amount":order.amount,"img_list":img_list,"product_num":product_num}
                datalist.append(order_info)
            result['code'] = 199
            result['msg'] = u'获取我的订单成功'
            result['current_page'] = current_page_number + 1
            result['total_page'] = total_page
            result['order_list'] = datalist
            return Response(result)
        except:
            traceback.print_exc()
            result['code'] = 661
            result['msg'] = u"获取我的订单失败"
            return Response(result)
        
    
#订单详情         
class APIGetOrderDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, order_id):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg 
            return Response(result)
        try:
            order = ProductOrder.objects.get(id=order_id)
            STATUS_CHOICES = ((0, u'未支付'), (1, u'支付中'), (2, u'支付成功'),
                  (3, u'支付失败'), (4, u'已关闭'), (5, u'已撤销'), (6, u'未发货'), (7, u'已发货'), (8, u'部分提货'), (9, u'已提货'))
            order_status_id = order.status
            order_status_name = STATUS_CHOICES[order_status_id][1]
            if order.effective == False:
                order_status_id = 5
                order_status_name = u"已撤消"
            if order.pickup_type == 1:
                pickup_type_name = u"自提"
            elif order.pickup_type == 2:
                pickup_type_name = u"物流"
            datalist = []
            all_info = order.order_info.all()
            for info in all_info:
                product = info.product
                product_group = product.product_group
                if product_group:
                    product_group_attr_count = product_group.attr.count()
                    if product_group_attr_count == 2:
                        first_attr = product_group.attr.all().order_by('index')[0]
                        second_attr = product_group.attr.all().order_by('index')[1]
                        first_attr_name = first_attr.name
                        second_attr_name = second_attr.name
                        cur_first_attr_value = ProductAttributeValue.objects.get(attribute=first_attr,product=product).value_text
                        cur_second_attr_value = ProductAttributeValue.objects.get(attribute=second_attr,product=product).value_text
                    elif product_group_attr_count == 1:
                        first_attr = product_group.attr.all().order_by('index')[0]
                        first_attr_name = first_attr.name
                        second_attr_name = ""
                        cur_first_attr_value = ProductAttributeValue.objects.get(attribute=first_attr,product=product).value_text
                        cur_second_attr_value = ""
                else:
                    first_attr_name = ""
                    second_attr_name = ""
                    cur_first_attr_value = ""
                    cur_second_attr_value = ""
                try:
                    img_url = product.primary_image().original.url
                except:
                    img_url = ""
                one_product_info = {"product_upc":product.upc,"product_name":product.title,"attribute_first_name":first_attr_name,
                                    "attribute_second_name":second_attr_name,"cur_first_attr_value":cur_first_attr_value,
                                    "cur_second_attr_value":cur_second_attr_value,"price":info.price,"order_num":info.product_num,
                                    "img_url":img_url}
                datalist.append(one_product_info)
            order_info = {"order_no":order.order_no,"order_status_id":order_status_id,"order_status_name":order_status_name,"addr":order.receive_addr.address,"province":order.receive_addr.province.name,"city":order.receive_addr.city.name,"district":order.receive_addr.district.name,
                          "consignee":order.receive_addr.consignee,"mobile_phone":order.receive_addr.mobile_phone,"email":order.receive_addr.email,"pickup_type_id":order.pickup_type,"pickup_type_name":pickup_type_name,"amount":order.amount,"product_price":order.product_price,"express_fee":order.express_fee,"pickup_fee":order.pickup_fee,"datalist":datalist}
            result['code'] = 199
            result['msg'] = u'获取订单成功'
            result['order_info'] = order_info
            return Response(result)
        except ProductOrder.DoesNotExist:
            result['code'] = 663
            result['msg'] = u'订单不存在'
            return Response(result)
        except:
            traceback.print_exc()
            result['code'] = 662
            result['msg'] = u'获取订单失败'
            return Response(result)
        
        
#取消订单     
class APICancelOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, order_id):
        result = {}
        (check_sign_result, check_code, check_msg) = check_sign(request)
        if not check_sign_result:
            result['code'] = check_code
            result['msg'] = check_msg 
            return Response(result)
        try:
            order = ProductOrder.objects.get(id=order_id)
            order.effective = False
            order.save()
            result['code'] = 199
            result['msg'] = u'取消订单成功'
            return Response(result)
        except ProductOrder.DoesNotExist:
            result['code'] = 663
            result['msg'] = u'订单不存在'
            return Response(result)
        except:
            traceback.print_exc()
            result['code'] = 662
            result['msg'] = u'取消订单失败'
            return Response(result)
            
        
def floatformat(flt):
    if flt:
        try:
            return "%.2f" % flt
        except:
            return flt
    else:
        return flt

