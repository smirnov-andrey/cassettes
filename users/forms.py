from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('first_name', 'last_name', 'username', 'email')


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

