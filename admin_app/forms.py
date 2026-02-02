from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
from .models import AdminProfile
from .models import RoleFunction, Function, UserProfile

import re  # for phone number regex

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required' }))

class AdminRegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'})
    )
    phoneno = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'})
    )
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    # ----------------------------------------------------------------------
    # ✓ Username must be unique
    # ----------------------------------------------------------------------
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # ----------------------------------------------------------------------
    # ✓ Email must be unique
    # ----------------------------------------------------------------------
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    # ----------------------------------------------------------------------
    # ✓ Phone number validation
    # ----------------------------------------------------------------------
    def clean_phoneno(self):
        phone = self.cleaned_data.get("phoneno")
        pattern = r'^\+?\d{10,15}$'
        if not re.match(pattern, phone):
            raise ValidationError("Enter a valid phone number (10–15 digits, optional '+').")
        return phone

    # ----------------------------------------------------------------------
    # ✓ Password validation rules (same as user registration)
    # ----------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 1. Password match
        if password != confirm_password:
            raise ValidationError("Passwords do not match!")

        if password:
            # Rule 1: Length 8–20
            if len(password) < 8 or len(password) > 20:
                raise ValidationError("Password must be between 8 and 20 characters long.")

            # Rule 2: At least one uppercase
            if not re.search(r'[A-Z]', password):
                raise ValidationError("Password must contain at least one uppercase letter (A–Z).")

            # Rule 3: At least one lowercase
            if not re.search(r'[a-z]', password):
                raise ValidationError("Password must contain at least one lowercase letter (a–z).")

            # Rule 4: At least one number
            if not re.search(r'\d', password):
                raise ValidationError("Password must contain at least one number (0–9).")

            # Rule 5: At least one special character
            if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
                raise ValidationError("Password must contain at least one special character (e.g., @, #, $, %, &, !, *).")

            # Rule 6: No spaces
            if ' ' in password:
                raise ValidationError("Password should not contain spaces.")

            # Rule 7: Not a common password
            common_passwords = ['password', '123456', 'admin', 'qwerty', 'letmein']
            if password.lower() in common_passwords:
                raise ValidationError("Password is too common. Choose a stronger password.")

            # Rule 8: Should not contain username
            if username and username.lower() in password.lower():
                raise ValidationError("Password should not contain the username.")

            # Rule 9: Should not contain email prefix
            if email:
                email_prefix = email.split("@")[0]
                if email_prefix.lower() in password.lower():
                    raise ValidationError("Password should not contain part of your email.")

            return  cleaned_data
        
class AdminProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = AdminProfile
        fields = ['email', 'phoneno', 'profile_photo']
        widgets = {
            "profile_photo": forms.FileInput(attrs={
                "class": "hidden-file-input",
                "accept": "image/*"
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # Pre-fill User model fields
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name


class UserRegistrationForm(forms.ModelForm):
    # 🔑 Password fields (handled manually)
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    # 🔹 Extra profile fields
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    phone_number = forms.CharField(max_length=15, required=False)

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    nationality = forms.CharField(max_length=100, required=False)
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        # 🚫 DO NOT INCLUDE PASSWORD HERE
        fields = ['username', 'first_name', 'last_name', 'email']

    # ✅ Username uniqueness (allow same user during edit)
    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("This username is already taken.")

        return username

    # ✅ Email uniqueness (allow same user during edit)
    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise ValidationError("This email is already registered.")

        return email

    # ✅ Phone number validation
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone:
            pattern = r'^\+?\d{10,15}$'
            if not re.match(pattern, phone):
                raise ValidationError(
                    "Enter a valid phone number (10–15 digits, optional '+')."
                )
        return phone

    # ✅ Password validation (SAFE for both add & edit)
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        is_edit = self.instance.pk is not None

        # 🔒 Create user → password required
        if not is_edit and not password:
            raise ValidationError("Password is required for new users.")

        # 🔑 Edit user → validate ONLY if password is entered
        if password:
            if not confirm_password:
                raise ValidationError("Please confirm the password.")

            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

            if len(password) < 8 or len(password) > 20:
                raise ValidationError(
                    "Password must be between 8 and 20 characters long."
                )

            if not re.search(r'[A-Z]', password):
                raise ValidationError(
                    "Password must contain at least one uppercase letter."
                )

            if not re.search(r'[a-z]', password):
                raise ValidationError(
                    "Password must contain at least one lowercase letter."
                )

            if not re.search(r'\d', password):
                raise ValidationError(
                    "Password must contain at least one number."
                )

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise ValidationError(
                    "Password must contain at least one special character."
                )

            if ' ' in password:
                raise ValidationError("Password should not contain spaces.")

            common_passwords = [
                'password', '123456', 'admin', 'qwerty', 'letmein'
            ]
            if password.lower() in common_passwords:
                raise ValidationError("Password is too common.")

            if username and username.lower() in password.lower():
                raise ValidationError(
                    "Password should not contain the username."
                )

            if email:
                email_prefix = email.split('@')[0]
                if email_prefix.lower() in password.lower():
                    raise ValidationError(
                        "Password should not contain part of your email."
                    )

        return cleaned_data
    
    
from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'})
    )

from django import forms

class AdminAccessKeyForm(forms.Form):
    access_key = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Security Key'
        }),
        label="Security Key"
    )


from django import forms
from django import forms
from django.contrib.auth.models import User

class ForgotPasswordRequestForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Registered email'
        })
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Reason for password reset',
            'rows': 3
        }),
        required=True
    )

class AdminApproveResetForm(forms.Form):
    approve = forms.BooleanField(required=False, initial=False)

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("new_password")
        p2 = cleaned.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned


from django import forms
from .models import UserProfile
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(required=False)  # For User model
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            'role',
            'phone_number',
            'gender',
            'nationality',
            'profile_photo',
            'description'
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # store user if needed
        # Pre-fill User model fields if editing
        if user and self.instance:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

from django import forms
from .models import Role, Function

class RoleFunctionForm(forms.ModelForm):
    functions = forms.ModelMultipleChoiceField(
        queryset=Function.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = RoleFunction
        fields = ["role", "functions"]



from django import forms

from .models import Carrier



class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = [
            'name',
            'carrier_type',
            'api_base_url',
            'api_key',
            'api_secret',
            'status'
        ]


# forms.py
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class SimplePasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter new password",
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm new password",
        })
    )

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password")
        p2 = cleaned_data.get("confirm_password")

        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data