from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPES = [
        ('movie', 'Movie'),
        ('webseries', 'Web Series'),
        ('shortfilm', 'Short Film'),
        ('social', 'Social Content'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    # optional local uploaded video for development (store in MEDIA_ROOT/videos)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200]
            slug = base
            counter = 1
            while Content.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('content_watch', kwargs={'slug': self.slug})

    @property
    def video_src(self):
        """Return the best available URL for the content's video.

        Order:
        1. uploaded FileField (MEDIA_URL)
        2. external video_url (assumed embeddable)
        3. project-level video folder (BASE_DIR / 'video') matching slug or title filename
        """
        # 1. uploaded file
        if self.video_file:
            try:
                return self.video_file.url
            except Exception:
                pass

        # 2. external URL
        if self.video_url:
            return self.video_url

        # 3. try project-level video folder (use slug with .mp4)
        # we avoid importing settings at module import time in case of circular imports
        from django.conf import settings
        import os
        name_candidates = [f"{self.slug}.mp4", f"{self.slug}.webm", f"{self.title}.mp4"]
        for name in name_candidates:
            path = os.path.join(settings.BASE_DIR, 'video', name)
            if os.path.exists(path):
                # build URL relative to VIDEO_URL
                return settings.VIDEO_URL + name

        return None


class SiteConfig(models.Model):
    """Simple single-row site configuration for name and logo."""
    site_name = models.CharField(max_length=100, default='withfamily')
    logo = models.ImageField(upload_to='site/', blank=True, null=True,
                             help_text='Logo displayed under navbar on main page')

    def __str__(self):
        return f"SiteConfig: {self.site_name}"

    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'