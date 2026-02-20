# -*- coding: utf8 -*-


def teacher_go():
    # todo: teacher_go action
    return {
        "result": "it is teacher_go action"
    }


def student_go():
    # todo: student_go action
    return {
        "result": "it is student_go action"
    }


def student_come():
    # todo: student_come action
    return {
        "result": "it is student_come action"
    }


def main_handler(event, context):
    print(str(event))
    # `/user_type/{user_type}/action/{action}`
    user_type = ""
    action = ""
    path = event.get('path')
    print(path)
    data_list = path.split("/")
    print(data_list)
    if len(data_list) >= 5:
        user_type = data_list[2]
        action = data_list[4]
    if user_type == "teacher":
        if action == "go":
            return teacher_go()
    if user_type == "student":
        if action == "go":
            return student_go()
        if action == "come":
            return student_come()
    return "hello world"
