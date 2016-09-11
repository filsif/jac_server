# -*- coding: cp1252 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Genre(models.Model):
    name            = models.CharField( unique = True, max_length = 64)
    
class BoardGame(models.Model):
    name            = models.CharField( unique = True, max_length=128)
    year            = models.IntegerField()
    synopsis        = models.TextField()
    thumbnail       = models.URLField()
    cover           = models.URLField()
    min_age         = models.IntegerField()
    min_player      = models.IntegerField()
    max_player      = models.IntegerField()
    playing_time    = models.IntegerField()
    bgg_id          = models.IntegerField( unique = True , null = True , default = 0)
    genres          = models.ManyToManyField( Genre )
    users           = models.ManyToManyField( User , through='UserGame')
    

class EventType(models.Model):
    name            = models.CharField( max_length = 64 )
    repetable       = models.BooleanField()
    
class Location(models.Model):
    name            = models.CharField( max_length = 64 )
    address         = models.CharField( max_length = 256 )
    dispo           = models.BooleanField()
    capacity        = models.IntegerField()


    
'''
Liste des inscrits : extension de user qui sert à l authentification
''' 

class Player(models.Model):
    user            = models.OneToOneField( User , on_delete= models.CASCADE )
    nickname        = models.CharField( unique= True, max_length = 64 )    
    photo           = models.URLField( )
    birthdate       = models.DateField()
    address         = models.CharField( max_length = 256 )    
    mobile_phone    = models.CharField( max_length = 20 )
    bgg_nickname    = models.CharField( unique = True, max_length = 64 ,default ='' )
    bgg_sync        = models.BooleanField( default=False)
    
    


'''
Liste des jeux des joueurs
'''
class UserGame(models.Model):
    user            = models.ForeignKey ( User , on_delete = models.CASCADE )
    boardgame       = models.ForeignKey ( BoardGame , on_delete = models.CASCADE )
    owned           = models.BooleanField()
    explanation     = models.BooleanField()
    qr_code         = models.CharField( max_length = 1024 )
    nfc_tag         = models.CharField( max_length = 1024 )

    
class Event(models.Model):
    begin_date      = models.DateField()
    end_date        = models.DateField()
    name            = models.CharField( max_length = 64 )
    event_type      = models.ForeignKey( EventType , on_delete= models.CASCADE )
    event_location  = models.ForeignKey( Location , on_delete= models.CASCADE )
    users           = models.ManyToManyField( User , through='UserEvent')
    games           = models.ManyToManyField( UserGame )
    matchs          = models.ManyToManyField( BoardGame, through='Match' )

'''
Liste des inscrits à un événement
'''
class UserEvent(models.Model):
    user            = models.ForeignKey ( User , on_delete = models.CASCADE )
    event           = models.ForeignKey ( Event,  on_delete = models.CASCADE )
    car_available   = models.BooleanField()
    with_keys       = models.BooleanField()

'''
description d'une saison avec les participants. Correspond aux inscrits d'une 
année de l'association
'''
class Season(models.Model):
    name            = models.CharField( max_length= 64)
    year            = models.IntegerField()
    users         = models.ManyToManyField( User , through='SeasonUser')
    '''   
    president       = models.ForeignKey ( Player , on_delete = models.CASCADE )
    secretaire      = models.ForeignKey ( Player , on_delete = models.CASCADE )
    tresorier       = models.ForeignKey ( Player , on_delete = models.CASCADE )
    ''' 
class SeasonUser(models.Model):
    user            = models.ForeignKey ( User , on_delete = models.CASCADE )
    season          = models.ForeignKey ( Season , on_delete = models.CASCADE )
    subscription_paid = models.BooleanField()


'''
description d'une partie lors d'un événement
'''
class Match(models.Model):
    event           = models.ForeignKey ( Event,  on_delete = models.CASCADE )
    boardgame       = models.ForeignKey ( BoardGame , on_delete = models.CASCADE )
    users         = models.ManyToManyField( User , through = 'MatchUser')
      

class MatchUser(models.Model):
    user            = models.ForeignKey ( User , on_delete = models.CASCADE )
    match           = models.ForeignKey ( Match , on_delete = models.CASCADE )
    score           = models.IntegerField()

