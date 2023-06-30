from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth import(
    authenticate,
    get_user_model
)
User=get_user_model()

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password =forms.CharField(widget=forms.PasswordInput)

    def clean (self,*args,**kwargs):
        username =self.cleaned_data.get('username')
        password =self.cleaned_data.get('password')
        if username and password:
            user =authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user dose not exist")
            if not user.check_password(password):
                raise forms.ValidationError("incorrect password")
            if not user.is_active:
                raise forms.ValidationError("The user is not actine")
        return super(UserLoginForm, self).clean(*args,**kwargs)
    
class UserRegisterForm(forms.ModelForm):
    email=forms.EmailField(label="Email address")
    email1=forms.EmailField(label="Confirm email")
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model =User
        fields=[
            'username',
            'email',
            'email1',
            'password'
        ]
    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        email1=self.cleaned_data.get('email1')
        if email!=email1:
            raise forms.ValidationError("Emails must match")
        emails_qs=User.objects.filter(email=email)
        if emails_qs.exists():
            raise forms.ValidationError("alredy registerd")
        return super(UserRegisterForm,self).clean(*args,**kwargs)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'address', 'phone_number']


class OrderForm(forms.Form):
   
    shipping_address = forms.CharField(max_length=100)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])

from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    )

    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Order
        fields = ['user', 'shipping_address', 'payment_method']

    def save(self, commit=True):
        order = super().save(commit=False)
        # Perform additional operations or modifications on the order instance if needed
        if commit:
            order.save()
        return order
    

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            profile.user = self.user
        if commit:
            profile.save()
        return profile