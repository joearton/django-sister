import re


def get_first_last_name(fullname):
    fullname = fullname.split(' ')
    first_name, last_name = fullname[0], ''
    if len(fullname) > 1:
        first_name, last_name = fullname[0], " ".join(fullname[1:])
    return (first_name, last_name)


def set_first_last_name_user(user, fullname):
    first_name, last_name = get_first_last_name(fullname)
    user.first_name = first_name
    user.last_name = last_name
    return user
