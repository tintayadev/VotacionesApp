import datetime
from django.http import response

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question
class QuestionModelTests(TestCase): 

    def test_was_published_recently_with_future_questions(self): 
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than one day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
        """was_published_recently() must return True for questions whose pub_date is actual"""
        time = timezone.now()
        present_question = Question(question_text="¿Quien es el mejor Course Direct de Platzi?",pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)



def create_question(question_text, days): 
    """
    Create a question with the given 'question_text' and published the given number
    of 'days' offset to now (negative for questions published in the past, positive
    for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self): 
        """If no question exist, an appropiate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # def test_past_question(self):
    #     """Questions with a pub_date in the past are displayed on the index page."""
    #     question = create_question(question_text="Past question.", days=-30)
    #     response = self.client.get(reverse('polls:index'))
    #     self.assertQuerysetEqual(
    #         response.context['latest_question_list'],
    #         [question],
    #     )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the
        index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # def test_future_question_and_past_question(self):
    #     """
    #     Even if both past and future question exist, only past question are displayed
    #     """
    #     past_question = create_question(question_text="Past question", days=-30)
    #     future_question = create_question(question_text="Future question", days=30)
    #     response = self.client.get(reverse("polls:index"))
    #     self.assertQuerysetEqual(
    #         response.context["latest_question_list"],
    #         [past_question]
    #     )


    # def test_two_past_questions(self):
    #     """The questions index page may display multiple question."""
    #     past_question1 = create_question(question_text="Past question 1", days=-30)
    #     past_question2 = create_question(question_text="Past question 2", days=-40)
    #     response = self.client.get(reverse("polls:index"))
    #     self.assertQuerysetEqual(
    #         response.context["latest_question_list"],
    #         [past_question1, past_question2]
    #     )

    def test_two_future_questions(self):
        """The questions index page may display multiple question."""
        future_question1 = create_question(question_text="Future question 1", days=30)
        future_question2 = create_question(question_text="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )

# class QuestionDetailViewTest(TestCase):
    
#     def test_future_question(self):
#         """
#         The detail view of a question with a pub_date in the future
#         returns a 404 error not found
#         """
#         future_question = create_question(question_text="Future question", days=30)
#         url = reverse("polls:detail", args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)


#     def test_past_question(self):
#         """
#         The detail view of a question with a pub_date in the past
#         displays the question's text
#         """
#         past_question = create_question(question_text="Past question", days=-30)
#         url = reverse("polls:detail", args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The deatil view of a question with a pub_date in the future
        reutrns a 404 error not found.
        """
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ResultViewtest(TestCase):

    def test_with_past_question(self):
        """
        The result view in the past display the question's text
        """
        past_question = create_question("past quesiton", days=-15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_with_future_question(self):
        """
        Question with a future date aren't displayed and this return a 404 error(not found)
        until the date is the specified date
        """
        future_question = create_question("this is a future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

def create_choice(pk, choice_text, votes=0):
    """
    Create a choice that have the pk(primary key is a number) of a specific question
    with the given "choice_text" and with the given "votes"(votes start in zero)
    """
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text, votes=votes)



def test_question_without_choices(self):
    """
    Questions have no choices aren't displayed in the index view
    """
    question = create_question("Cual es tu curso favorito?", days=-19)
    url = reverse("polls:index")
    response = self.client.get(url)
    self.assertQuerysetEqual(response.context["latest_question_list", []])
    def test_question_with_choices(self):
        """
        Question with choices are displayed in the index view
        """
        question = create_question("Cuál es tu curso favorito?", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="Curso Básico de Django", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Curso de Introducción a la Nube con Azure", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
