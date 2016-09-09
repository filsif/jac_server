from django import forms
from server.models import Genre




class StringListField(forms.CharField):
    def prepare_value(self, value):
        return ', '.join(value)

    def to_python(self, value):
        if not value:
            return []
        return [item.strip() for item in value.split(',')]


class PlayerForm(forms.Form):
    firstname       = forms.CharField( max_length = 64 )
    lastname        = forms.CharField( max_length = 64 )
    nickname        = forms.CharField( max_length = 64 )    
    photo           = forms.URLField( )
    age             = forms.IntegerField()
    address         = forms.CharField( max_length = 256 )
    email           = forms.EmailField()
    mobile_phone    = forms.CharField( max_length = 20 )
    
    
    
class BoardGameForm(forms.Form):
    
    name            = forms.CharField( max_length=128)
    year            = forms.IntegerField()
    synopsis        = forms.CharField( max_length = 4096)    
    min_age         = forms.IntegerField()
    min_player      = forms.IntegerField()
    max_player      = forms.IntegerField()
    playing_time    = forms.IntegerField()
    bgg_id          = forms.IntegerField( required = False )
    
    genre           = forms.CharField( required = False,max_length = 256 ) # json values 
    
    
    
    cover           = forms.FileField(required=False )
    snapshot        = forms.FileField(required=False )
    
    