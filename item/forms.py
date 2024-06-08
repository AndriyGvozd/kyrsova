from django import forms

from .models import Item, Complaint

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'region', 'price', 'image',)
        labels = {
            'name': ('Назва'),
            'description': ('Опис'),
            'region': ('Регіон'),
            'price': ('Ціна'),
            'image': ('Зображення'),
            'category': ('Категорія'),
        }
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'region': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Ціна не може бути від'ємною")
        return price
    def clean_image(self):
        image = self.cleaned_data['image']
        if not image:
            raise forms.ValidationError("Завантаження зображення є обов'язковим")
        return image    

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'region', 'price', 'image', 'is_sold')
        labels = {
            'name': ('Назва'),
            'description': ('Опис'),
            'region': ('Регіон'),
            'price': ('Ціна'),
            'image': ('Зображення'),
            'is_sold': ('Деактивувати'),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'region': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Ціна не може бути від'ємною")
        return price
    def clean_image(self):
        image = self.cleaned_data['image']
        if not image:
            raise forms.ValidationError("Завантаження зображення є обов'язковим")
        return image
        
class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            })
        }

        