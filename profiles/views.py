from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.

def profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    print(user)
    context = {
        'user': user
    }
    return render(request, "profiles/profile.html", context)