from django.shortcuts import render, get_object_or_404
from app.models import UserSetting, Languages, NewPhrases, NewConnections, NewConnectionsForGroup
from app.forms import WordWordForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
#from googletrans import Translator
#import googletrans
#for me rus_chine_project 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 Prizrak
#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


def get_system(user_setting_language_from):
    system_arr = NewPhrases.objects.filter(language=user_setting_language_from, is_group=False, connections__group=3)
    system = {
        "no_translate": system_arr[0].word,
        "no_synonim": system_arr[1].word,
        "title": system_arr[2].word,
        "enter": system_arr[3].word,
        "original": system_arr[4].word,
        "translate": system_arr[5].word,
        "write": system_arr[6].word,
        "list": system_arr[7].word,
        "action": system_arr[8].word,
        "copy": system_arr[9].word,
        "delete": system_arr[10].word,
        "group": NewPhrases.objects.get(language = user_setting_language_from, is_group = True, connections__group = 2).word,
        "login": system_arr[11].word,
        "logout": system_arr[12].word,
    }
    return system

def get_menu_context(request, language = None):
    menu = []
    if not language:
        menu = [
            # dict(title='Главная Страница', url=reverse('index')),
            dict(title='Phrase Book', url=reverse('new_copy_page_new')),
        ]
    else:
        menu = [
            # dict(title='Главная Страница', url=reverse('index')
            dict(title=get_system(language)["title"], url=reverse('new_copy_page_new')),
        ]
    return menu

def main_page(request):
    context = {"menu": get_menu_context(request)}

    return render(request, 'index.html', context)

def check_language_1(request, current_user):
    language_1 = request.POST.get("LANGUAGE_1")
    if (language_1):
        try:
            tmp = UserSetting.objects.get(user = current_user)
            tmp.language_from = Languages.objects.get(id = language_1)
            tmp.save()
        except:
            print("error")

def check_language_2(request, current_user):
    language_2 = request.POST.get("LANGUAGE_2")
    if (language_2):
        try:
            tmp = UserSetting.objects.get(user = current_user)
            tmp.language_to = Languages.objects.get(id = language_2)
            tmp.save()
        except:
            print("error")

def update_group_name(current_group_connection, no_translate, user_setting):
    if (NewPhrases.objects.filter(connections=current_group_connection, language=user_setting.language_from)):
        return NewPhrases.objects.get(connections=current_group_connection,
                                                               language=user_setting.language_from).word
    elif (NewPhrases.objects.filter(connections=current_group_connection, language=user_setting.language_to)):
        return no_translate + NewPhrases.objects.get(connections=current_group_connection,
                                                                              language=user_setting.language_to).word
    else:
        return no_translate

@login_required
def new_copy_page_new(request):
    current_user = request.user

    user_setting = UserSetting.objects.get(user = current_user)
    context = {}
    context['current_group'] = user_setting.current_group
    current_group_connection = NewConnections.objects.filter(group = user_setting.current_group)
    current_group_language = user_setting.language_from

    context["menu"] = get_menu_context(request,user_setting.language_from)

    system = get_system(user_setting.language_from)
    no_translate = system["no_translate"]
    no_synonim = system["no_synonim"]
    context["system"] = system

    is_group = False
    if(NewConnections.objects.filter(group = user_setting.current_group)[0].id == 2):
        is_group = True
    context["is_group"] = is_group

    context['current_group_name'] = update_group_name(current_group_connection[0],no_translate,user_setting)

    context["language_list"] = Languages.objects.all()
    if request.method == 'POST':
        check_language_1(request, current_user)
        check_language_2(request, current_user)

        user_setting = UserSetting.objects.get(user=current_user)

        shift_languages = request.POST.get("SHIFT_LANGUAGES")
        if (shift_languages):
            tmp = user_setting.language_from
            user_setting.language_from = user_setting.language_to
            user_setting.language_to = tmp
            user_setting.save()

        system = get_system(user_setting.language_from)
        no_translate = system["no_translate"]
        no_synonim = system["no_synonim"]
        context["system"] = system

        current_group_post = request.POST.get("GROUP")
        if(current_group_post):
            user_setting.current_group = NewConnectionsForGroup.objects.get(id = current_group_post)
            #user_setting.current_group = current_group_post
            user_setting.save()
            context['current_group'] = user_setting.current_group




        delete = request.POST.get("DELETE")
        if (delete):
            try:
                tmp = NewPhrases.objects.get(id=delete)
                tmp.delete()
                print("delete")
            except:
                print("id", delete, "is not exist")

        change_word = request.POST.get("CHANGE_GROUP")
        if (change_word):
            print("change")
            change_group, change_word = map(int, change_word.split(";"))
            tmp1 = NewPhrases.objects.filter(connections=change_word)
            is_exist = False
            is_exist_tmp4 = None
            for tmp4 in tmp1:
                if NewPhrases.objects.filter(word=tmp4.word, connections__group=change_group):
                    NewPhrases.objects.get(word=tmp4.word, connections__group=user_setting.current_group).delete()
                    is_exist = True
                    is_exist_tmp4 = tmp4.word
            if is_exist:
                print("est")
                tmp = NewConnections.objects.get(id=change_word)
                tmp_new = NewPhrases.objects.filter(word=is_exist_tmp4, connections__group=change_group)[0]
                for tmp_for_change_connect in NewPhrases.objects.filter(connections = tmp):
                    tmp_for_change_connect.connections = tmp_new.connections
                    tmp_for_change_connect.save()
                tmp.delete()
            else:
                try:
                    tmp = NewConnections.objects.get(id=change_word)
                    tmp.group = NewConnectionsForGroup.objects.get(id=change_group)
                    tmp.save()
                except:
                    print("error")

        is_group = False
        if (NewConnections.objects.filter(group=user_setting.current_group)[0].id == 2):
            is_group = True
        context["is_group"] = is_group

        f1 = WordWordForm(request.POST)
        word_1 = ""
        word_2 = ""
        if f1.is_valid():
            word_1 = f1.data['word_1']
            word_2 = f1.data['word_2']
            if not is_group:
                print("form correct")
                tmp1 = NewPhrases.objects.filter(word = word_1, connections__group = user_setting.current_group, is_group = False)
                tmp2 = NewPhrases.objects.filter(word = word_2, connections__group = user_setting.current_group, is_group = False)
                print(tmp1, tmp2)
                if tmp1 and tmp2:
                    print("tmp1 tmp2 exist")
                    tmp2 = NewPhrases.objects.filter(connections = tmp2[0].connections, is_group = False)
                    for item in tmp2:
                        tmp_for_change_connect = NewPhrases.objects.get(id = item.id)
                        tmp_for_change_connect.is_group = False
                        tmp_for_change_connect.connections = tmp1[0].connections
                        tmp_for_change_connect.save()
                elif tmp1:
                    print("tmp1 exist")
                    tmp2 =  NewPhrases(word=word_2, language=user_setting.language_to, connections = tmp1[0].connections, is_group = False)
                    tmp2.save()
                elif tmp2:
                    print("tmp2 exist")
                    tmp1 =  NewPhrases(word=word_1, language=user_setting.language_from, connections = tmp2[0].connections, is_group = False)
                    tmp1.save()
                else:
                    print("nothing exist")
                    newconnection = NewConnections(group = user_setting.current_group, is_group = False)
                    newconnection.save()
                    NewPhrases(word = word_1, language = user_setting.language_from, connections = newconnection, is_group = False).save()
                    NewPhrases(word = word_2, language = user_setting.language_to, connections = newconnection, is_group = False).save()

            else:
                print("form correct (group)")
                tmp1 = NewPhrases.objects.filter(word=word_1, is_group = True)
                tmp2 = NewPhrases.objects.filter(word=word_2, is_group = True)
                print(tmp1,tmp2)
                print(word_1, word_2)
                if (word_1 != word_2):
                    if tmp1 and tmp2:
                        print("tmp1 tmp2 exist")
                        '''
                        tmp2 = NewPhrases.objects.filter(connections=tmp2[0].connections, is_group = True)
                        print(tmp2)
                        for item in tmp2:
                            tmp_for_change_connect = NewPhrases.objects.get(id=item.id)
                            tmp_for_change_connect.is_group = True
                            tmp_for_change_connect.connections = tmp1[0].connections
                            tmp_for_change_connect.save()'''

                    elif tmp1:
                        print("tmp1 exist")
                        tmp2 = NewPhrases.objects.filter(language=user_setting.language_to, connections=tmp1[0].connections, is_group = True)
                        if (tmp2):
                            tmp2 = tmp2[0]
                            tmp2.word = word_2
                        else:
                            tmp2 = NewPhrases(language=user_setting.language_to, connections=tmp1[0].connections, is_group = True)

                        tmp2.save()

                    elif tmp2:
                        print("tmp2 exist")
                        tmp1 = NewPhrases.objects.filter(language=user_setting.language_from, connections=tmp2[0].connections, is_group = True)
                        if (tmp1):
                            tmp1 = tmp1[0]
                            tmp1.word = word_1
                        else:
                            tmp1 = NewPhrases(language=user_setting.language_from, connections=tmp2[0].connections, is_group = True)

                        tmp1.save()
                    else:
                        print("nothing exist")
                        new_group = NewConnectionsForGroup()
                        new_group.save()
                        newconnection = NewConnections(group=new_group, is_group = True)
                        newconnection.save()
                        NewPhrases(word=word_1, language=user_setting.language_from, connections=newconnection, is_group = True).save()
                        NewPhrases(word=word_2, language=user_setting.language_to, connections=newconnection, is_group = True).save()

        else:
            context['form1'] = f1

        context['word_1'] = word_1
        context['word_2'] = word_2
        context['form1'] = WordWordForm()
    else:
        context['nothing_entered'] = True
        context['form1'] = WordWordForm()

    context["new_history"] = []


    user_setting = UserSetting.objects.get(user = current_user)
    context["language_1"] = user_setting.language_from
    context["language_2"] = user_setting.language_to

    context["menu"] = get_menu_context(request,user_setting.language_from)

    context['current_group'] = user_setting.current_group
    current_group_connection = NewConnections.objects.filter(group = user_setting.current_group)
    current_group_language = user_setting.language_from
    if (NewPhrases.objects.filter(connections = current_group_connection[0], language = current_group_language)):
        context['current_group_name'] = NewPhrases.objects.get(connections = current_group_connection[0], language = current_group_language).word
    elif (NewPhrases.objects.filter(connections=current_group_connection[0], language=user_setting.language_to)):
        context['current_group_name'] = no_translate + NewPhrases.objects.get(connections=current_group_connection[0],
                                                               language=user_setting.language_to).word
    else:
        context['current_group_name'] = no_translate



    system = get_system(user_setting.language_from)
    no_translate = system["no_translate"]
    no_synonim = system["no_synonim"]
    context["system"] = system


    groups = []

    for i in NewConnectionsForGroup.objects.all():
        if (i.id != 3):
            current_group_connection_tmp = NewConnections.objects.filter(group = i)
            current_group_language_tmp_from = user_setting.language_from
            current_group_language_tmp_to = user_setting.language_to
            if (NewPhrases.objects.filter(connections=current_group_connection_tmp[0], language=user_setting.language_from)):
                groups.append(
                    {
                        "group": i.id,
                        "group_name": NewPhrases.objects.get(connections=current_group_connection_tmp[0],
                                                             language=current_group_language_tmp_from).word
                    }
                )
            elif (NewPhrases.objects.filter(connections=current_group_connection_tmp[0], language=user_setting.language_to)):
                groups.append(
                    {
                        "group": i.id,
                        "group_name": no_translate + NewPhrases.objects.get(connections=current_group_connection_tmp[0],
                                                                                language=current_group_language_tmp_to).word
                    }
                )

    context['groups'] = groups
    is_group = False
    if(NewConnections.objects.filter(group = user_setting.current_group)[0].id == 2):
        is_group = True
    context["is_group"] = is_group
    if(not is_group):

        connections3 = NewConnections.objects.filter(group=user_setting.current_group, is_group = False)
        tmp_i = 0
        if connections3:
            for i in connections3:
                phrase_1 = NewPhrases.objects.filter(connections__group=user_setting.current_group,
                                                     language=user_setting.language_from, connections=i, is_group=False)
                for k in range(len(phrase_1)):
                    phrase_2 = NewPhrases.objects.filter(connections__group=user_setting.current_group,
                                                         language=user_setting.language_to, connections=i,
                                                         is_group=False)
                    synonim = False
                    for l in range(len(phrase_2)):
                        if (phrase_1[k].word != phrase_2[l].word):
                            context["new_history"].append(
                                {"group": i.group, "first": phrase_1[k].word, "second": phrase_2[l].word,
                                 "id": tmp_i, "connection_id": i.id, "first_word_id": phrase_1[k].id, "is_group": is_group})
                            tmp_i += 1
                            synonim = True
                    if(not synonim) and user_setting.language_from==user_setting.language_to:
                        context["new_history"].append(
                            {"group": i.group, "first": phrase_1[k].word, "second": no_synonim, "id": tmp_i,
                             "connection_id": i.id, "first_word_id": phrase_1[k].id, "is_group": is_group})
                        tmp_i += 1
    else:
        connections3 = NewConnections.objects.filter(is_group = True)
        tmp_i = 0
        if connections3:
            for i in connections3:
                print(i.group)
                if (i.group != NewConnectionsForGroup.objects.get(id=3)):
                    phrase_1 = NewPhrases.objects.filter(
                                                         language=user_setting.language_from, connections=i,
                                                         is_group=True)
                    if(phrase_1):
                        for k in range(len(phrase_1)):
                            phrase_2 = NewPhrases.objects.filter(
                                                                 language=user_setting.language_to, connections=i,
                                                                 is_group=True)
                            if (phrase_2):
                                for l in range(len(phrase_2)):

                                    # if(user_setting.language_from != user_setting.language_to and phrase_1[k].word != phrase_2[l].word):
                                    if (phrase_1[k].word != phrase_2[l].word):
                                        context["new_history"].append(
                                            {"first": phrase_1[k].word, "second": phrase_2[l].word,
                                             "id": tmp_i, "connection_id": i.id, "first_word_id": phrase_1[k].id, "is_group": is_group})
                                    else:
                                        context["new_history"].append(
                                            {"first": phrase_1[k].word, "second": "", "id": tmp_i,
                                             "connection_id": i.id, "first_word_id": phrase_1[k].id, "is_group": is_group})
                                    tmp_i += 1
                            else:
                                context["new_history"].append(
                                    {"first": phrase_1[k].word, "second": no_translate, "id": tmp_i,
                                     "connection_id": i.id, "first_word_id": phrase_1[k].id, "is_group": is_group})
                                tmp_i += 1
                    else:
                        phrase_2 = NewPhrases.objects.filter(
                            language=user_setting.language_to, connections=i,
                            is_group=True)
                        if (phrase_2):
                            for l in range(len(phrase_2)):
                                context["new_history"].append(
                                        {"first": no_translate, "second": phrase_2[l].word,
                                         "id": tmp_i, "connection_id": i.id, "first_word_id": 0,
                                         "is_group": is_group})
                                tmp_i += 1

    return render(request, 'new_copy_page_new.html', context)
