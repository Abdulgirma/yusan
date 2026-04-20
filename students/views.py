from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import hashlib
from .models import Student


def generate_reg_number():
    last_student = Student.objects.all().order_by('-id').first()
    if last_student:
        try:
            last_num = int(last_student.reg_number.split('/')[-1])
            new_num = last_num + 1
        except (ValueError, IndexError):
            new_num = 1
    else:
        new_num = 1
    return f"DG/ICT/25/{new_num:04d}"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ── HOME ────────────────────────────────────────────────
def home(request):
    return render(request, 'students/home.html')


# ── REGISTER ────────────────────────────────────────────
def register(request):
    departments = Student.DEPARTMENTS
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        department = request.POST.get('department', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not all([full_name, phone_number, department, password, confirm_password]):
            return render(request, 'students/register.html', {
                'error': 'Please fill in all fields.',
                'departments': departments,
            })

        if password != confirm_password:
            return render(request, 'students/register.html', {
                'error': 'Passwords do not match.',
                'departments': departments,
                'full_name': full_name,
                'phone_number': phone_number,
                'department': department,
            })

        if Student.objects.filter(phone_number=phone_number).exists():
            return render(request, 'students/register.html', {
                'phone_exists': True,
                'departments': departments,
            })

        reg_number = generate_reg_number()
        hashed_pw = hash_password(password)

        student = Student.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            department=department,
            password=hashed_pw,
            reg_number=reg_number,
        )

        dept_dict = dict(Student.DEPARTMENTS)
        dept_full = dept_dict.get(department, department)

        return render(request, 'students/register.html', {
            'success': True,
            'student_name': full_name,
            'student_phone': phone_number,
            'student_dept': dept_full,
            'student_reg': reg_number,
            'departments': departments,
        })

    return render(request, 'students/register.html', {'departments': departments})


# ── LOGIN ────────────────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        reg_number = request.POST.get('reg_number', '').strip()
        password = request.POST.get('password', '').strip()

        if not reg_number or not password:
            return render(request, 'students/login.html', {'error': 'Please fill in all fields.'})

        hashed_pw = hash_password(password)
        try:
            student = Student.objects.get(reg_number=reg_number, password=hashed_pw)
            request.session['student_id'] = student.id
            return redirect('dashboard')
        except Student.DoesNotExist:
            return render(request, 'students/login.html', {'error': 'Invalid registration number or password.'})

    return render(request, 'students/login.html')


# ── DASHBOARD ────────────────────────────────────────────
def dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    try:
        student = Student.objects.get(id=student_id)
        dept_dict = dict(Student.DEPARTMENTS)
        dept_full = dept_dict.get(student.department, student.department)
        return render(request, 'students/dashboard.html', {
            'student': student,
            'dept_full': dept_full,
        })
    except Student.DoesNotExist:
        return redirect('login')


# ── LOGOUT ───────────────────────────────────────────────
def logout_view(request):
    request.session.flush()
    return redirect('home')


# ── ADMIN LOGIN ──────────────────────────────────────────
def admin_login(request):
    if request.session.get('is_admin'):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            return render(request, 'students/admin_login.html', {
                'error': 'Invalid credentials or not an admin account.'
            })

    return render(request, 'students/admin_login.html')


# ── ADMIN DASHBOARD ──────────────────────────────────────
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    students = Student.objects.all().order_by('-id')
    today = timezone.now().date()
    today_count = Student.objects.filter(created_at__date=today).count()
    ict_count = Student.objects.filter(department='ICT').count()
    dept_count = Student.objects.values('department').distinct().count()

    return render(request, 'students/admin_dashboard.html', {
        'students': students,
        'total_students': students.count(),
        'today_count': today_count,
        'ict_count': ict_count,
        'dept_count': dept_count,
        'departments': Student.DEPARTMENTS,
    })


# ── ADMIN DELETE STUDENT ──────────────────────────────────
def admin_delete_student(request, student_id):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('admin_dashboard')


# ── ADMIN LOGOUT ─────────────────────────────────────────
def admin_logout(request):
    request.session.pop('is_admin', None)
    logout(request)
    return redirect('admin_login')
