from django import forms


class FeedBackFormA(forms.Form):
    """First feedback form"""
    CHOICES = [
        ("I am very satisfied and will refer my friends and family to you",
         "I am very satisfied and will refer my friends and family to you"),

        ('I am not satisfied', "I am not satisfied")
    ]

    experience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={}), label="How was your experience today?")


class FeedBackFormB(forms.Form):
    """Second feedback form"""
    CHOICES = [
        ("Not happy with front desk", "Not happy with front desk"),
        ("Not happy with Consultant", "Not happy with Consultant"),
        ("This is a billing issue", "This is a billing issue")
    ]

    experience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={}),
                                   label="Why are you not happy?")

    comment = forms.CharField(widget=forms.TextInput)
