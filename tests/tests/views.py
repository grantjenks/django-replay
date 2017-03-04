from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Essay, Comment


def index(request):
    essays = Essay.objects.exclude(publish_date=None)
    essays = essays.order_by('-publish_date')
    return render(request, 'tests/index.html', locals())


def essay(request, essay_id):
    essay = get_object_or_404(Essay, id=int(essay_id))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.essay = essay
            comment.save()
            return redirect('essay', essay.id)
    else:
        form = CommentForm()

    comments = essay.comment_set.order_by('-date')
    return render(request, 'tests/essay.html', locals())
