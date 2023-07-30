from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
# FOR FLAW 2: from django.db import connection

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

#Flaw 2: Insecure Direct Object References (IDOR)
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    #Flaw 2 fix:
    #def test_func(self):
        # Check if the user has permission to view the question
        #return self.request.user.is_authenticated

    #def handle_no_permission(self):
        # Redirect to a custom error page or display a custom message
        #return render(self.request, 'polls/no_permission.html')

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#Flaw 5: SQL Injection
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
    
#Flaw 5 fix:
#def vote(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    #try:
        #choice_id = request.POST.get('choice')
        #with connection.cursor() as cursor:
            # Use parameterized query to prevent SQL injection
            #cursor.execute("UPDATE polls_choice SET votes = votes + 1 WHERE id = %s", [choice_id])
    #except (KeyError, Choice.DoesNotExist):
        #return render(request, 'polls/detail.html', {
            #'question': question,
            #'error_message': "You didn't select a choice.",
        #})
    #else:
        #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))"""
