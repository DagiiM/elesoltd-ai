from django.shortcuts import render, get_object_or_404, redirect
from .models import Email
from .forms import EmailForm, EmailReplyForm
from datetime import timezone

def email_list(request):
    emails = Email.objects.all()
    context = {'emails': emails}
    return render(request, 'mails/email_list.html', context)

def email_detail(request, pk):
    email = get_object_or_404(Email, pk=pk)
    context = {'email': email}
    return render(request, 'mails/email_detail.html', context)

def email_compose(request):
    form = EmailForm()
    return render(request, 'mails/email_compose.html', {'form': form})

def email_draft(request, pk):
    email = get_object_or_404(Email, pk=pk)
    context = {'email': email}
    return render(request, 'mails/email_draft.html', context)

def email_send(request, pk):
    email = get_object_or_404(Email, pk=pk)
    email.draft = False
    email.send_time = timezone.now()
    email.save()
    return redirect('email_detail', pk=pk)

def email_delete(request, pk):
    email = get_object_or_404(Email, pk=pk)
    email.delete()
    return redirect('email_list')
