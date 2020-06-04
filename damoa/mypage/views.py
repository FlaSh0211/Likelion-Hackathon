from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import (authenticate, login as django_login, logout as django_logout)
from django.contrib.auth.models import User
from auction.models import Write, Bid
from django.utils.safestring import mark_safe
import json
def mymain(request):
    username = request.user.username
    print(request.user.is_authenticated)
    try:
        if request.user.is_authenticated:
            print("1"*10)
            userdata = {
                "username" : request.user.username
                }
                
            loggeduser = request.user.username
            loggedid = request.user.id
            post = Write.objects.filter(writer = loggeduser) #내가 등록한 글
            post2 = Bid.objects.filter(userId_id = loggedid) #내가 입찰한 글
            
            
            context = {"userdata":userdata, "post":post, "post2":post2,'username': mark_safe(json.dumps(username)),'userid':mark_safe(json.dumps(loggedid)) }
            return render(request, "mypage/mymain.html", context)
        else:
            return redirect("/")

    except:
        return render(request, "mypage/error.html")

