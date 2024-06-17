from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User,Vehicle,Review,Profile,Booking


USER_TYPE_CHOICES = [
    (0, 'Customer'),
    (1, 'Owner'),
    (2, 'Admin'),
]

class SignUpForm(UserCreationForm):
    email=forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Email Address'}))
    first_name=forms.CharField(label='First Name',max_length='100',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your First name'}))
    last_name=forms.CharField(label='Last Name',max_length='100',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Last name'}))
    user_type = forms.TypedChoiceField(
        label="Register As",
        choices=USER_TYPE_CHOICES,
        coerce=int,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model=User
        fields=('first_name','last_name','username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Your Username'
        self.fields['username'].label = 'Username'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Your Password'
        self.fields['password1'].label = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = 'Confirm Password'

    def save(self, commit=True):
        user = super().save(commit=False)   
        user_type = self.cleaned_data['user_type']
        if user_type == 2:
            user.is_admin = True
            user.is_owner = False
            user.is_customer = False
        elif user_type == 1:
            user.is_admin = False
            user.is_owner = True
            user.is_customer = False
        else:
            user.is_admin = False
            user.is_owner = False
            user.is_customer = True
        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control custom-email-class'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','profile_picture', 'phone_number','licence_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control custom-full-name-class'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control custom-profile-picture-class'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control custom-phone-number-class'}),
            'licence_picture': forms.FileInput(attrs={'class': 'form-control custom-profile-picture-class'}),
            
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_name','vehicle_description','vehicle_number', 'vehicle_gear','vehicle_model', 'vehicle_type', 'vehicle_color', 'vehicle_front_image', 'vehicle_right_image', 'vehicle_left_image', 'vehicle_back_image', 'vehicle_location', 'vehicle_seat','price_per_day']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {

            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields = ['pickup_date', 'return_date']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control ', 'type': 'date'}),
        }

