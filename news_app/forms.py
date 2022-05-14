from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"label": "Name", "placeholder": "Name here"}),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"label": "Email", "placeholder": "Email here..."}
        ),
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={"label": "Subject", "placeholder": "Subject here..."}
        ),
        required=False,
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "label": "Message",
                "placeholder": "Message",
                "class": "contact_form",
            },
        ),
        required=False,
    )
