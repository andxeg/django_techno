import os
import sys
import time
import math
import datetime

project_path = "/home/andrew/TECHNOSPHERE/python/env/django_project/project/"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techno.settings")
sys.path.append(project_path)
os.chdir(project_path)

import django
django.setup()

import names
from django.utils import timezone
from  random import randint

from django.contrib.auth.models import User
from blog.models import Post, Category
from polls.models import Poll, Choice, Answer
from comment.models import Comment
from custom_user.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

# passwd = *123abcd
password = 'pbkdf2_sha256$30000$c4Ot97M8Av2t$V4o5Ih3luCfFIU9QxqNQw6XpWl7KJ6yzM/oTJ7Vxwj8='
CONSTANTS = {
    'users_count': 100000,

    'categories_count': 5000,
    'posts_count': 100000,
    'comments_per_post': {
        'min': 5,
        'max': 15
    },
    'posts_per_category': {
        'min': 100,
        'max': 200
    },


    'polls_count': 100000,
    'choices_per_poll': {
        'min': 5,
        'max': 5
    },
    'answers_per_choice': {
        'min': 5,
        'max': 10
    },
    'comments_per_poll': {
        'min': 5,
        'max': 15
    },


}

TEST_CONSTANTS = {
    'users_count': 10,

    'categories_count': 5,
    'posts_count': 100,
    'comments_per_post': {
        'min': 2,
        'max': 5
    },
    'posts_per_category': {
        'min': 10,
        'max': 15
    },

    'polls_count': 100,
    'choices_per_poll': {
        'min': 2,
        'max': 5
    },
    'answers_per_choice': {
        'min': 10,
        'max': 15
    },
    'comments_per_poll': {
        'min': 2,
        'max': 5
    },

}


def generate_users():
    users = []
    custom_users = []
    for i in range(CONSTANTS['users_count']):
        # first_name, last_name = names.get_full_name().split(' ')
        first_name = "User_%d" % i
        last_name = "lastname"
        user = User(password=password,
                    username=first_name.lower() + '_' + last_name.lower(),
                    first_name=first_name,
                    last_name=last_name,
                    is_superuser=False,
                    is_staff=True,
                    is_active=True,
                    date_joined=timezone.now())

        users.append(user)

    # with transaction.atomic():
    #     for user in users:
    #         user.save()

    with transaction.atomic():
        print("Before bulk_create users")
        User.objects.bulk_create(users)
        print("After bulk_create users")
    
    # after bulk_create i cannot know id, because query incomplete
    # first method -> use not AutoIncrement Id, set it manually
    # second method -> use transaction and save in the loop <- bad way
    # third methow -> uses below

    # Due to bulk_create doesn't return objects with primary_key(briefly id)
    # Send query to db
    # users = User.objects.all()
    users_id = User.objects.values_list('id', flat=True).all()

    # SET ID OF CONNECTED OBJECT
    for user_id in users_id:
        # print("User -> %s with id -> %d"
        #        % (custom_user.user.username, custom_user.user.id))
        add_info = "Additional info for user with id %d" % user_id
        custom_user = CustomUser(user_id=user_id, about=add_info)
        custom_users.append(custom_user)
        
    print("Before bulk_create custom_users")
    CustomUser.objects.bulk_create(custom_users)
    return users_id


def generate_categories():
    categories = []
    for i in range(CONSTANTS['categories_count']):
        headline = "Category #%d" % i
        category = Category(headline=headline)
        categories.append(category)

    with transaction.atomic():
        Category.objects.bulk_create(categories)

    categories_id = Category.objects.values_list('id', flat=True).all()
    # categories = Category.objects.all()
    return categories_id


def generate_posts(users_id):
    last_user_index = len(users_id) - 1
    posts = []
    for i in range(CONSTANTS['posts_count']):
        user_id = users_id[randint(0, last_user_index)]
        title = "Post #%d" % i
        text = "Text of the %d-th post" % i
        created_date = timezone.now()
        post = Post(author_id=user_id,
                    title=title,
                    text=text,
                    created_date=created_date)
        posts.append(post)

    with transaction.atomic():
        Post.objects.bulk_create(posts, 50000)

    # may be need take only id from db
    # posts = Post.objects.all()
    posts_id = Post.objects.values_list("id", flat=True).all()
    return posts_id


def generate_comments(users_id, objects_id, obj_type):
    comments = []
    last_user_index = len(users_id) - 1
    if obj_type == "post":
        key = 'comments_per_post'
        content_type = ContentType.objects.get_for_model(Post)
        title_template = "Comment #%d for post with id %d"
        body_template = "Body of %d-th comment of post with id %d"
    elif obj_type == "poll":
        key = 'comments_per_poll'
        content_type = ContentType.objects.get_for_model(Poll)
        title_template = "Comment #%d for poll with id %d"
        body_template = "Body of %d-th comment of poll with id %d"

    for object_id in objects_id:
        comments_per_obj = randint(CONSTANTS[key]['min'],
                                   CONSTANTS[key]['max'])   
        for j in range(comments_per_obj):
            user_id = users_id[randint(0, last_user_index)]
            title = title_template % (j, object_id)
            body = body_template % (j, object_id)
            created_date = timezone.now()
            comment = Comment(author_id=user_id,
                              title=title,
                              body=body,
                              created_date=created_date,
                              content_type=content_type,
                              object_id=object_id)

            comments.append(comment)

    # слишком большие запросы - нужно обрезать в bulk_create размер
    with transaction.atomic():
        Comment.objects.bulk_create(comments, 50000)

    # comments_id = Comment.objects.values_list('id', flat=True).all()


def generate_m2m_links(categories_id, posts_id):
    posts_count = len(posts_id)
    curr_pos = 0
    m2m_links = []
    m2m_obj = Post.categories.through

    for category_id in categories_id:
        size = randint(CONSTANTS['posts_per_category']['min'],
                       CONSTANTS['posts_per_category']['max'])

        delta = 0
        next_pos = curr_pos + size
        if next_pos >= posts_count:
            delta = next_pos - posts_count

        for j in range(curr_pos, next_pos - delta):
            post_category_link = m2m_obj(post_id=posts_id[j], category_id=category_id)
            m2m_links.append(post_category_link)

        for j in range(delta):
            post_category_link = m2m_obj(post_id=posts_id[j], category_id=category_id)
            m2m_links.append(post_category_link)

        curr_pos = next_pos % posts_count

    m2m_obj.objects.bulk_create(m2m_links, 10000)


    # for category in categories:
    #     size = randint(CONSTANTS['posts_per_category']['min'],
    #                    CONSTANTS['posts_per_category']['max'])

    #     delta = 0
    #     next_pos = curr_pos + size
    #     if next_pos >= posts_count:
    #         delta = next_pos - posts_count

    #     posts = []
    #     for j in range(curr_pos, next_pos - delta):
    #         posts.append(posts_id[j])

    #     for j in range(delta):
    #         posts.append(posts_id[j])

    #     category.post_set.set(posts)
    #     # Post.category.through - m2m model

    #     curr_pos = next_pos % posts_count


def generate_polls_and_choices(users_id):
    last_user_index = len(users_id) - 1
    polls = []
    choices = []
    for i in range(CONSTANTS['polls_count']):
        user_id = users_id[randint(0, last_user_index)]
        question = "Question #%d" % i
        pub_date = timezone.now()
        poll = Poll(author_id=user_id,
                    question=question,
                    pub_date=pub_date)
        polls.append(poll)

    # problem with bulk_create i describe in func generate_users()
    
    with transaction.atomic():
        Poll.objects.bulk_create(polls, 50000)

    # polls = Poll.objects.all()
    polls_id = Poll.objects.values_list('id', flat=True).all()

    for poll_id in polls_id:
        choices_per_poll = randint(CONSTANTS['choices_per_poll']['min'],
                                   CONSTANTS['choices_per_poll']['max'])
        for j in range(choices_per_poll):
            choice_text = "Choice #%d for question with id -> %d" % (j, poll_id,)
            choice = Choice(poll_id=poll_id,
                            choice_text=choice_text)
            choices.append(choice)
    
    Choice.objects.bulk_create(choices, 50000)

    # choices = Choice.objects.all()
    choices_id = Choice.objects.values_list("id", flat=True).all()
    return polls_id, choices_id


def generate_answers(users_id, choices_id):
    answers = []
    last_user_index = len(users_id) - 1
    for choice_id in choices_id:
        answers_per_choice = randint(CONSTANTS['answers_per_choice']['min'],
                                     CONSTANTS['answers_per_choice']['max'])
        for j in range(answers_per_choice):
            user_id = users_id[randint(0, last_user_index)]
            answer = Answer(choice_id=choice_id,
                            author_id=user_id)
            answers.append(answer)

    Answer.objects.bulk_create(answers, 50000)


def print_time_stamp(t2, t1):
    curr_time = datetime.datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
    print("Current time -> %s " % curr_time)
    delta = math.floor(t2 - t1) + 1
    h = math.floor(delta / 3600)
    m = math.floor(delta - 3600*h) / 60
    s = delta % 60
    print("Delta time -> %dh %dm %ds" % (h, m, s))
    print("Delta time in seconds -> %f" % delta)


def init_db(argv):
    t1 = time.time()
    curr_time = datetime.datetime.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S')
    print("Current time -> %s " % curr_time)

    if len(argv) == 1:
        print("Try start script in this form: python %s test|create" % argv[0])
        return

    if not argv[1] == "test" and not argv[1] == "create":
        print("Try start script in this form: python %s test|create" % argv[0])
        return

    if argv[1] == "test":
        global CONSTANTS
        CONSTANTS = TEST_CONSTANTS

    # GENERATE USERS
    users_id = generate_users()
    print("\nUsers were created")
    print_time_stamp(time.time(), t1)

    # GENERATE CATEGORIES
    categories_id = generate_categories()
    print("\nCategories were created")
    print_time_stamp(time.time(), t1)

    # GENERATE POSTS
    posts_id = generate_posts(users_id)
    print("\nPosts were created")
    print_time_stamp(time.time(), t1)

    # GENERATE COMMENTS TO POSTS
    generate_comments(users_id, posts_id, "post")
    print("\nComments to posts were created")
    print_time_stamp(time.time(), t1)

    # GENERATE MANY_TO_MANY LINKS BETWEEN POSTS AND CATEGORIES
    generate_m2m_links(categories_id, posts_id)
    print("\nMany to many links beetween posts and categories were created")
    print_time_stamp(time.time(), t1)

    # GENERATE POLLS AND CHOICES
    polls_id, choices_id = generate_polls_and_choices(users_id)
    print("\nPolls and choices were created")
    print_time_stamp(time.time(), t1)

    # GENERATE ANSWERS
    generate_answers(users_id, choices_id)
    print("\nAnswers to choices were created")
    print_time_stamp(time.time(), t1)

    # GENERATE COMMENTS TO POLLS
    generate_comments(users_id, polls_id, "poll")
    print("\nComments to polls were created")

    print("All ok")
    print_time_stamp(time.time(), t1)
    return

if __name__ == "__main__":
    init_db(sys.argv[0:])

# Можно запрашивать из базы не содержимое объектов
# а только id объектов

# bulk_create

# в цикле к БД обращаться нельзя
