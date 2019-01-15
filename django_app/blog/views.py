from django.shortcuts import render
from blog import players

stats = players.getCurrentSeasonPlayerStats(8480829)

def home(request):
    context = {
        'stats': stats
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
