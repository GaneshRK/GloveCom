from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Testimonial
def home(request):
    testimonials = Testimonial.objects.all()[:4]
    context = {'testimonials': testimonials, 'achievement': 'Top 18 in Indian Startup Rankings'}
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:contact_success')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'core/contact_success.html')
