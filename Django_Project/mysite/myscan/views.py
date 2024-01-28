from django.shortcuts import render

from aip import AipImageClassify
import base64
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ParseError
from django.http import JsonResponse

from mysite.config import APP_ID, API_KEY, SECRET_KEY

# Create your views here.

# 创建百度植物识别API客户端对象
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)


class PhotoUploadView(APIView):
    # 定义解析器类列表，用于解析multipart/form-data类型和form表单类型的数据
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        try:
            photo = request.FILES.get('photo')  # 获取上传的照片文件
            if not photo:
                raise ParseError("No file was submitted")

            # 进行照片处理和其他逻辑操作

            # 调用百度植物识别接口
            image_data = photo.read()

            # 将图片转换为base64编码格式
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            result = client.plantDetect(image_base64)

            # 处理识别结果
            if 'result' in result and result['result']:
                plant_name = result['result'][0]['name']
                probability = result['result'][0]['score']
                # 构建植物信息界面URL
                plant_info_url = f"https://baike.baidu.com/item/{plant_name}"
                return JsonResponse(
                    {'plant_name': plant_name, 'probability': probability, 'plant_info_url': plant_info_url})
            else:
                return JsonResponse({'error': '未识别到植物'}, status=404)
        # 处理异常情况
        except ParseError as e:
            return JsonResponse({'error': str(e)}, status=400)
