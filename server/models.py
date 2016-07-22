# -*- coding: cp1252 -*-
from __future__ import unicode_literals

from django.db import models
from PIL.ImageTk import PhotoImage
from email import email
from MySQLdb.constants.FIELD_TYPE import YEAR
from MySQLdb.constants.ER import PRIMARY_CANT_HAVE_NULL

# Create your models here.

class Genre(models.Model):
    name            = models.CharField( max_length = 64)
    
class BoardGame(models.Model):
    name            = models.CharField( max_length=128)
    year            = models.IntegerField()
    synopsis        = models.TextField()
    thumbnail       = models.URLField()
    cover           = models.URLField()
    min_age         = models.IntegerField()
    min_player      = models.IntegerField()
    max_player      = models.IntegerField()
    playing_time    = models.IntegerField()
    bgg_id          = models.IntegerField()
    
class GenreBoardGame(models.Model):
    genre           = models.ForeignKey( Genre , on_delete = models.CASCADE )
    boardgame       = models.ForeignKey( BoardGame , on_delete = models.CASCADE )
    primary         = models.BooleanField()
    
class EventType(models.Model):
    name            = models.CharField( max_length = 64 )
    repetable       = models.BooleanField()
    
class Location(models.Model):
    name            = models.CharField( max_length = 64 )
    address         = models.CharField( max_length = 256 )
    dispo           = models.BooleanField()
    capacity        = models.IntegerField()
    
class Event(models.Model):
    begin_date      = models.DateField()
    end_date        = models.DateField()
    name            = models.CharField( max_length = 64 )
    event_type      = models.ForeignKey( EventType , on_delete= models.CASCADE )
    event_location  = models.ForeignKey( Location , on_delete= models.CASCADE )
'''
Liste des inscrits
''' 
class Player(models.Model):
    firstname       = models.CharField( max_length = 64 )
    lastname        = models.CharField( max_length = 64 )
    nickname        = models.CharField( max_length = 64 )
    photo           = models.URLField( )
    age             = models.IntegerField()
    address         = models.CharField( max_length = 256 )
    email           = models.EmailField()
    mobile_phone    = models.CharField( max_length = 20 )
'''
Liste des inscrits à un événement
'''
class PlayerEvent(models.Model):
    player          = models.ForeignKey ( Player , on_delete = models.CASCADE )
    event           = models.ForeignKey ( Event,  on_delete = models.CASCADE )
    car_available   = models.BooleanField()
    with_keys       = models.BooleanField()
'''
Liste des jeux des joueurs
'''
class PlayerGame(models.Model):
    player          = models.ForeignKey ( Player , on_delete = models.CASCADE )
    boardgame       = models.ForeignKey ( BoardGame , on_delete = models.CASCADE )
    owned           = models.BooleanField()
    explanation     = models.BooleanField()
    qr_code         = models.CharField( max_length = 1024 )
    nfc_tag         = models.CharField( max_length = 1024 )

'''
Liste des jeux apportés par les joueurs à un événement
'''
class PlayerGameEvent(models.Model):
    playergame      = models.ForeignKey ( PlayerGame , on_delete = models.CASCADE )
    event           = models.ForeignKey ( Event,  on_delete = models.CASCADE )
'''

description d'une saison avec les participants. Correspond aux inscrits d'une 
année de l'association
'''
class Season(models.Model):
    name            = models.CharField( max_length= 64)
    year            = models.IntegerField()
    '''   
    president       = models.ForeignKey ( Player , on_delete = models.CASCADE )
    secretaire      = models.ForeignKey ( Player , on_delete = models.CASCADE )
    tresorier       = models.ForeignKey ( Player , on_delete = models.CASCADE )
    ''' 
class SeasonPlayer(models.Model):
    iplayer         = models.ForeignKey ( Player , on_delete = models.CASCADE )
    season          = models.ForeignKey ( Season , on_delete = models.CASCADE )
    subscription_paid = models.BooleanField()


'''
description d'une partie lors d'un événement
'''
class Match(models.Model):
    event           = models.ForeignKey ( Event,  on_delete = models.CASCADE )
    boardgame       = models.ForeignKey ( BoardGame , on_delete = models.CASCADE )
      

class MatchPlayer(models.Model):
    player          = models.ForeignKey ( Player , on_delete = models.CASCADE )
    match           = models.ForeignKey ( Match , on_delete = models.CASCADE )
    score           = models.IntegerField()

    