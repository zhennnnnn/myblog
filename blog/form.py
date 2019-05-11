from django import forms
class ContactForm(forms.Form):
 subject = forms.CharField(max_length=100,label='主题')
 message = forms.CharField(widget=forms.TextInput)
 sender = forms.EmailField()
 cc_myself = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    username = forms.CharField(label="用戶名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="確認密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label = "信箱", max_length=256, widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label = "性別",choices=gender)

class UserForm(forms.Form):
    username = forms.CharField(label="用戶名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密碼", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))