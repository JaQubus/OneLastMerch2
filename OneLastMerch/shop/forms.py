from django import forms

class FilterForm(forms.Form):
    
    # value for backend <-> label
    CATEGORY_CHOICES = [
        ('shirt', 'Shirts'),
        ('accessory', 'Accessories'),
        ('cap', 'Caps'),
        ('hoodie', 'Hoodies'),
    ]
    
    tags = forms.MultipleChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Categories"
    )
    