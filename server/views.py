# coding: utf8
from django.shortcuts import render
from django.http import HttpResponse , Http404 ,HttpResponseForbidden
from django.core import serializers as szs
from server.models import BoardGame , Player , UserGame , BoardGameVersion
from server.forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login , logout 
from django.contrib.auth.models import User
import json
import sys




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
        
        u = User.objects.get( pk = request.user.pk )
        objs = []
        
        objs.append(u)
        objs.append(u.player)
        data = szs.serialize("json" ,objs , fields=('first_name' , 'last_name' , 'address' , 'bgg_nickname') )
        return HttpResponse( data )        
    else:
        return HttpResponseForbidden()

def user_logout( request ):
    if request.user.is_authenticated():            
        logout(request )
        return HttpResponse("ok")
    
    return HttpResponse("vide")
        
def add_boardgame(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
   
    if request.method == 'POST':       
       
        form = BoardGameForm( request.POST , request.FILES )
        if form.is_valid():            
            metadata          = form.cleaned_data['metadata']
            bg_info = json.loads( metadata )
            
            
           
            '''
            test if boardgame is already present
            by name
            or by bgg_id          
            
            '''            
            cur_bg = None
            
            cur_key = None
            
            try:
                cur_bg = BoardGame.objects.get(Q(name = bg_info['title']) | Q( bgg_id = bg_info['bgg_id'] ) )
            except BoardGame.DoesNotExist:
                cur_bg = BoardGame(name = bg_info['title'] , year = bg_info['year'] , synopsis = bg_info['synopsis'] , min_age = bg_info['min_age'] , min_player = bg_info['min_player'] , max_player = bg_info['max_player'] , playing_time = bg_info['duration'] , bgg_id = bg_info['bgg_id'] )
                cur_bg.save()               
                
                cur_key = cur_bg.pk
                
                cover = None
                snapshot = None               
                
                cover = request.FILES.get('cover',None)            
                if cover is not None:
                    with open('cover_' + str(cur_key) + '.jpg', 'wb+') as destination:
                        for chunk in cover.chunks():
                            destination.write(chunk)
                    cur_bg.cover = 'http://127.0.0.1/cover_' + str(cur_key) + '.jpg'
                    cur_bg.save()
                            
                snapshot = request.FILES.get('thumbnail',None)
                if snapshot is not None:
                    with open('snapshot_' + str(cur_key) + '.jpg', 'wb+') as destination:
                        for chunk in snapshot.chunks():
                            destination.write(chunk)
                    cur_bg.thumbnail = 'http://127.0.0.1/snapshot_' + str(cur_key) + '.jpg'
                    cur_bg.save()
                            
                ''' now write the new genres '''
                
                for genre in bg_info['genres']:  
                    #print("genre :" + genre)
                    mygenre, created = Genre.objects.get_or_create( name=genre)
                    cur_bg.genres.add( mygenre)    
            else:
                cur_key = cur_bg.pk
            
            ''' versions       
                
            
            '''
                
            if len(bg_info['versions'])>0:               
                for vers in bg_info['versions']:            
                    myversion , v_created = BoardGameVersion.objects.get_or_create( bgg_version_id = vers['version_id'] , boardgame = cur_bg)
                    myversion.name = vers['title']
                    myversion.year = vers['year']
                    myversion.bgg_version_id = vers['version_id']
                    myversion.language = vers['language']
                    myversion.boardgame = cur_bg              
                   
                    cover_v = None
                    snapshot_v = None               
                    
                    cover_v = request.FILES.get('cover_'+ str(vers['version_id']),None)            
                    if cover_v is not None:
                        with open('cover_' + str(cur_key) + "_" + str(vers['version_id']) + '.jpg', 'wb+') as destination:
                            for chunk in cover_v.chunks():
                                destination.write(chunk)
                        myversion.cover = 'http://127.0.0.1/cover_' + str(cur_key) + "_" + str(vers['version_id']) + '.jpg'
                        
                                
                    snapshot_v = request.FILES.get('thumbnail_'+ str(vers['version_id']),None)
                    if snapshot_v is not None:
                        with open('snapshot_' + str(cur_key) + "_" + str(vers['version_id']) + '.jpg', 'wb+') as destination:
                            for chunk in snapshot_v.chunks():
                                destination.write(chunk)
                        myversion.thumbnail = 'http://127.0.0.1/snapshot_' + str(cur_key) + "_" + str(vers['version_id']) + '.jpg'                   
                    
                    myversion.save()
                    player_boardgame = UserGame( user=  request.user  , boardgame = cur_bg , bg_version = myversion , owned = True , explanation = False) 
                    player_boardgame.save()
                
            else:     
                '''
                now reference current user with game added or already existing
                '''
                player_boardgame = UserGame( user=  request.user  , boardgame = cur_bg , owned = True , explanation = False) 
                player_boardgame.save()
            

            return HttpResponse(  "ok" )
        else:
            print("erreur " + str(form.errors))
            return HttpResponseForbidden()
    else:
        raise Http404("Not a POST request")
    
    
def player_boardgames( request ):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    games = UserGame.objects.select_related('bg_version', 'boardgame').filter( user__id = request.user.pk )
    
    ''' own serialization because ... pfff
    
    '''    
    datas = szs.serialize("json", games )
        
    json_datas = json.loads( datas )
    for data in json_datas:        
        bg = data['fields']['boardgame']
        v = data['fields']['bg_version']        
        pk = int(data['pk'])        
        obj_bg = []
        obj_bg.append(games.get(pk = pk).boardgame)
        data_bg = szs.serialize("json", obj_bg )        
        json_bg = json.loads( data_bg )        
        data['fields']['boardgame'] = json_bg        
        if v is not None:
            obj_v = []
            obj_v.append(games.get(pk = pk).bg_version)
            data_v = szs.serialize("json", obj_v )        
            
            json_v = json.loads( data_v )        
            data['fields']['bg_version'] = json_v    

    return HttpResponse( json.dumps(json_datas) )
    
    
    

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
            
            user = User(first_name = firstname , last_name = lastname , username = username , email = email )                     
            user.set_password( password )            
            user.save()  
            
            u = User.objects.get( pk = user.pk )            
            
            player = u.player
            player.bgg_nickname = bggnickname
            player.address = address
            player.mobile_phone = mobilephone
            player.save()
            
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
    #print (u)
    #print (u.player)
    objs.append(u)
    objs.append(u.player)
    data = szs.serialize("json" ,objs , fields=('first_name' , 'last_name' , 'address' , 'bgg_nickname') )
    return HttpResponse( data )
    