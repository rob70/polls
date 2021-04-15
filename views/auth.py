from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages



def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("polls:min-side")
    else:
        form = UserCreationForm()

    return render(request, "polls/auth/signup.html", {"form": form})


class LoginView(BaseLoginView):
    template_name = "polls/auth/login.html"
    redirect_authenticated_user = True


logg_inn = LoginView.as_view()

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()            
            username = form.cleaned_data.get('username')
            messages.success(request, f"Din konto er opprettet: {username}")
            # logges brukeren inn?
            login(request, user)
            return redirect("polls:min-side")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request = request,
                          template_name = "polls/auth/signup.html",
                          context={"form":form})
    form = UserCreationForm
    return render(request = request,
                  template_name = "polls/auth/signup.html",
                  context={"form":form})

def logout_request(request):
    
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("polls:index")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
            
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})

