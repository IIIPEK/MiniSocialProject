# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from accounts.models import CustomUser
from .models import Thread, Message
from .forms import MessageForm
from utils.settings import get_user_settings
from utils.templatetags.rights import can_interact


@login_required
def thread_list(request):
    threads = request.user.threads.all().prefetch_related("participants")
    return render(request, "messaging/thread_list.html", {"threads": threads})


@login_required
def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk, participants=request.user)
    print(request.headers.get('x-requested-with'), request.GET.get('ajax'))

    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if not can_interact(request.user):
            messages.error(request, "Вы не можете отправлять сообщения.")
            return redirect("messaging:thread_detail", pk=pk)

        message = form.save(commit=False)
        message.thread = thread
        message.sender = request.user
        message.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('messaging/includes/message_item.html', {'message': message}, request=request)
            return JsonResponse({'html': html})

        return redirect("messaging:thread_detail", pk=pk)

    messages_qs = thread.messages.select_related("sender").order_by('created_at')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.GET.get('ajax'):
        html = render_to_string('messaging/includes/message_list.html', {'messages_qs': messages_qs, 'user': request.user})
        return JsonResponse({'html': html})

    return render(request, "messaging/thread_detail.html", {
        "thread": thread,
        "messages_qs": messages_qs,
        "form": form,
        'refresh_interval': get_user_settings('CHAT_REFRESH_INTERVAL'),
    })


@login_required
def start_thread(request, nickname):
    recipient = get_object_or_404(CustomUser, nickname=nickname)
    if recipient == request.user:
        messages.error(request, "Нельзя писать самому себе.")
        return redirect("accounts:public_profile", nickname=nickname)

    # Ищем существующий чат между двумя пользователями
    existing_thread = Thread.objects.filter(participants=request.user).filter(participants=recipient).first()

    if existing_thread:
        return redirect("messaging:thread_detail", pk=existing_thread.pk)

    # Создаем новый чат
    thread = Thread.objects.create()
    thread.participants.add(request.user, recipient)
    return redirect("messaging:thread_detail", pk=thread.pk)
