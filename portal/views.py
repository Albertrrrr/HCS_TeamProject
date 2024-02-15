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
        1: 'https://storage.googleapis.com/hcsproject/Alert-Icon.gif',
        2: 'https://storage.googleapis.com/hcsproject/A_1%20-original-original.gif',
        3: 'https://storage.googleapis.com/hcsproject/Front-LED-Flash.gif',
        4: 'https://storage.googleapis.com/hcsproject/Fake-Text-Filter.gif',
        5: 'https://storage.googleapis.com/hcsproject/Low-Brightness.gif',
        6: 'https://storage.googleapis.com/hcsproject/Preset-modes-of-vibration-3.gif'
    }
    solution_list = {
        1: 'A. Alert Icon',
        2: 'B. Front Camera Preview',
        3: 'C. Front LED Flash',
        4: 'D. Fake Text Filter',
        5: 'E. Low Brightness',
        6: 'F. Preset Modes Vibration',
    }
    questions = [
        "To what extent is the solution easy to understand and use?",
        "How effective do you subjectively feel the solution is?",
        "How far did using the solution make you feel safer?",
        "To what extent do you think the solution will cause embarrassment or social discomfort?",
        "What do you think about the comfort level of using the solution?",
        "To what extent are you likely to use the solution in real life?",
        "Do you see any obvious flaws in the solution? (Optional)"
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
        "Which solutions are you most satisfied with?",
        "Would you mind to explain the choice for the most satisfied ? (Optional)",
        "Which solutions are you least satisfied with?",
        "Would you mind to explain the choice for the least satisfied ? (Optional)",
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
