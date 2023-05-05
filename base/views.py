from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Polls_details,Choice_poll,User_choices
from django.contrib.auth.decorators import login_required
from .forms import loginform,createpoll,createchoices
from django.urls import reverse
# Create your views here.

def home(request):
    authent=False
    all_polls=Polls_details.objects.all().order_by('Is_active')
    recent5=Polls_details.objects.all().order_by('Date_created')[:5]
    thevotingdictionary=[]
    
    for a in all_polls:
        listofchoices=Choice_poll.objects.filter(poll_belongsto=a.id)
        
        thevotingdictionary.append({'num': a, 'list': listofchoices})
        print(listofchoices)
    posts_contribution=[]
   
    posts_reactions=[]
    
    
    authent = request.user.is_authenticated
    if authent:
        posts_contribution=Polls_details.objects.filter(Created_by=request.user).order_by('Date_created')[:5]
        posts_reactions=User_choices.objects.filter(the_voter=request.user).order_by("the_poll")[:5]
        
    
    
    
    print('authent:', authent)
    context={
        'you':request.user,
        'authent':authent,
        'pols':all_polls,
        'recent':recent5,
        'posts_contribution':posts_contribution,
        'posts_reactions':posts_reactions,
        'thevotingdictionary':thevotingdictionary,
    }
    return render(request,'home.html',context)




def login_page(request):
    isvalidlogin=False
    form=loginform()
    Listoferrors=[]
    u=""
    user1=None
    user=[]
    if request.method=='POST':
        form=loginform(request.POST)
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        
        try:
            user=User.objects.get(username=username)
            u=user
        except:
            
            simpletext="username invalid or incorrect"
            Listoferrors.append(simpletext)
      
        user=authenticate(request,username=username,password=password)
        if user is not None:
            
            login(request,user)
           
            isvalidlogin=True
            return redirect('home')
        
        else:
            isvalidlogin=False
            
            if password != u.password:
                
                print(password)
                simpletext="password incorrect"
                print(simpletext)
                Listoferrors.append(simpletext)
            
            
            
    print(Listoferrors)
    context={'form':form,
             'isvalidlogin':isvalidlogin,
             'Listoferrors':Listoferrors,
            }
    return render(request,'log.html',context)


def register_page(request):
    page=False
    usercreation=UserCreationForm()
    if request.method=='POST':
        usercreation=UserCreationForm(request.POST)
        if usercreation.is_valid():
            user=usercreation.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
    context={
        'usercreation':usercreation,
        'page':page
    }
    return render(request,'reg.html',context)


def logout_page(request):
    logout(request)
    return redirect('home')




#functions for voting

def deletechoices(current_user,poll):
    P=User_choices.objects.filter(the_poll_id=poll.id,the_voter_id=current_user.id)
    for p in P:
        p.delete()

    return True

def check_if_votedver2(poll,current_user):

    p=User_choices.objects.filter(the_poll__id=poll.id, the_voter__id=current_user.id)
    if p.exists():
        return False
    
    return True

def getlistifvoted(poll,current_user):
    listofchoices=[]

    if not check_if_votedver2(poll,current_user):
        thelistofchoices=User_choices.objects.filter(the_poll__id=poll.id, the_voter__id=current_user.id)
        for i in thelistofchoices:
                
            listofchoices.append(i.the_choice)


    return listofchoices

def check_if_voted(current_choice,poll,current_user):

    p=User_choices.objects.filter(the_choice__id=current_choice.id,the_poll__id=poll.id, the_voter__id=current_user.id)
    if p.exists():
        return False
    
    return True


def ch_selected(selected,current_user,poll):

    for s in selected:
        user_ch=User_choices.objects.filter(the_poll_id=poll)
        
        
        if user_ch is not None:
            current_choice=Choice_poll.objects.get(id=s)
            if check_if_voted(current_choice,poll,current_user):
                current_choice.count+=1
                current_choice.save()
                print(current_choice.choices)
                user_c=User_choices.objects.create(
                    the_poll=poll,
                    the_choice=current_choice,
                    the_voter=current_user,
                    is_voted=True,

                    )
            
        else:
            return selected
                    

    return selected




@login_required(login_url="loginpage")
def poll_voting(request,pk):
    didvote=False
    cansee=False
    poll=Polls_details.objects.get(id=pk)
    choices_avaiable=poll.choice_poll_set.all()
    current_user=request.user
    listofchoices=[]
    if request.user==poll.Created_by:
        cansee=True
    

    p=User_choices.objects.filter(the_poll__id=poll.id, the_voter__id=current_user.id)
    if p.exists():
        didvote=True
        listofchoices=getlistifvoted(poll,current_user)

    else:
            if request.method=='POST':
                selected=request.POST.getlist('check_choices')
                ch_selected(selected,current_user,poll)
                p=User_choices.objects.filter(the_poll__id=poll.id, the_voter__id=current_user.id)
                if p.exists():
                    didvote=True
                    listofchoices=getlistifvoted(poll,current_user)
                else:
                    didvote=False
            
    
    context={
        'poll':poll,
        'choices_avaiable':choices_avaiable,
        'listofchoices':listofchoices,
        'didvote':didvote,
        'cansee':cansee,
    }
    return render(request,'poll_extended.html',context)


@login_required(login_url="loginpage")
def poll_create(request):
    form=createpoll()
    if request.method=='POST':
        form=createpoll(request.POST)
        print("here here")
        if form.is_valid:
            P=Polls_details.objects.create(
                Question=request.POST.get('Question'),
                Desc=request.POST.get('Desc'),
                Date_end=request.POST.get('Date_end'),
                Created_by=request.user
            )
            print("finished")
            return redirect(reverse('poll_visit', args=[P.pk]))

        
    context={'form':form}
    return render(request,'poll_create.html',context)

def choice_create(request,pk):
    form=createchoices()
    if request.method=='POST':
        form=createchoices(request.POST)
        poll=Polls_details.objects.get(id=pk)
        if form.is_valid:
            P=Choice_poll.objects.create(
                choices=request.POST.get('choices'),
                poll_belongsto=poll
                )
            print('h')
            return redirect(reverse('poll_visit', args=[pk]))
    context={'form':form,}
    return render(request,'choice_create.html',context)





def editvote(request,pk):
    
    current_user=request.user
    poll=Polls_details.objects.get(id=pk)
    choices_avaiable=poll.choice_poll_set.all()
    listofchoices=getlistifvoted(poll,current_user)

    if request.method=='POST':
        deletechoices(current_user,poll)
        selected=request.POST.getlist('check_choices')
        S=User_choices.objects.filter(the_poll_id=poll,the_voter_id=request.user.id)
        
            
        ch_selected(selected,current_user,poll)

        return redirect(reverse('poll_visit',args=[pk]))
    context={
        'choices_avaiable':choices_avaiable,
        'listofchoices':listofchoices,
    }
    return render(request,'editvote.html',context)