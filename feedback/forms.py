from django import forms


class FeedBackFormA(forms.Form):
    """First feedback form"""
    option1 = forms.RadioSelect()
    option2 = forms.RadioSelect()


class FeedBackFormB(forms.Form):
    """Second feedback form"""
    option3 = forms.RadioSelect()
    option4 = forms.RadioSelect()
    option5 = forms.RadioSelect()
    comment = forms.TextInput()
