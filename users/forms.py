from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    username = forms.CharField(label='search',
                        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='search',
                               widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='search',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='search',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Password repeat'}))
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super(CreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-cust modal__input'
class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'born_date', 'country', 'image', 'language', 'website', 'bio')
        labels = {
            'bio': 'О себе',
        }
        help_texts = {
            'born_date': 'Формат записи (2023-12-31)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].widget.attrs.update({'class': 'input-cust input-cust_fz14'})
        self.fields['language'].widget.attrs.update({'class': 'input-cust input-cust_fz14'})

