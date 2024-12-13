from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="/login")
def profile(request):
    from .forms import ChangeImageForm

    if request.method == 'POST':
        image_form=ChangeImageForm(request.POST, request.FILES, instance=request.user.profile)

        if image_form.is_valid():
            image_form.save()
            messages.success(request, "Image uploaded successfully!")
        else:
            for error in list(image_form.errors.values()):
                messages.error(request, error)


    image_form=ChangeImageForm()

    return render(request, './users/profile.html', {
        "image_form": image_form
        })


def login(request):
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth import authenticate, login
    from .forms import LoginForm
    if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                

                user=authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
                
                if user is not None:
                    login(request, user)
                    messages.success(request,"Authentication")
                    return redirect('/')

                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
            else:
                messages.error(request,"Not Found")
    else:
        form=LoginForm()
    return render(request, './users/login.html', {'form':form})

# Create your views here.

def registration(request):
    from .forms import RegistrationForm
    from django.contrib.auth import login
    from .models import Profile

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            # user.is_active=False
            user.save()

            profile=Profile.objects.create(user=user)
            profile.save()

            if activate_email(user, user.email, "Blog App. Activate your email!","emails/activate_email.html"):
                messages.info(request, f"Dear {user.username}, check your email {user.email} to confirm registration!")
            else:
                messages.error(request, f"Failed to send email to {user.email}. Please try again!")


            # login(request, user)
            return redirect('/login')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form=RegistrationForm()
    
    return render(request, './users/registration.html', {'form':form})

@login_required(login_url="/login")
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request,"Logout ok!")
    return redirect('/')

def activate_email(user, to_email,subject:str, html_file_path:str ):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from .token import account_activation_token


    # subject = 'Activate Your Blog Account'
    uid=urlsafe_base64_encode(force_bytes(user.pk))
    # print("Uid:",uid)

    token=account_activation_token.make_token(user)
    # print("Token:",token)

    message=render_to_string(html_file_path, {
    'user':user,
    'uid': uid,
    'token':token
    })

    email=EmailMultiAlternatives(
    subject,
    message,
    to=[to_email]
    )
    email.attach_alternative(message, "text/html")

    return email.send()

def activate(request, token, uid):
    # print("Token:",token,"uid:", uid)
    from django.contrib.auth.models import User
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    from .token import account_activation_token

    try: 
        uid= force_str(urlsafe_base64_decode(uid))
        user=User.objects.get(pk=uid)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user, token):
        profile=user.profile
        profile.activated=True
        profile.save()
        messages.info(request, "Your account has been activated. You can now login!")
        return redirect("login")
    else:
        messages.error(request, "The activation link is invalid or expired. Please try again!")
        return redirect("registration")

# def confirm_login_allowed(self, user: AbstractBaseUser) -> None:
#     if not user.is_active:
#         raise forms.ValidationError(f"Check your email: {user.email} and confirm your acccount first!")
#     return super().confirm_login_allowed(user)

@login_required(login_url="/login")
def toggle_save_post(request, post_id):
    from django.shortcuts import get_object_or_404
    from core.models import Post
    post=get_object_or_404(Post, pk=post_id)
    profile=request.user.profile

    if post in profile.saved_posts.all():
        profile.saved_posts.remove(post)
        messages.info(request, "Removed saved post")
    else:
        profile.saved_posts.add(post)
        messages.info(request, "Saved post")

    return redirect('/')

@login_required(login_url="/login")
def change_email(request):
    if request.method == "POST":
        email=request.POST.get("email")
        if email:
            user=request.user
            user.email=email
            user.save()

            user.profile.activated=False
            user.profile.save()

            if activate_email(user, email, "Blog App. Confirm your email to change it!", "emails/change_email.html"):
                messages.info(request, f"Dear {user.username}, check your email {email} to confirm it!")
            else:
                messages.error(request, f"Failed to send email to {email}. Please try again!")

    return redirect("/profile")

@login_required(login_url="/login")
def change_password(request):
    from django.contrib.auth.password_validation import validate_password
    from django.contrib.auth import update_session_auth_hash
    from django.core.exceptions import ValidationError

    if request.method == "POST":
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        user=request.user

        if password != confirm_password:
            messages.error(request, "Password do not match!")
            return redirect("/profile")
        
        try:
            validate_password(password, user)
            user.set_password(password)
            user.save()

            update_session_auth_hash(request, user)

            messages.info(request,"Password changed")


        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect("/profile")



    return redirect("/profile")


def reset_password(request):
    from django.contrib.auth.forms import PasswordResetForm
    from django.contrib.auth.models import User
    form=PasswordResetForm()

    if request.method == "POST":
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            user_email=form.cleaned_data["email"]
            user=User.objects.filter(email=user_email).first()
            if user:
                if activate_email(user, user_email, "Blog App. Reset password!", "emails/reset_password.html"):
                    messages.info(request, f"Dear {user.username}, check your email {user_email} to confirm it!")
                else:
                    messages.error(request, f"Failed to send email to {user_email}. Please try again!")

            else:
                messages.error(request, f"No user founf with the email")
                return redirect("password_reset")
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        

    return render(request, "users/password_reset.html", {'form': form})
def reset_password_confirm(request, token, uid):
    from django.contrib.auth.forms import SetPasswordForm
    from django.contrib.auth.models import User
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    from .token import account_activation_token

    try: 
        uid = force_str(urlsafe_base64_decode(uid))
        user=User.objects.get(pk=uid)

    except:
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form= SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Your password haas been set. You can log in now!")

                return redirect("login")

            else:
                for error in list(form.errors.values()):
                    messages.error(request,error )
        else:
            form=SetPasswordForm(user) 
            return render(request, "users/password_reset.html", {"form":form})


    else:
        messages.error(request, "The activation link is invalid or expired. Please try again!")
    return redirect("login")
