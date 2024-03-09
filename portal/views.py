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
        try:
            data = json.loads(request.body)
            if hasattr(request, 'user') and request.user is not None:
                response = PageResponse(user=request.user)
                for page, page_data in data.items():
                    page_data.pop('csrfmiddlewaretoken', None)
                    json_data = json.dumps(page_data)
                    if hasattr(response, f'{page}_responses'):
                        setattr(response, f'{page}_responses', json_data)
                    print("Save：" + f"Processing {page}: {page_data}")

                response.save()
                print("Current user id: ", request.user.id)

            return JsonResponse({'status': 'success', 'message': 'Data processed successfully.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data received.'}, status=400)


class SurveyView(View):
    gif_urls = {
        1: 'https://storage.googleapis.com/ithcs/Alert-Icon.gif',
        2: 'https://storage.googleapis.com/ithcs/A_1%20-original-original.gif',
        3: 'https://storage.googleapis.com/ithcs/Front-LED-Flash.gif',
        4: 'https://storage.googleapis.com/ithcs/Fake-Text-Filter.gif',
        5: 'https://storage.googleapis.com/ithcs/Low-Brightness.gif',
        6: 'https://storage.googleapis.com/ithcs/Preset-modes-of-vibration-3.gif'
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
            data = json.loads(request.body)
            if hasattr(request, 'user') and request.user is not None:
                page_response = PageResponse.objects.get(user=request.user)
                page_response.quiz = json.dumps(data)
                page_response.save()
                print("Save：", data)
                return JsonResponse({'status': 'success', 'message': 'Quiz responses updated successfully.'})

            else:
                return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'}, status=401)

        except PageResponse.DoesNotExist:

            return JsonResponse({'status': 'error', 'message': 'PageResponse instance not found.'}, status=404)
        except json.JSONDecodeError:

            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data received.'}, status=400)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        email_value = request.POST.get('email', "")
        nickname = request.POST.get('nickname', "")
        code = request.POST.get('code',"")
        if code == "UofGHCS2024.":
            try:
                if email_value and nickname:
                    user = User(email=email_value, nickname=nickname)
                    user.save()
                    request.session['user_id'] = user.id
                    request.session['email'] = user.email
                    return JsonResponse({"success": True})

            except IntegrityError:

                return JsonResponse({"error": "Email already used, please use another email address"}, status=400)
        else:
            return JsonResponse({"error": "Invitation Code error, please enter right code"}, status=400)
