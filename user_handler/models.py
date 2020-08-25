from django.db import models
import uuid 
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from .models_permission import CustomPermission
import random
from django.core.mail import send_mail
from django.template.loader import get_template 
from django.template import Context
import datetime
from io import BytesIO
from django.http import HttpResponse
import xhtml2pdf.pisa as pisa
from django.conf import settings

class CustomUserBase(AbstractUser):
    '''Base Custom UserClass'''
    is_active = models.BooleanField(default=True)
    is_destroyed = models.BooleanField(default=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    role = models.ForeignKey(CustomPermission, on_delete=models.PROTECT, related_name='role_users', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta(object):
        unique_together = ('email',)

def image_directory_path(instance, filename):
    return 'image/user_{0}/image_{1}.jpg'.format(instance.user.username, random.randint(0,100))

class Profile(models.Model):
    user = models.OneToOneField(CustomUserBase, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    phone_number2 = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to= image_directory_path, null=True, blank=True)
    post = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.user)
  
class Vendor(models.Model):
    ''' Vendor model'''
    added_by = models.ForeignKey(CustomUserBase, on_delete= models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default="Nepal")
    company = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    website = models.CharField(null=True, max_length=255)
    tax_number = models.CharField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=25)
    phone2 = models.CharField(max_length=25)
    address = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CustomerCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name}'

class Customer(models.Model):
    ''' model schema for customer '''
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.CharField(null=True, max_length=255)
    tax_number = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=25)
    phone2 = models.CharField(max_length=25)
    address = models.TextField()
    category = models.ForeignKey(CustomerCategory, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.PositiveIntegerField()
    tax_types = (
        ('fixed', "Fixed"),
        ('normal', "Normal")
    )
    tax_type = models.CharField(max_length=30, choices=tax_types, default='normal')
    code = models.CharField(max_length=255, null=True, blank=True, default=" ")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name} {self.rate}'

class Discount(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, null=True, blank=True)
    discount_types =(
        ('fixed',"Fixed"),
        ('percent', "Percent")
    )
    discount_type = models.CharField(max_length=20, default="Percent")
    rate = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name} {self.code} {self.rate}'

class UserActivities(models.Model):
    LOGIN_STATUS = (('LOGIN', 'Login'),
                           ('LOGOUT', 'Logout'))
    user = models.ForeignKey(CustomUserBase, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    log_time = models.DateTimeField()
    action = models.CharField(max_length=6, choices=LOGIN_STATUS, null=True, blank=True)

class PasswordResetCode(models.Model):
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField()
    ip = models.GenericIPAddressField(null=True, blank=True)
    email = models.EmailField()

    class Meta():
        unique_together=('code','email')


class Setting(models.Model):
    units = (
        ('kg', "kg"),
        ('g', "g"),
        ('lb', "lb")
    )    
    default_weight_unit = models.CharField(max_length=25, choices=units, default='g')
    company = models.CharField(max_length=255)
    company_address = models.TextField()
    branch = models.CharField(max_length=25)
    branch_code = models.CharField(max_length=5)
    pan_number = models.CharField(max_length=255)

    manufacturer = models.CharField(max_length=255, default="Mandala IT Solutions")
    distributor = models.CharField(max_length=255, default="Mandala IT Solutions")
    contact = models.CharField(max_length=255, default= '+(977)9846785856')
    manufacturer_address = models.CharField(max_length=255, default='Pokhara, Lakeside')
    manufacturer_website = models.URLField(default='https://mandalaitsolutions.com/')

    change_fisal_year = models.DateTimeField()          # only using day and month 
    
    stock_low_notification_on = models.PositiveIntegerField(default = 10)

    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationSetting(models.Model):
    model_choice = (
        ('item', "Item"),
        ('purchase_order', "Purchase Order"),
        ('invoice', "Invoice")
    )
    model = models.CharField(max_length=25, choices=model_choice)
    roles_to_get_notified = models.ManyToManyField(CustomPermission, blank=True)

    class Meta:
        unique_together = ('model',)
    
    def __str__(self):
        return f'{self.model}'

class Notification(models.Model):
    msg = models.TextField()
    object_id = models.CharField(max_length=25)
    model = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ActivityLog(models.Model):
    action_choice = (
        ('delete', "Delete"),
        ('create', "Create"),
        ('update', "Update"),
        ('soft_delete', "Soft Delete")
    )
    model = models.CharField(max_length=25)
    action = models.CharField(max_length=25, choices=action_choice)
    object_id = models.PositiveIntegerField()
    object_str = models.CharField(max_length=255)
    change = models.TextField()
    user = models.ForeignKey(CustomUserBase, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)   

    def delete(self):
        raise Exception("Activity logs cannot be removed.")

def log(model, action, id, stri, change, user):
    ActivityLog.objects.create(
        model = model,
        action = action,
        object_id = id,
        object_str = stri,
        change =  str(change),
        user = user
    )

def notify(msg, object_id, model):
    try:
        notify = Notification.objects.get(
            object_id = object_id, model = str(model).lower()
        )
        notify.delete()
    except:
        pass
    Notification.objects.create(
        msg = msg,
        object_id = object_id,
        model = str(model).lower()
    )
    data = {
        'msg' : msg,
        'id' : object_id,
        'model' : model
    }
    try:
        roles = NotificationSetting.objects.get(model = str(model).lower()).roles_to_get_notified.all()
        for role in roles:
            users = CustomUserBase.objects.filter(role = role)
            for user in users:
                response = export_data(data)
                res = send_mail("Email Notification", "Some Generic Msg", settings.EMAIL_HOST_USER, [user.email], html_message=response['html'])
                if res:
                    print("Notification sent through email.")
                else:
                    print("Notification cannot be sent through email.")
    except:
        print("Notification settings has not been setup.")

def render_to_pdf(template_src, context_dict={}):
    template = get_template('notification.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return {'pdf' : HttpResponse(result.getvalue(), content_type='application/pdf'), 'html': html}
    return None

def export_data(data):
    template = get_template('notification.html')
    data = {
        'today': datetime.date.today(),
        'data': data
    }
    html = template.render(data)
    pdf = render_to_pdf('notification', data)
    return pdf
