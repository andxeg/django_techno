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
        'max': 10
    },
    'posts_per_category': {
        'min': 100,
        'max': 200
    },


    'polls_count': 100000,
    'choices_per_poll': {
        'min': 5,
        'max': 10
    },
    'answers_per_choice': {
        'min': 5,
        'max': 10
    },
    'comments_per_poll': {
        'min': 5,
        'max': 10
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
        #first_name, last_name = names.get_full_name().split(' ')
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

        add_info = "Additional info for user %s" % first_name + ' ' + last_name
        custom_user = CustomUser(user=user, about=add_info)
        users.append(user)
        custom_users.append(custom_user)

    with transaction.atomic():
        for user in users:
            user.save()

    # with transaction.atomic():
    #     print("Before bulk_create users")
    #     User.objects.bulk_create(users)
    
    # sys.exit()

    # after bulk_create i cannot know id, because query incomplete
    # first method -> use not AutoIncrement Id, set it manually
    # second method -> use transaction and save in the loop <- bad way

    # SET ID OF CONNECTED OBJECT
    for custom_user in custom_users:
        # print("User -> %s with id -> %d"
        #        % (custom_user.user.username, custom_user.user.id))
        custom_user.user_id = custom_user.user.id

    # print("Before bulk_create custom_users")
    CustomUser.objects.bulk_create(custom_users)

    return users


def generate_categories():
    categories = []
    for i in range(CONSTANTS['categories_count']):
        headline = "Category #%d" % i
        category = Category(headline=headline)
        categories.append(category)

    # Category.objects.bulk_create(categories)

    with transaction.atomic():
        for category in categories:
            category.save()

    return categories


def generate_posts(users):
    last_user_index = len(users) - 1
    posts = []
    for i in range(CONSTANTS['posts_count']):
        user = users[randint(0, last_user_index)]
        title = "Post #%d" % i
        text = "Text of the %d-th post" % i
        created_date = timezone.now()
        post = Post(author=user,
                    title=title,
                    text=text,
                    created_date=created_date)
        posts.append(post)

    # Post.objects.bulk_create(posts)

    with transaction.atomic():
        for post in posts:
            post.save()

    return posts


def generate_comments(users, objects, obj_type):
    comments = []
    last_user_index = len(users) - 1
    if obj_type == "post":
        key = 'comments_per_post'
        content_type = ContentType.objects.get_for_model(Post)
    elif obj_type == "poll":
        key = 'comments_per_poll'
        content_type = ContentType.objects.get_for_model(Poll)

    for obj in objects:
        comments_per_obj = randint(CONSTANTS[key]['min'],
                                   CONSTANTS[key]['max'])
        content_object = obj
        object_id = obj.id
        for j in range(comments_per_obj):
            user = users[randint(0, last_user_index)]
            if obj_type == "post":
                title = "Comment #%d for post %s" % (j, obj.title,)
                body = "Body of %d-th comment of post %s" % (j, obj.title,)
            elif obj_type == "poll":
                title = "Comment #%d for poll %s" % (j, obj.question,)
                body = "Body of %d-th comment of poll %s" % (j, obj.question,)

            created_date = timezone.now()
            comment = Comment(author=user,
                              title=title,
                              body=body,
                              created_date=created_date,
                              content_type=content_type,
                              content_object=content_object,
                              object_id=object_id)

            comments.append(comment)

    Comment.objects.bulk_create(comments)
    return comments


def generate_m2m_links(categories, posts):
    posts_count = len(posts)
    curr_pos = 0
    for category in categories:
        size = randint(CONSTANTS['posts_per_category']['min'],
                       CONSTANTS['posts_per_category']['max'])

        category_id = category.id

        delta = 0
        next_pos = curr_pos + size
        if next_pos >= posts_count:
            delta = next_pos - posts_count

        for j in range(curr_pos, curr_pos+size):
            posts[j].categories.add(category_id)

        for j in range(delta):
            posts[j].categories.add(category_id)

        curr_pos = next_pos % posts_count


def generate_polls_and_choices(users):
    last_user_index = len(users) - 1
    polls = []
    choices = []
    for i in range(CONSTANTS['polls_count']):
        user = users[randint(0, last_user_index)]
        question = "Question #%d" % i
        pub_date = timezone.now()
        poll = Poll(author=user,
                    question=question,
                    pub_date=pub_date)
        polls.append(poll)

        choices_per_poll = randint(CONSTANTS['choices_per_poll']['min'],
                                   CONSTANTS['choices_per_poll']['max'])
        for j in range(choices_per_poll):
            choice_text = "Choice #%d for question#%d" % (j, i,)
            choice = Choice(poll=poll,
                            choice_text=choice_text)
            choices.append(choice)

    # problem with bulk_create i describe in func generate_users()
    # Poll.objects.bulk_create(polls)

    with transaction.atomic():
        for poll in polls:
            poll.save()


    #Choice.objects.bulk_create(choices)

    with transaction.atomic():
        for choice in choices:
            choice.poll_id = choice.poll.id
            choice.save()

    return polls, choices


def generate_answers(users, choices):
    answers = []
    last_user_index = len(users) - 1
    for choice in choices:
        answers_per_choice = randint(CONSTANTS['answers_per_choice']['min'],
                                     CONSTANTS['answers_per_choice']['max'])
        for j in range(answers_per_choice):
            user = users[randint(0, last_user_index)]
            answer = Answer(choice=choice,
                            author=user)
            answers.append(answer)

    Answer.objects.bulk_create(answers)


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
    users = generate_users()
    print("\nUsers were created")
    print_time_stamp(time.time(), t1)

    # GENERATE CATEGORIES
    categories = generate_categories()
    print("\nCategories were created")
    print_time_stamp(time.time(), t1)

    # GENERATE POSTS
    posts = generate_posts(users)
    print("\nPosts were created")
    print_time_stamp(time.time(), t1)

    # GENERATE COMMENTS TO POSTS
    comments_posts = generate_comments(users, posts, "post")
    print("\nComments to posts were created")
    print_time_stamp(time.time(), t1)

    # GENERATE MANY_TO_MANY LINKS BETWEEN POSTS AND CATEGORIES
    generate_m2m_links(categories, posts)
    print("\nMany to many links beetween posts and categories were created")
    print_time_stamp(time.time(), t1)

    # GENERATE POLLS AND CHOICES
    polls, choices = generate_polls_and_choices(users)
    print("\nPolls and choices were created")
    print_time_stamp(time.time(), t1)

    # GENERATE ANSWERS
    generate_answers(users, choices)
    print("\nAnswer to choices were created")
    print_time_stamp(time.time(), t1)

    # GENERATE COMMENTS TO POLLS
    comments_polls = generate_comments(users, polls, "poll")
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

