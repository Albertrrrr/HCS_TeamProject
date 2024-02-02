from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render, redirect
from portal.models import User, PageResponse
from django.http import JsonResponse
import json


# Create your views here.
class FormDataSubmissionView(View):
    def post(self, request, *args, **kwargs):
        # 解析接收到的JSON数据
        try:
            data = json.loads(request.body)
            if hasattr(request, 'user') and request.user is not None:
                # 处理数据，例如保存到数据库
                response = PageResponse(user=request.user)
                for page, page_data in data.items():
                    page_data.pop('csrfmiddlewaretoken', None)
                    json_data = json.dumps(page_data)
                    if hasattr(response, f'{page}_responses'):
                        setattr(response, f'{page}_responses', json_data)
                    print("已保存：" + f"Processing {page}: {page_data}")

                response.save()
                # 现在可以直接使用request.user
                print("Current user id: ", request.user.id)

            return JsonResponse({'status': 'success', 'message': 'Data processed successfully.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data received.'}, status=400)


class SurveyView(View):
    gif_urls = {
        1: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF',
        2: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF',
        3: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF',
        4: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF',
        5: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF',
        6: 'https://storage.googleapis.com/hcsproject/2e134eda2c3612bde48d0492f66c2f75.GIF'
    }
    solution_list = {
        1: 'A. Alert Icon',
        2: 'B. Crystalize Filter',
        3: 'C. Dimming Filter',
        4: 'D. Fake Text Filter',
        5: 'E. Front Camera Preview',
        6: 'G. Grayscale Filter',
    }
    questions = [
        "该方案在多大程度上易于理解和使用？",
        "你主观上感觉该方案有效性如何？",
        "使用该方案在多大程度上令你感觉更安全？",
        "你认为该方案在多大程度上会引起尴尬或社交不适？",
        "你认为该方案的使用舒适度如何？",
        "你在多大程度上可能会在实际生活中使用该方案？",
        "你认为该方案是否有明显缺陷？（可选）"
    ]

    def get(self, request, page):
        if page < 1 or page > 6:
            return redirect('form', page=1)
        gif_url = self.gif_urls.get(page, '')
        solutionName = self.solution_list.get(page, "")
        context = {
            'page': page,
            'questions': self.questions,
            'gif_url': gif_url,
            'next_page': page + 1 if page < 6 else None,
            'prev_page': page - 1 if page > 1 else None,
            'solution_name': solutionName
        }
        return render(request, 'form.html', context)


class Quiz(View):
    questions = [
        "该方案在多大程度上易于理解和使用？",
        "你主观上感觉该方案有效性如何？",
        "使用该方案在多大程度上令你感觉更安全？",
    ]

    def get(self, request):
        context = {
            'questions': self.questions,
        }

        return render(request, 'quiz.html', context)

    def post(self, request, *args, **kwargs):
        try:
            # 解析JSON格式的请求体数据
            data = json.loads(request.body)
            if hasattr(request, 'user') and request.user is not None:
                page_response = PageResponse.objects.get(user=request.user)
                # 将接收到的数据转换为JSON字符串并保存到quiz字段
                page_response.quiz = json.dumps(data)
                page_response.save()
                print("已存入：", data)
                # 返回确认信息
                return JsonResponse({'status': 'success', 'message': 'Quiz responses updated successfully.'})

            else:
                # 如果用户未认证，返回错误信息
                return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'}, status=401)

        except PageResponse.DoesNotExist:
            # 如果找不到实例，返回错误信息
            return JsonResponse({'status': 'error', 'message': 'PageResponse instance not found.'}, status=404)
        except json.JSONDecodeError:
            # 如果JSON解析失败，返回错误信息
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data received.'}, status=400)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        email_value = request.POST.get('email', "")
        nickname = request.POST.get('nickname', "")
        try:
            if email_value and nickname:
                user = User(email=email_value, nickname=nickname)
                user.save()
                request.session['user_id'] = user.id  # 保存ID 到Session
                request.session['email'] = user.email
                return JsonResponse({"success": True})

        except IntegrityError:
            # 指出email 已经存在
            return JsonResponse({"error": "Email already used, please use another email address"}, status=400)
