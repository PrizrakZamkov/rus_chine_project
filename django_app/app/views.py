from django.shortcuts import render

from app.models import RusChineHistory, Groups
from app.forms import RusChineForm
from django.urls import reverse


def get_menu_context(request):
    menu = [
        dict(title='Главная Страница', url=reverse('index')),
        dict(title='Страница копипаста', url=reverse('copy_page')),
    ]
    return menu


def main_page(request):
    context = {"menu": get_menu_context(request)}
    return render(request, 'index.html', context)


def copy_page(request):
    context = {"menu": get_menu_context(request)}
    delete = request.POST.get("DELETE")
    current_group_id = int(request.GET.get('current_group_id', '1'))
    current_group = Groups.objects.get(id=current_group_id)
    context['current_group'] = current_group
    if (delete):
        RusChineHistory.objects.get(id=delete).delete()
    if request.method == 'POST':
        f = RusChineForm(request.POST)
        if f.is_valid():

            rus = f.data['rus']
            chine = f.data['chine']

            item = RusChineHistory(rus=rus, chine=chine, group=current_group)
            item.save()

            context['rus'] = rus
            context['chine'] = chine
            context['form'] = f
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = RusChineForm()

    history = RusChineHistory.objects.filter(group=current_group_id)
    context["history"] = history

    context['groups'] = Groups.objects.all()

    return render(request, 'copy_page.html', context)
