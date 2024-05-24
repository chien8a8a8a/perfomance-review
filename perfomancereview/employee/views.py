import uuid;

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from employee.forms import EmployeeForm
from employee.models import Employee


@login_required
# Create your views here.
def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                employee = Employee(
                    id=str(uuid.uuid4()),
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    contact=form.cleaned_data['contact'],
                )
                employee.save()

                user = User.objects.create_user(
                    username=employee.email,  # Or any suitable username based on employee data
                    email=employee.email,
                    password='abcd@1234',
                    is_staff=True,
                )
                user.save()

                # Optionally, link the employee instance to the user

                return redirect("/employees")
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, 'create-employee.html', {'form': form})


@login_required
def employees(request):
    employees = Employee.objects.all()
    return render(request, "employees.html", {'employees': employees})


@login_required
def edit_employee(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'edit-employee.html', {'employee': employee})


@login_required
def update_employee(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        employee.name = form.cleaned_data['name']
        employee.email = form.cleaned_data['email']
        employee.contact = form.cleaned_data['contact']
        employee.save()
        return redirect("/employees")
    return render(request, 'edit-employee.html', {'employee': employee})


@login_required
def delete_employee(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("/employees")
