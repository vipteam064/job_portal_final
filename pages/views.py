from django.shortcuts import render

# Create your views here.
def icons_test_view(request):
    return render(request, 'pages/icons_test.html')
