from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class EmployeeManager(BaseUserManager):
   '''
        Custom manager for Employee
   '''
   def create_user(self, email, password=None, **extra_fields):
       if not email:
           raise ValueError("The Email field must be set")
       email = self.normalize_email(email)
       user = self.model(email=email, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user
   
   def create_superuser(self, email, password=None, **extra_fields):
       extra_fields.setdefault('is_superuser', True)
       if not extra_fields.get('is_superuser'):
           raise ValueError("Superuser must have is_superuser=True.")
       return self.create_user(email, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    '''
        Class for storing employee details
    '''
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    department = models.ForeignKey('Department',on_delete=models.PROTECT)
    reporting_manager = models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True)
    role = models.ForeignKey('Role',on_delete=models.PROTECT)
    
    objects = EmployeeManager()
    
    USERNAME_FIELD = 'email'
    
    class Meta:
        db_table = 'employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Department(models.Model):
    '''
        Class for storing department details
    '''
    name = models.CharField(max_length=50,unique=True)
    manager = models.OneToOneField('Employee',on_delete=models.SET_NULL,blank=True,null=True,related_name='manager')
    hr = models.OneToOneField('Employee',on_delete=models.SET_NULL,blank=True,null=True,related_name='hr')
    
    class Meta:
        db_table = 'department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return self.name
    
class Role(models.Model):
    '''
        Class to store various roles
    '''
    name = models.CharField(max_length=20,unique=True)
    
    class Meta:
        db_table = 'role'
        verbose_name_plural = 'Roles'