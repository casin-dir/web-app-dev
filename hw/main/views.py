from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.views import View

from django.http import HttpResponse, JsonResponse

# local imports
from .models import Team
from .forms import AuthForm, RegistrationForm, AddTeamForm

from django.core.files import File
from django.core.files.storage import FileSystemStorage


from django.contrib.staticfiles.templatetags.staticfiles import static
import os


# Create your views here.

    
# Base for all View instances in my code, 
#   modifies context to render base.html properly
class BaseView(View):
    def get(self, request, template, context):
        context.update ({
            'authorized' : request.user.is_authenticated,
            'user' : { 'name' : request.user.username },
        })
        
        return render(request, template, context)
    
    
# View displaying 2 forms : AuthForm & RegistrationForm
class LogRegView(BaseView):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
       
        authForm = AuthForm()
        regForm = RegistrationForm()
        
        return super().get(request, 'registration/login.html', {
                'registration_form': regForm,
                'login_form' : authForm,
            })

            
# register new user & login it
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Data should be POSTed to this URL'})
    username = request.POST.get("username")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    if (password1 == password2):
        
        if (User.objects.filter(username = username).exists()):
            return JsonResponse({"error" : "Данный логин занят, придумайте, пожалуйста, другой."})
            
        # register now    
        user = User.objects.create_user(username = username, password = password1)
        request.POST = request.POST.copy()
        request.POST["password"]=password1
        return auth(request)

    return JsonResponse({'error': 'Пароли не равны.'})
  

# login users  
def auth(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Data should be POSTed to this URL'})
    form = AuthForm(request.POST)
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
        return JsonResponse({'error': 'NO'})
    return JsonResponse({'error': 'Неверный логин или пароль, если Вы злоумышленник - идите отсюда. Но если Вы просто проверяете валидацию - то она работает, будьте уверены.'})

    
# returns requested page
def page_request(request, page_id):
    context = {
        'teams' : ObjectListView.get_page_dict(page_id),
    }
    return render_to_response('main/base_list.html', context)
    
    
    
# Main Page view, lists all objects
class ObjectListView(BaseView): 
    objOnList = 10
    
    
    def get_page_dict(page_id):
        page_id = int(page_id)
        st_pos = len(Team.objects.all()) - ObjectListView.objOnList * page_id
        end = st_pos if st_pos > 0 else 0
        start = end - ObjectListView.objOnList if end > ObjectListView.objOnList else 0
        
        #need to cut description
        all = Team.objects.all()[start: end][::-1]
        
        for i in all:
            if len(i.desc) > 200:
                i.desc = i.desc[:200] + '...'
        return all
        
        
    def get(self, request):
        return super().get(
            request, 
            'main/main.html', 
            context = {
                'name' : 'Teams',
                'teams': ObjectListView.get_page_dict(0),
                'add_form' : AddTeamForm(),
            }
        )

    def post(self, request):
        form = AddTeamForm(request.POST)
        
        if form.is_valid():
            team = form.fill_object()
            
            #saving file
            f = request.FILES.get("image")
            
            if f is None:
                file_url = r'images/default.jpg'
            else:
                file_url = r'images/pokemons/%d%s' % (team.id, '.jpg')
                filename = FileSystemStorage().save('main/static/' + file_url, File(f))
            
            team.imageUrl = file_url
            team.save()
            return redirect('single_object', team_id=team.id)
        return JsonResponse(form.errors)

        
# View 
class ObjectView(BaseView):
    def get(self, request, team_id):
        obj = get_object_or_404(Team, id = team_id)

        context = {
            'team' : obj,
            'status' : obj.betUsers.filter(id=request.user.id).exists()
        }
        return super().get(request, 'object/object.html', context)
        
    # @login_required(redirect_field_name='login_url')
    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        if request.user.is_authenticated():
            state = request.POST.get('state')
            
            rel = team.betUsers.filter(id=request.user.id).exists()
            if state == 'True' and not rel:
                    team.betUsers.add(request.user)
            
            if state == 'False' and rel:
                    team.betUsers.remove(request.user)
        
        return render_to_response(
            'object/base_user_list.html', 
            { 'users' : team.betUsers.all() }
        )

        

        

    