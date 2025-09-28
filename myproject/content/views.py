from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Content
from django.shortcuts import get_object_or_404

def home_view(request):
    featured = Content.objects.order_by('-created_at')[:6]
    return render(request, 'content/home.html', {'featured': featured})

def movies_view(request):
    movies = Content.objects.filter(content_type='movie')
    return render(request, 'content/movies.html', {'movies': movies})

def webseries_view(request):
    webseries = Content.objects.filter(content_type='webseries')
    return render(request, 'content/webseries.html', {'webseries': webseries})

def shortfilm_view(request):
    shortfilms = Content.objects.filter(content_type='shortfilm')
    return render(request, 'content/shortfilm.html', {'shortfilms': shortfilms})

def socialcontent_view(request):
    social_content = Content.objects.filter(content_type='social')
    return render(request, 'content/socialcontent.html', {'social_content': social_content})


@login_required
def watch_view(request, slug):
    item = get_object_or_404(Content, slug=slug)
    # use Content.video_src property which looks in MEDIA, external URL, then project video/
    video_src = item.video_src
    return render(request, 'content/watch.html', {'item': item, 'video_src': video_src})