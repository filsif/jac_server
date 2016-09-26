from django.shortcuts import render
from django.http import HttpResponse , Http404 ,HttpResponseForbidden
from django.core import serializers as szs
from server.models import BoardGame , Player
from server.forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.models import User
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def boardgames_id(request, boardgame_id):
    
    datas = boardgame_id.split(',')
    
    objs = []
    
    for elem in datas:
        try:
            obj = BoardGame.objects.get(pk=int(elem))
        except BoardGame.DoesNotExist:
            pass
        else:
            objs.append( obj )
    data = szs.serialize("json",objs)
    return HttpResponse( data )

def boardgames(request ):     
    data = szs.serialize("json",BoardGame.objects.all())
    return HttpResponse( data )

def boardgames_name(request, boardgame_name):
    
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    datas = boardgame_name.split(',')
    
    objs = []
    
    for elem in datas:
        try:
            obj = BoardGame.objects.filter(name__startswith=elem)
        except BoardGame.DoesNotExist:
            pass
        else:
            objs += obj
    
    print (objs)
    data = szs.serialize("json",objs)
    
    return HttpResponse(data)

def check_nickname( request , nickname ):
    try:
        User.objects.get( username = nickname )
    except:    
        return HttpResponse('{ "result" : false }')
    else:
        return HttpResponse('{ "result" : true }')
    

def check_email( request , email ):
    try:
        User.objects.get( email = email )    
    except:
        return HttpResponse('{ "result" : false }')
    else:
        return HttpResponse('{ "result" : true }')

def user_login( request, user , password ):
    
    if request.user.is_authenticated():
        print("already authenticated")        
        logout(request )
        
    newuser = authenticate(username=user, password=password)
    if newuser is not None:
        login(request, newuser)
        # Redirect to a success page.
        return HttpResponse("ok"  )        
    else:
        return HttpResponseForbidden()

def user_logout( request ):
    if request.user.is_authenticated():            
        logout(request )
        return HttpResponse("ok")
    
    return HttpResponse("vide")
        
def add_boardgame(request):
    #if not request.user.is_authenticated():
    #    return HttpResponseForbidden()
   
    if request.method == 'POST':
        form = BoardGameForm( request.POST , request.FILES )
        if form.is_valid():            
            name            = form.cleaned_data['name']
            year            = form.cleaned_data['year']
            synopsis        = form.cleaned_data['synopsis']            
            min_age         = form.cleaned_data['min_age']
            min_player      = form.cleaned_data['min_player']
            max_player      = form.cleaned_data['max_player']
            playing_time    = form.cleaned_data['playing_time']
            bgg_id          = form.cleaned_data['bgg_id']            
            #genre           = form.cleaned_data['genre']          
            
            
            mydict = dict(request.POST.iterlists())  
            
            genres=[]
            try:      
                genres = mydict['genre'] # only way to recup a list of forms entries with the same key
            except:
                print("no genre for this game")
              
           
            '''
            test if boardgame is already present
            by name
            or by bgg_id          
            
            '''            
            obj = None
            
            try:
                obj = BoardGame.objects.get(Q(name = name) | Q( bgg_id = bgg_id ) )
            except BoardGame.DoesNotExist:
                query = BoardGame(name = name , year = year , synopsis = synopsis , min_age = min_age , min_player = min_player , max_player = max_player , playing_time = playing_time , bgg_id = bgg_id )
                query.save()               
                
                count = query.pk
                
                cover = None
                snapshot = None               
                
                cover = request.FILES.get('cover',None)            
                if cover is not None:
                    with open('cover_' + str(count) + '.jpg', 'wb+') as destination:
                        for chunk in cover.chunks():
                            destination.write(chunk)
                            
                snapshot = request.FILES.get('thumbnail',None)
                if snapshot is not None:
                    with open('snapshot_' + str(count) + '.jpg', 'wb+') as destination:
                        for chunk in snapshot.chunks():
                            destination.write(chunk)
                            
                ''' now write the new genres '''
                
                for genre in genres:  
                    print("genre :" + genre)
                    mygenre, created = Genre.objects.get_or_create( name=genre)
                    query.genres.add( mygenre)    

            return HttpResponse(  "ok" )
        else:
            print("erreur " + str(form.errors))
            return HttpResponseForbidden()
    else:
        raise Http404("Not a POST request")

def add_player(request):
    if request.method == 'POST':        
        form = PlayerForm(request.POST)
        
        if form.is_valid():
            firstname       = form.cleaned_data['firstname']
            lastname        = form.cleaned_data['lastname']
            username        = form.cleaned_data['username']
            photo           = form.cleaned_data['photo']            
            address         = form.cleaned_data['address']
            email           = form.cleaned_data['email']
            password        = form.cleaned_data['password']
            mobilephone     = form.cleaned_data['mobilephone']
            bggnickname     = form.cleaned_data['bggnickname']
            
            #query = User(first_name = firstname , last_name = lastname , username = username , photo = photo , bgg_nickname = bggnickname , address = address , email = email , mobile_phone = mobilephone , password = password)
            user = User(first_name = firstname , last_name = lastname , username = username , email = email )                     
            user.set_password( password )            
            user.save()  
            
            u = User.objects.get( pk = user.pk )            
            
            player = u.player
            player.bgg_nickname = bggnickname
            player.address = address
            player.mobile_phone = mobilephone
            player.save()     
            
          
            #data = szs.serialize("json" , Player.objects.filter( pk = user.pk ) )
            
            
            
            return HttpResponse("")
        else:
            raise Http404("Form is not valid : " + str(form.errors) )
    else:
        raise Http404("Not a POST request")
            
            
def players(request):   
    data = szs.serialize("json",Player.objects.all())
    return HttpResponse( data )

def player_infos( request ):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    u = User.objects.get( pk = request.user.pk )
    objs = []
    #obj = dict( u.items() , u.player.items())
    print (u)
    print (u.player)
    objs.append(u)
    objs.append(u.player)
    data = szs.serialize("json" ,u.player )
    return HttpResponse( data )
    