from django.db import models
class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'}"

class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()
    position = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Testimonial by {self.name}"
