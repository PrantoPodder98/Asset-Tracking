from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile, Company

@login_required
def create_company(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        user_profile = UserProfile.objects.get(user=request.user)
        Company.objects.create(user_profile=user_profile, name=company_name)
        return redirect('dashboard')  # Redirect to the user's dashboard or company page
    return render(request, 'create_company.html')

