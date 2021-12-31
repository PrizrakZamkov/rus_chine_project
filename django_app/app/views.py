from django.shortcuts import render, get_object_or_404

from app.models import RusChineHistory, Groups
from app.forms import RusChineForm, AddGroupForm
from django.urls import reverse


def get_menu_context(request):
    menu = [
        dict(title='Главная Страница', url=reverse('index')),
        dict(title='Страница копипаста', url=reverse('copy_page')),
        dict(title='Редактирование групп', url=reverse('add_group')),
    ]
    return menu


def main_page(request):
    context = {"menu": get_menu_context(request)}
    return render(request, 'index.html', context)


def add_group(request):
    context = {"menu": get_menu_context(request)}

    if request.method == 'POST':
        delete = request.POST.get("DELETE")
        if (delete):
            try:
                if(id != 1 and id != 2):
                    Groups.objects.get(id=delete).delete()
                else:
                    print("it is default or deleted group")
            except:
                print("id",delete,"is not exist")

        f = AddGroupForm(request.POST)
        if f.is_valid():

            group = f.data['group']

            item = Groups(group=group)
            item.save()

            context['group'] = group
        else:
            context['form'] = f
    else:
        context['nothing_entered'] = True
        context['form'] = AddGroupForm()

    context["history"] = Groups.objects.all()

    return render(request, 'add_group.html', context)

def copy_page(request):
    context = {"menu": get_menu_context(request)}
    current_group_id = request.POST.get("GROUP")
    if(not current_group_id):
        current_group_id = 1

    current_group = Groups.objects.get(id=current_group_id)
    context['current_group'] = current_group

    if request.method == 'POST':

        restore = request.POST.get("RESTORE")
        if (restore):
            try:
                tmp = RusChineHistory.objects.get(id=restore)
                item = RusChineHistory(group=Groups.objects.get(id=1), rus=tmp.rus, chine=tmp.chine)
                item.save()
                RusChineHistory.objects.get(id=restore).delete()
            except:
                print("id",restore,"is not exist")
        delete = request.POST.get("DELETE")
        if (delete):
            try:
                tmp = RusChineHistory.objects.get(id=delete)
                if (tmp.group.id != 2):
                    item = RusChineHistory(group=Groups.objects.get(id=2), rus=tmp.rus, chine=tmp.chine)
                    item.save()
                RusChineHistory.objects.get(id=delete).delete()
            except:
                print("id",delete,"is not exist")

        delete_all = request.POST.get("DELETE_ALL")
        if (delete_all):
            try:
                RusChineHistory.objects.filter(group=delete_all).delete()#всегда 2 - делетед
            except:
                print("id",delete_all,"is not exist")


        current_group = Groups.objects.get(id=current_group_id)
        context['current_group'] = current_group

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
    context["isDeletedGroup"] = False
    if int(current_group_id) == 2:
        context["isDeletedGroup"] = True
    return render(request, 'copy_page.html', context)
