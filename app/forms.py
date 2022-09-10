from django import forms

from .models import Category, Card


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def invalid_login_error(self):
        self.add_error(None, forms.ValidationError('User with such login and password not found.'))


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

    def __init__(self, user, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(user=user)


class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['question', 'question_image', 'answer', 'answer_image', 'category']

    def __init__(self, user, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_category(self):
        category = self.cleaned_data['category']
        if not category:
            raise forms.ValidationError('Category is required field!')
        return category
