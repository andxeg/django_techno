import os, sys

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

# passwd = *123abcd
password = 'pbkdf2_sha256$30000$c4Ot97M8Av2t$V4o5Ih3luCfFIU9QxqNQw6XpWl7KJ6yzM/oTJ7Vxwj8='
CONSTANTS = {
    'users_count': 100000,

    'categories_count': 5000,
    'posts_count': 100000,
    'comments_per_post': {
        'min': 10,
        'max': 20
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
        'min': 50,
        'max': 500
    },
    'comments_per_poll': {
        'min': 10,
        'max': 20
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
        first_name, last_name = names.get_full_name().split(' ')
        user = User(password=password,
                    username=first_name,
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

    User.objects.bulk_create(users)
    CustomUser.objects.bulk_create(custom_users)

    return users


def generate_categories():
    categories = []
    for i in range(CONSTANTS['categories_count']):
        headline = "Category #%d" % i
        category = Category(headline=headline)
        categories.append(category)

    Category.objects.bulk_create(categories)
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

    Post.objects.bulk_create(posts)
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

    Comment.bulk_create(comments)
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
            posts[j].add(category_id)

        for j in range(delta):
            posts[j].add(category_id)

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

    Poll.objects.bulk_create(polls)
    Choice.objects.bulk_create(choices)
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


def init_db(argv):
    if argv[1] == "test":
        global CONSTANTS
        CONSTANTS = TEST_CONSTANTS

    # GENERATE USERS
    users = generate_users()

    # GENERATE CATEGORIES
    categories = generate_categories()

    # GENERATE POSTS
    posts = generate_posts(users)

    # GENERATE COMMENTS TO POSTS
    comments_posts = generate_comments(users, posts, "post")

    # GENERATE MANY_TO_MANY LINKS BETWEEN POSTS AND CATEGORIES
    generate_m2m_links(categories, posts)

    # GENERATE POLLS AND CHOICES
    polls, choices = generate_polls_and_choices(users)

    # GENERATE ANSWERS
    generate_answers(users, choices)

    # GENERATE COMMENTS TO POLLS
    comments_polls = generate_comments(users, polls, "poll")


if __name__ == "__main__":
    init_db(sys.argv[0:])

#Можно запрашивать из базы не содержимое объектов
# а только id объектов

#bulk_create

#в цикле к БД обращаться нельзя

