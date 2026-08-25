from django.shortcuts import render, redirect, get_object_or_404
from apps.users.forms import CustomUserCreationForm, CustomAuthenticationForm, EmailVerificationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from apps.users.models import User, Shop, EmailVerificationCode
import logging
from django.db.models import Q, prefetch_related_objects
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from apps.users.utils import generate_verification_code
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings


def index(request):
    shops = Shop.objects.prefetch_related("sellers").all()
    shop_filter = request.GET.get('shop', '').strip()
    if shop_filter:
        shops = shops.filter(title__iexact=shop_filter)
    q = request.GET.get('q', "").strip()
    if q:
        shops = shops.filter(
            Q(title__icontains=q)
            | Q(sellers__first_name__icontains=q)
            | Q(sellers__last_name__icontains=q)
            | Q(sellers__username__icontains=q)
        ).distinct()

        if shops:
            messages.success(request, f"Результати пошуку для запиту '{q}' ")
        else:
            messages.error(request, f"Нічого не знайдено для запиту '{q}' ")
    prefetch_related_objects(shops, "sellers")

    return render(request, "index.html", context={"shops": shops})


def render_index_with_auth_modal(request, form, active_modal, email=None):
    shops = Shop.objects.prefetch_related("sellers").all()
    return render(
        request,
        "index.html",
        context={
            "shops": shops,
            "auth_form": form,
            "active_modal": active_modal,
            "verification_email": email,
        },
    )


logger = logging.Logger(__name__)


def signup(request):
    if request.method == "GET":
        return redirect("index")

    logger.error(request.method)
    logger.error(request.user)
    logger.error(request.user.is_authenticated)
    form = CustomUserCreationForm()

    if request.method == "POST":

        if "code" in request.POST:
            form = EmailVerificationForm(request.POST)

            user_id = request.session.get("verification_user_id")
            if not user_id:
                return redirect("index")

            user = get_object_or_404(User, id=user_id)
            verification = get_object_or_404(EmailVerificationCode, user=user)

            if not form.is_valid():
                return render_index_with_auth_modal(request, form, "verify_email", user.email)

            entered_code = form.cleaned_data["code"]

            if verification.expires_at < timezone.now():
                form.add_error("code", "The verification code has expired.")
                return render_index_with_auth_modal(request, form, "verify_email", user.email)

            if entered_code != verification.code:
                form.add_error("code", "Invalid verification code.")
                return render_index_with_auth_modal(request, form, "verify_email", user.email)

            user.is_active = True
            user.save()

            verification.delete()
            request.session.pop("verification_user_id", None)

            login(request, user, "django.contrib.auth.backends.ModelBackend")

            return redirect("index")

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            code = generate_verification_code()
            verification = EmailVerificationCode.objects.update_or_create(
                user=user,
                defaults={
                "code": code,
                "expires_at": timezone.now() + timedelta(minutes=10),
            },
        )

            html_content = render_to_string(
                "emails/verification_code.html",
                {"code": code},
            )

            email = EmailMultiAlternatives(
                subject="ISAS — Email Verification",
                body=f"Your verification code is {code}. The code is valid for 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            request.session["verification_user_id"] = user.id

            return render_index_with_auth_modal(
                request,
                form,
                "verify_email",
                user.email,
            )

        context = {"form": form, "form_title": "Sign up"}
        return render_index_with_auth_modal(request, form, "signup")


def login_view(request):
    if request.method == "GET":
        return redirect("index")

    form = CustomAuthenticationForm(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        inactive_user = User.objects.filter(username=username, is_active=False).first()

        if inactive_user and inactive_user.check_password(password):
            code = generate_verification_code()

            EmailVerificationCode.objects.update_or_create(
                user=inactive_user,
                defaults={
                    "code": code,
                    "expires_at": timezone.now() + timedelta(minutes=10),
                },
            )

            html_content = render_to_string(
                "emails/verification_code.html",
                {"code": code},
            )

            email = EmailMultiAlternatives(
                subject="ISAS — Email Verification",
                body=f"Your verification code is {code}. The code is valid for 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[inactive_user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send()

            request.session["verification_user_id"] = inactive_user.id

            return render_index_with_auth_modal(
                request,
                EmailVerificationForm(),
                "verify_email",
                inactive_user.email,
            )

        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")

        return render_index_with_auth_modal(request, form, "login")
    context = {"form": form, 'form_title': "Login"}
    return render(request, 'signup.html', context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('index')


@login_required(login_url='/users/login/')
def crud_users(request):
    if not request.user.is_staff:
        return redirect("/user/redirect/")
    query = request.GET.get('q', '')
    shop_id = request.GET.get('shop')
    current_shop = None
    if shop_id:
        current_shop = get_object_or_404(Shop, pk=shop_id)
        users = User.objects.filter(shop_id=shop_id)
    else:
        users = User.objects.all()
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    return render(request, 'crud_users.html', context={'users': users, 'current_shop': current_shop})


@staff_member_required(login_url='/user/redirect/')
def user_create(request):
    shop = Shop.objects.all()
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            patronymic=request.POST.get('patronymic'),
            document_in_passport=request.POST.get('document_in_passport'),
            nn_in_passport=request.POST.get('nn_in_passport'),
            password=request.POST.get('password'),
        )
        shop_id = request.POST.get('shop')
        if shop_id:
            user.shop_id = shop_id
            user.save()
        return redirect('crud_users')
    return render(request, 'user_create.html', {'shops': shop})


@staff_member_required(login_url='/user/redirect/')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    shops = Shop.objects.all()
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.patronymic = request.POST.get('patronymic')
        user.document_in_passport = request.POST.get('document_in_passport')
        user.nn_in_passport = request.POST.get('nn_in_passport')
        shop_id = request.POST.get('shop')
        user.shop_id = shop_id if shop_id else None
        user.save()
        return redirect('crud_users')
    return render(request, 'user_edit.html', {'user_obj': user, 'shops': shops})


@staff_member_required(login_url='/user/redirect/')
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('crud_users')
    return render(request, 'user_delete.html', {'user_obj': user})


def user_redirect(request):
    return render(request, 'user_redirect.html')


@login_required(login_url='/users/login/')
def crud_shops(request):
    if not request.user.is_staff:
        return redirect("/user/redirect/")
    query = request.GET.get('q', '')
    shops = Shop.objects.all()
    if query:
        shops = shops.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'crud_shops.html', context={'shops': shops})


@staff_member_required(login_url='/user/redirect/')
def shop_create(request):
    if request.method == 'POST':
        shop = Shop.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            poster=request.FILES.get('poster'),
        )
        return redirect('crud_shops')
    return render(request, 'shop_create.html')


@staff_member_required(login_url='/user/redirect/')
def shop_edit(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.title = request.POST.get('title')
        shop.description = request.POST.get('description')
        if request.FILES.get('poster'):
            shop.poster = request.FILES.get('poster')
        shop.save()
        return redirect('crud_shops')
    return render(request, 'shop_edit.html', {'user_obj': shop})


@staff_member_required(login_url='/user/redirect/')
def shop_delete(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == 'POST':
        shop.delete()
        return redirect('crud_shops')
    return render(request, 'shop_delete.html', {'shop_obj': shop})


class ShopDetailView(DetailView):
    model = Shop
    template_name = "shop_detail.html"
    context_object_name = 'shop'

    def get_queryset(self):
        return super().get_queryset().prefetch_related("sellers")

