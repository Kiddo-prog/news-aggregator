from msilib.schema import ListView
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Article

# form class
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm

# pip install feedparser apscheduler
# feeds -  yahoo, cnn, reddit


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Article
    context_object_name = "news_list"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pub_date")[:10]
        return context


def contact_page(request):
    if request.method == "GET":
        form = ContactForm(request.GET)
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            try:
                send_mail(
                    subject, message, email, {"admin@example.com"}, fail_silently=False
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("success")
    return render(request, "contact.html", {"form": form})


def success_page(request):
    return render(request, "success.html", {})


def search_view(request):
    if request.method == "POST":
        searched = request.POST["search"]
        filter_search = Article.objects.filter(title__contains=searched)
        context = {
        'filter_search': filter_search, 
        'searched': searched
        }
        return render(request, "search.html", context)
    else:
        return render(request, "search.html")
