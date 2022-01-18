from django.contrib.auth.models import Group


def set_user_to_group(user, name):
    group = Group.objects.get(name = name)
    user.groups.add(group)
    return user




