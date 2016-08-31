from django.shortcuts import render

from django.http import HttpResponse , Http404 ,HttpResponseForbidden

from django.core import serializers as szs

from server.models import BoardGame , Player

from server.forms import *

from django.contrib.auth import authenticate, login , logout




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
            
            
            count = 0
            
            cover = None
            snapshot = None
            
            try:
                cover = request.FILES['cover']            
            except:
                pass
            else:
                with open('cover_' + str(count) + '.jpg', 'wb+') as destination:
                    for chunk in cover.chunks():
                        destination.write(chunk)
                        
            try:               
                snapshot = request.FILES['snapshot']            
            except:
                pass
            else:
                with open('snapshot_' + str(count) + '.jpg', 'wb+') as destination:
                    for chunk in snapshot.chunks():
                        destination.write(chunk)
                        
            #save into database
            
            
            name            = form.cleaned_data['name']
            year            = form.cleaned_data['year']
            synopsis        = form.cleaned_data['synopsis']
            min_age         = form.cleaned_data['min_age']
            min_player      = form.cleaned_data['min_player']
            max_player      = form.cleaned_data['max_player']
            playing_time    = form.cleaned_data['playing_time']
            bgg_id          = form.cleaned_data['bgg_id']
            
            query = BoardGame(name = name , year = year , synopsis = synopsis , min_age = min_age , min_player = min_player , max_player = max_player , playing_time = playing_time , bgg_id = bgg_id )
            query.save()
            
            
            
            
            
            
                

            return HttpResponse(  "ok" )
        else:
            print("erreur " + str(form.errors))
            return HttpResponseForbidden()
    else:
        raise Http404("Not a POST request")
    
    

def add_player(request):
    if request.method == 'POST':
        print ("TOTO : " + str(request.POST)) 
        form = PlayerForm(request.POST)
        
        if form.is_valid():
            firstname       = form.cleaned_data['firstname']
            lastname        = form.cleaned_data['lastname']
            nickname        = form.cleaned_data['nickname']
            photo           = form.cleaned_data['photo']
            age             = form.cleaned_data['age']
            address         = form.cleaned_data['address']
            email           = form.cleaned_data['email']
            mobile_phone    = form.cleaned_data['mobile_phone']
            
            query = Player(firstname = firstname , lastname = lastname , nickname = nickname , photo = photo , age = age , address = address , email = email , mobile_phone = mobile_phone )
            query.save()
            
            
            
          
            data = szs.serialize("json" , Player.objects.filter( pk = query.pk ) )
            
            
            
            return HttpResponse(  data )
        else:
            raise Http404("Form is not valid : " + str(form.errors) )
    else:
        raise Http404("Not a POST request")
            