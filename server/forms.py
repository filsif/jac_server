from django import forms


class PlayerForm(forms.Form):
    firstname       = forms.CharField( max_length = 64 )
    lastname        = forms.CharField( max_length = 64 )
    nickname        = forms.CharField( max_length = 64 )    
    photo           = forms.URLField( )
    age             = forms.IntegerField()
    address         = forms.CharField( max_length = 256 )
    email           = forms.EmailField()
    mobile_phone    = forms.CharField( max_length = 20 )