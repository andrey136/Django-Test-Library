from django import forms

from .models import Product

class ProductForm( forms.ModelForm):
    title = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Your description",
                "class": "new-class name",
                "id": "my-id-for-text-area",
                "rows": 20,
                "cols": 120
            }
        )
    )
    price = forms.DecimalField(initial=199.99)
    email = forms.EmailField()
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if "CFE" not in title:
            raise forms.ValidationError("This is not a valid title")
        if "news" not in title:
            raise forms.ValidationError("This is not a valid title")
        return title

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        if "edu" not in email:
            raise forms.ValidationError("This is not a valid email")
        return email

class RawProductForm(forms.Form):
    title       = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    description = forms.CharField(
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "placeholder": "Your description",
                                    "class":"new-class name",
                                    "id": "my-id-for-text-area",
                                    "rows": 20,
                                    "cols": 120
                                }
                            )
                        )
    price       = forms.DecimalField(initial=199.99)
