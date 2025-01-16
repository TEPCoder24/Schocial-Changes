from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from .models import PostModel, ProfileModel
from datetime import datetime

# Create your views here.
def home_page_load(request):
	dt = datetime.now()
	if dt.isoweekday() == 6 or dt.isoweekday() == 7:
		return redirect("closed")
	elif not request.user.is_authenticated:
		return redirect("welcome")
	else:
		tot_posts = list(PostModel.objects.all())[::-1]
		print(tot_posts)
		profile = get_object_or_404(ProfileModel, username=request.user.username)
		context={}
		context["userpost"] = tot_posts
		context["profile"] = profile
		if request.method == "POST":
			text = request.POST.get("text")
			img = request.FILES.get("img")
			vid = request.FILES.get("vid")
			time = datetime.now().strftime("%H:%M:%S")
			if text and img and vid:
				post = PostModel(username=request.user.username, text=text, img=img, vid=vid, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif text and img:
				post = PostModel(username=request.user.username, text=text, img=img, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif text and vid:
				post = PostModel(username=request.user.username, text=text, vid=vid, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif img and vid:
				post = PostModel(username=request.user.username, img=img, vid=vid, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif text:
				post = PostModel(username=request.user.username, text=text, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif img:
				post = PostModel(username=request.user.username, img=img, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
			elif vid:
				post = PostModel(username=request.user.username, vid=vid, grade=profile.grade, pfp=profile.pfp, time=time)
				post.save()
				return redirect("home")
		return render(request, "home.html", context=context)

def welcome_page_load(request):
	dt = datetime.now()
	if dt.isoweekday() == 6 or dt.isoweekday() == 7:
		return redirect("closed")
	else:
		return render(request,"welcome.html")

def user_page_load(request): 
	context = {}
	dt = datetime.now()
	if dt.isoweekday() == 6 or dt.isoweekday() == 7:
		return redirect("closed")
	elif not request.user.is_authenticated:
		return redirect("welcome")
	else:
		username = request.user.username
		profile = get_object_or_404(ProfileModel, username=username)
		context["username"] = username
		context["grade"] = profile.grade
		context["pfp"] = profile.pfp
		if request.method == "POST":
			new_pfp = request.FILES.get("upload")
			current_user = ProfileModel.objects.get(username=username)
			updated_user = ProfileModel(username=username, grade=current_user.grade, pfp=new_pfp)
			updated_user.save()
			current_user.delete()
			tot_posts = PostModel.objects.all()
			for post in tot_posts:
				if post.username == username:
					post.pfp = new_pfp
					post.save()
			return redirect("user")
		return render(request, "user.html", context)

def login_page_load(request):
	dt = datetime.now()
	if dt.isoweekday() == 6 or dt.isoweekday() == 7:
		return redirect("closed")
	elif request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect("home")
		else:
			return redirect("login")
	else:
		return render(request, "registration/login.html", {})

def signup_page_load(request):
	dt = datetime.now()
	if dt.isoweekday() == 6 or dt.isoweekday() == 7:
		return redirect("closed")
	elif request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password1"]
			grade = form.cleaned_data["grade"]
			pfp = request.FILES.get("pfp")
			profile = ProfileModel(username=username, grade=grade, pfp=pfp)
			profile.save()
			user = authenticate(username=username, password=password, email=email)
			login(request, user)
			return redirect("home")
	else:
		form = CustomUserCreationForm()

	return render(request, "registration/signup.html", {"form": form})

def logout_user(request):
	logout(request)
	return redirect("welcome")

def closed_site(request):
	dt = datetime.now()
	if dt.isoweekday() != 6 or dt.isoweekday() != 7:
		return redirect("welcome")
	return render(request, "closed.html")

def like_function(request, pk):
	if request.user.is_authenticated:
		post = get_object_or_404(PostModel, id=pk)
		if post.likes.filter(id=request.user.id):
			post.likes.remove(request.user)
		else:
			post.likes.add(request.user)
		return redirect("home")
	else:
		return redirect('welcome')

def dislike_function(request, pk):
	if request.user.is_authenticated:
		post = get_object_or_404(PostModel, id=pk)
		if post.dislikes.filter(id=request.user.id):
			post.dislikes.remove(request.user)
		else:
			post.dislikes.add(request.user)
		return redirect("home")
	else:
		return redirect('welcome')

def delete(request, pk):
	post = get_object_or_404(PostModel, id=pk)
	PostModel.delete(post)
	return redirect("home")