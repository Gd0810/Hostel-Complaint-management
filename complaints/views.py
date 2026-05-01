from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When, IntegerField
from functools import wraps
from .models import CustomUser, Complaint

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin_user():
            messages.error(request, 'Access denied. Admin only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_admin_user():
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def priority_order():
    return Case(
        When(priority='High', then=1),
        When(priority='Medium', then=2),
        When(priority='Low', then=3),
        output_field=IntegerField()
    )

def register_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard' if not request.user.is_admin_user() else 'admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'register.html')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role='student')
        login(request, user)
        messages.success(request, f'Welcome, {username}! Your account has been created.')
        return redirect('student_dashboard')
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('student_dashboard' if not request.user.is_admin_user() else 'admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin_dashboard' if user.is_admin_user() else 'student_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@student_required
def student_dashboard(request):
    status_filter = request.GET.get('status', '')
    search_q = request.GET.get('q', '')
    complaints = Complaint.objects.filter(user=request.user)
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if search_q:
        complaints = complaints.filter(title__icontains=search_q)
    complaints = complaints.annotate(p_order=priority_order()).order_by('p_order', '-created_at')
    stats = {
        'total': Complaint.objects.filter(user=request.user).count(),
        'pending': Complaint.objects.filter(user=request.user, status='Pending').count(),
        'in_progress': Complaint.objects.filter(user=request.user, status='In Progress').count(),
        'resolved': Complaint.objects.filter(user=request.user, status='Resolved').count(),
    }
    return render(request, 'student_dashboard.html', {
        'complaints': complaints, 'stats': stats,
        'status_filter': status_filter, 'search_q': search_q
    })

@student_required
def submit_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority = request.POST.get('priority', 'Medium')
        if not title or not description:
            messages.error(request, 'Title and description are required.')
            return render(request, 'submit_complaint.html')
        if priority not in ['High', 'Medium', 'Low']:
            priority = 'Medium'
        Complaint.objects.create(user=request.user, title=title, description=description, priority=priority)
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('student_dashboard')
    return render(request, 'submit_complaint.html')

@admin_required
def admin_dashboard(request):
    priority_filter = request.GET.get('priority', '')
    status_filter = request.GET.get('status', '')
    search_q = request.GET.get('q', '')
    complaints = Complaint.objects.select_related('user').all()
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if search_q:
        complaints = complaints.filter(title__icontains=search_q)
    complaints = complaints.annotate(p_order=priority_order()).order_by('p_order', '-created_at')
    stats = {
        'total': Complaint.objects.count(),
        'pending': Complaint.objects.filter(status='Pending').count(),
        'in_progress': Complaint.objects.filter(status='In Progress').count(),
        'resolved': Complaint.objects.filter(status='Resolved').count(),
        'high': Complaint.objects.filter(priority='High').count(),
    }
    return render(request, 'admin_dashboard.html', {
        'complaints': complaints, 'stats': stats,
        'priority_filter': priority_filter, 'status_filter': status_filter, 'search_q': search_q
    })

@admin_required
def update_complaint_status(request, pk):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'In Progress', 'Resolved']:
            complaint.status = new_status
            complaint.save()
            messages.success(request, f'Status updated to "{new_status}".')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')

@admin_required
def delete_complaint(request, pk):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, pk=pk)
        title = complaint.title
        complaint.delete()
        messages.success(request, f'Complaint "{title}" deleted.')
    return redirect('admin_dashboard')
