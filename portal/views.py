from django.shortcuts import render

# Create your views here.
# portal return
def portal(request):
    return render(request,"index.html")


