from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic.edit import CreateView
from .forms import PostForm

from .models import Choice, Question, Comment


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class CommentView(CreateView):
    model = Comment
    form_class = PostForm
    success_url = 'list/'

class CommentListView(generic.ListView):
    model = Comment(title='', comment_text='')
    template_name = 'polls/comment-list.html'
    context_object_name = 'comment_list'
    def get_queryset(self):
        return Comment.objects.all()

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def publish(request):
    comment = Comment(title='', comment_text='')

    try:
        comment.title = request.POST.get('title', 'nothing')
        comment.comment_text = request.POST.get('comment_text', 'nothing')
    except comment.DoesNotExist:
        return render(request, 'polls/comments.html', (
            'error_message',
        ))
    else:
        comment.save()
        return HttpResponseRedirect(reverse('polls:comment-list'))