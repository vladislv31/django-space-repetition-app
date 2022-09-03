from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def invalid_login_error(self):
        self.add_error(None, forms.ValidationError("User with such login and password not found."))
