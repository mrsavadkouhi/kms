from django import forms
from .models import *
import re


# ========  Profile ========
class ProfileCreateForm(forms.ModelForm):
	username = forms.CharField(label='نام کاربری', required=True, error_messages={'required': 'وارد کردن نام کاربری الزامی است.'})
	first_name = forms.CharField(label='نام', required=True,error_messages={'required': 'وارد کردن نام الزامی است.'})
	last_name = forms.CharField(label='نام خانوادگی', required=True,error_messages={'required': 'وارد کردن نام خانوادگی الزامی است.'})
	password = forms.CharField(label='رمز عبور', required=True, error_messages={'required': 'وارد کردن رمز عبور الزامی است.'})
	mobile_number = forms.CharField(label='رمز عبور', required=True, error_messages={'required': 'وارد کردن شماره همراه الزامی است.'})
	email = forms.EmailField(label='ایمیل', required=True, error_messages={'required': 'وارد کردن ایمیل الزامی است.'})
	avatar = forms.ImageField(label='Avatar', required=False)
	permissions=forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)

	field_order = ['username','first_name', 'last_name','password', 'email', 'mobile_number','avatar','permissions']

	class Meta:
		model = Profile
		exclude = ['user', ]

	def clean(self):
		cleaned_data = super().clean()

		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		mobile_number = cleaned_data.get('mobile_number')

		if username:
			if re.search("[ا-ی]", username):
				raise forms.ValidationError("برای نام کاربری از کاراکترهای انگلیسی استفاده نمایید.")
			if User.objects.filter(username=username).exists():
				raise forms.ValidationError("نام کاربری از قبل وجود داشته است.")
			elif re.search("\s", username):
				raise forms.ValidationError("نام کاربری نباید شامل فاصله باشد.")

		if password:
			if re.search("[ا-ی]", password):
				raise forms.ValidationError("برای کلمه عبور از کاراکترهای انگلیسی استفاده نمایید.")
			elif len(password) < 8:
				raise forms.ValidationError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
			elif not re.search("[a-z]", password):
				raise forms.ValidationError("رمز عبور باید شامل حروف کوچک باشد.")
			elif not re.search("[A-Z]", password):
				raise forms.ValidationError("رمز عبور باید شامل حروف بزرگ باشد.")
			elif not re.search("[0-9]", password):
				raise forms.ValidationError("رمز عبور باید شامل عدد باشد.")
			elif re.search("\s", password):
				raise forms.ValidationError("رمز عبور نباید شامل فاصله باشد.")

		if mobile_number:
			if not re.search("^09\d{9}$", mobile_number):
				raise forms.ValidationError("لطفا شماره همراه را طبق فرمت *********09 وارد نمایید.")

		return cleaned_data

	def save(self, commit=True):
		instance = super().save(commit=False)
		user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
										password=self.cleaned_data['password'],
										first_name=self.cleaned_data['first_name'],
										last_name=self.cleaned_data['last_name'], )

		instance.user = user
		self.instance = instance
		if commit:
			# If committing, save the instance and the m2m data immediately.
			self.instance.save()
			self._save_m2m()

		return self.instance


class ProfileUpdateForm(forms.ModelForm):
	first_name = forms.CharField(label='نام', required=False)
	last_name = forms.CharField(label='نام خانوادگی', required=False)
	email = forms.EmailField(label='ایمیل', required=True)
	avatar = forms.ImageField(label='Avatar', required=False)
	permissions=forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)

	field_order = ['username','first_name', 'last_name', 'email', 'avatar', 'permissions']

	class Meta:
		model = Profile
		exclude = ['user', ]

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		instance = kwargs.get('instance', None)
		if instance is not None:
			initial['first_name'] = instance.user.first_name
			initial['last_name'] = instance.user.last_name
			initial['email'] = instance.user.email

		kwargs['initial'] = initial
		super().__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super().clean()

		mobile_number = cleaned_data.get('mobile_number')

		if mobile_number:
			if not re.search("^09\d{9}$", mobile_number):
				raise forms.ValidationError("لطفا شماره همراه را طبق فرمت *********09 وارد نمایید.")

		return cleaned_data

	def save(self, commit=True):
		instance = super().save(commit=False)

		instance.user.first_name = self.cleaned_data['first_name']
		instance.user.last_name = self.cleaned_data['last_name']
		instance.user.email = self.cleaned_data['email']

		self.instance = instance
		if commit:
			# If committing, save the instance and the m2m data immediately.
			instance.user.save()
			self.instance.save()
			self._save_m2m()

		return self.instance
