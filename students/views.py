import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student


# ─────────────────────────────────────────────
def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def gen_reg():
    last = Student.objects.order_by('-id').first()
    if last:
        try:
            n = int(last.reg_number.split('/')[-1]) + 1
        except Exception:
            n = 1
    else:
        n = 1
    return f"DG/ICT/25/{n:04d}"


# ── HOME ──────────────────────────────────────
def home(request):
    return render(request, 'students/home.html')


# ── REGISTER ──────────────────────────────────
def register(request):
    departments = Student.DEPARTMENTS
    if request.method == 'POST':
        full_name        = request.POST.get('full_name', '').strip()
        phone_number     = request.POST.get('phone_number', '').strip()
        department       = request.POST.get('department', '').strip()
        password         = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        ctx = {'departments': departments, 'full_name': full_name,
               'phone_number': phone_number, 'department': department}

        if not all([full_name, phone_number, department, password, confirm_password]):
            ctx['error'] = 'Please fill in all fields.'
            return render(request, 'students/register.html', ctx)

        if password != confirm_password:
            ctx['error'] = 'Passwords do not match.'
            return render(request, 'students/register.html', ctx)

        if Student.objects.filter(phone_number=phone_number).exists():
            ctx['phone_exists'] = True
            return render(request, 'students/register.html', ctx)

        reg_number = gen_reg()
        Student.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            department=department,
            password=hash_pw(password),
            reg_number=reg_number,
        )
        dept_full = dict(Student.DEPARTMENTS).get(department, department)
        return render(request, 'students/register.html', {
            'departments': departments,
            'success': True,
            'student_name': full_name,
            'student_phone': phone_number,
            'student_dept': dept_full,
            'student_reg': reg_number,
        })

    return render(request, 'students/register.html', {'departments': departments})


# ── LOGIN ─────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        reg_number = request.POST.get('reg_number', '').strip()
        password   = request.POST.get('password', '').strip()

        if not reg_number or not password:
            return render(request, 'students/login.html',
                          {'error': 'Please fill in all fields.'})

        try:
            student = Student.objects.get(
                reg_number=reg_number, password=hash_pw(password))
            request.session['student_id'] = student.id
            return redirect('dashboard')
        except Student.DoesNotExist:
            return render(request, 'students/login.html',
                          {'error': 'Invalid registration number or password.'})

    return render(request, 'students/login.html')


# ── STUDENT DASHBOARD ─────────────────────────
def dashboard(request):
    sid = request.session.get('student_id')
    if not sid:
        return redirect('login')
    try:
        student   = Student.objects.get(id=sid)
        dept_full = dict(Student.DEPARTMENTS).get(student.department, student.department)
        return render(request, 'students/dashboard.html',
                      {'student': student, 'dept_full': dept_full})
    except Student.DoesNotExist:
        return redirect('login')


# ── STUDENT LOGOUT ────────────────────────────
def logout_view(request):
    request.session.flush()
    return redirect('home')


# ── ADMIN LOGIN ───────────────────────────────
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
        return render(request, 'students/admin_login.html',
                      {'error': 'Invalid username or password.'})

    return render(request, 'students/admin_login.html')


# ── ADMIN DASHBOARD ───────────────────────────
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    students = Student.objects.all().order_by('-id')
    today    = timezone.now().date()

    return render(request, 'students/admin_dashboard.html', {
        'students':       students,
        'total_students': students.count(),
        'today_count':    Student.objects.filter(created_at__date=today).count(),
        'ict_count':      Student.objects.filter(department='ICT').count(),
        'dept_count':     Student.objects.values('department').distinct().count(),
        'departments':    Student.DEPARTMENTS,
    })


# ── ADMIN DELETE STUDENT ──────────────────────
def admin_delete_student(request, student_id):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    get_object_or_404(Student, id=student_id).delete()
    return redirect('admin_dashboard')


# ── ADMIN LOGOUT ──────────────────────────────
def admin_logout(request):
    request.session.pop('is_admin', None)
    logout(request)
    return redirect('admin_login')
