from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update   = forms.BooleanField(initial=False,required=False,widget=forms.HiddenInput)   
