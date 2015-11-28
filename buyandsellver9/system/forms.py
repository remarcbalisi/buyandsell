from django import forms
from .models import User, Item, Type, Image, Category

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'contact_number']

class ItemForm(forms.ModelForm):

	class Meta:
		model = Item
		fields = ['name', 'description', 'price', 'category_id', 'type_id', 'user_id']

class ImageForm(forms.ModelForm):

	class Meta:
		model = Image
		fields = ['title', 'stuff_image', 'item_id']