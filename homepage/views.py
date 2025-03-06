from django.shortcuts import render

# Create your views here.

def index(request):
    """
    Render the homepage, using the index.html template in the homepage app.
    """
    return render(request, 'homepage/index.html')