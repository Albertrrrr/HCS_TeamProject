from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render, redirect
from portal.models import User
from django.http import JsonResponse


# Create your views here.
# portal return
class ReturnView(View):
    def get(self, request, *args, **kwargs):
        if hasattr(request, 'user') and request.user is not None:
            # 现在可以直接使用request.user
            print("Current user id: ", request.user.id)  # 举例使用用户的昵称
            # 现在你可以访问user对象，进行后续操作
        return render(request, "form.html")

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
                request.session['user_id'] = user.id  # 保存用户ID到会话
                request.session['email'] = user.email  # 也可以保存邮箱或其他信息
                return JsonResponse({"success": True})
        except IntegrityError:
            # 如果出现错误（例如，邮箱已存在）
            return JsonResponse({"error": "Email already used, please use another email address"}, status=400)

