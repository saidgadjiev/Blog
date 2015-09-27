from optparse import make_option
from django.core.management.base import BaseCommand

from asking.models import Profile, Question, Answer
from django.contrib.auth.models import User

from faker.frandom import random
from faker.lorem import sentence, sentences, words
from mixer.fakers import get_username, get_email

from django.db.models import Min, Max

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--users',
            action='store',
            dest='users',
            default=0,
        ),
        make_option('--questions',
            action='store',
            dest='questions',
            default=0,
        ),
        make_option('--answers',
            action='store',
            dest='answers',
            default=0,
        ),
        make_option('--tags',
            action='store',
            dest='tags',
            default=0,
        ),
    )

    def handle(self, *args, **options):
        names = {}
        while(len(names.keys())<int(options['users'])):
            names[get_username(length=26)+str(random.randint(1950, 2015))]=1
        
        for name in names.keys():
            u = User.objects.create(username=name, email=get_email())
            p = Profile.objects.create(user_id=u.id, rating=random.randint(0,20))
        
        p_min = Profile.objects.all().aggregate(Min('id'))['id__min']
        p_max = Profile.objects.all().aggregate(Max('id'))['id__max']

        for i in range(0, int(options['questions'])):
            q = Question.objects.create(author_id=random.randint(p_min, p_max),
                title=(sentence())[0:59], text=sentences(3))

        q_min = Question.objects.all().aggregate(Min('id'))['id__min']
        q_max = Question.objects.all().aggregate(Max('id'))['id__max']

        for i in range(0, int(options['answers'])):
            a = Answer.objects.create(author_id=random.randint(p_min, p_max),
                question_id=random.randint(q_min, q_max), text=sentences(4))
