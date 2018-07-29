from django.shortcuts import HttpResponse
from django.views.decorators.http import *
from django.http import JsonResponse
from . import models
import json
import datetime
from . import face


# Create your views here.


@require_http_methods(['POST'])
def Login(request):
    response = {}
    req = json.loads(request.body)
    if req['user'] == 'student':
        response = StudentIndex(req)
    elif req['user'] == 'teacher':
        response = TeacherIndex(req)
    elif req['user'] == 'classroom':
        print("classroom")
        response = ClassroomIndex(req)
    print(response)
    return JsonResponse(response)


def StudentIndex(req):
    print(req)
    stu = models.StudentMessage.objects.filter(studentId=req['id'])
    if stu.exists():
        if stu.get().studentPwd == req['pwd']:
            name = stu.get().name
            age = datetime.datetime.now().year - stu.get().birthday.year
            classMessage = stu.get().classMessage
            schedules = models.Schedule.objects.filter(classMessage=classMessage)
            courses = [schedule.course for schedule in schedules]
            coursesData = [CourseData(data) for data in courses]
            attence = models.Attence.objects.filter(student=stu.get(), attenceTime__gte=datetime.date.today())
            allatence = models.Attence.objects.filter(student=stu.get()).count()
            todayattence = attence.filter(attenceTime__lte=datetime.datetime.now()).count()

            response = {
                'msg': 'Success',
                'error_num': 0,
                'id': stu.get().studentId,
                'name': name,
                'age': age,
                'classMessage': classMessage.name,
                'courses': coursesData,
                'todayattence': todayattence,
                'allatence': allatence,
                'user': req['user']
            }
        else:
            response = {'msg': 'PasswordError', 'error_num': 800}
    else:
        response = {'msg': 'NotFindUser', 'error_num': 801}
    return response


def CourseData(course):
    weekDay = course.classDay
    classOrder = course.classOrder
    name = course.course.name
    classroom = course.classroom.name
    return {
        'weekDay': weekDay,
        'classOrder': classOrder,
        'classroom': classroom,
        'name': name,
    }


def TeacherIndex(req):
    reponse = {}
    tea = models.TeacherMessage.objects.filter(userId=req['id'])
    if tea.exists():
        if tea.get().userPwd == req['pwd']:
            name = tea.get().name
            courses = models.CourseMessage.objects.filter(teacher=tea.get())
            courseNames = [course.name for course in courses]
            courseMessage = {name : SumCoursePeople(name) for name in courseNames}
            response = {
                'msg': 'Success',
                'error_num': 0,
                'name': name,
                'id': req['id'],
                'courseMessage': courseMessage

            }
        else:
            response = {'msg': 'PasswordError', 'error_num': 800}
    else:
        response = {'msg': 'NotFindUser', 'error_num': 801}
    return response


def SumCoursePeople(name):
    Schedules = models.Schedule.objects.filter(course__course__name=name).all()
    classMsgs = list(set([x.classMessage for x in Schedules]))
    people = [models.StudentMessage.objects.filter(classMessage=classmsg).count() for classmsg in classMsgs]
    peoplesum = sum(people)
    return peoplesum

def ClassroomIndex(req):
    response = {}
    print(req)
    classroom = models.ClassroomMessage.objects.filter(userid=req['id'])
    if classroom.exists():
        if classroom.get().userPassword == req['pwd']:
            name = classroom.get().name
            response = {
                'msg': 'Success',
                'error_num': 0,
                'name': name,
                'id':req['id']
            }
        else:
            response = {'msg': 'PasswordError', 'error_num': 800}
    else:
        response = {'msg': 'NotFindUser', 'error_num': 801}
    return response


@require_http_methods(['POST'])
def AddAttence(request):
    response = {}
    req = json.loads(request.body)
    face_token = face.DetectBase(req['image_base64'])
    if len(face_token) != 0:
        classroom = models.ClassroomMessage.objects.filter(userid=req['id'])
        face_token2 = face.SeachFace('Student', face_token)
        stu = models.StudentMessage.objects.filter(faceId=face_token2)
        attencetime = datetime.datetime.now()
        attencetime = attencetime.strftime("%Y-%m-%d %H:%M:%S")
        course = models.Schedule.objects.filter(classMessage=stu.get().classMessage, course__classDay=req['weekday'], course__classOrder=req['classOrder'])
            #.filter(
            #course__classDay=req['weekday'], course__classOrder=req['classOrder'])

        models.Attence.objects.create(course=course.get().course, student=stu.get(), classRoom=classroom.get())
        print(attencetime)
        if stu.exists():
            response = {
                'msg': '打卡成功',
                'face_token': face_token2,
                'name': stu.get().name,
                'classMassage': stu.get().classMessage.name,
                'attencetime': attencetime,
                'course': str(course.get().course),
                'error_num': 200
            }
        else:
            response = {
                'msg': '没有该学生',
                'error_num': 804,
            }
    else:
        response = {'msg': '没有检测到人脸', 'error_num': 803}
    return JsonResponse(response)


@require_http_methods(['POST'])
def EditPassword(request):
    response = {}
    req = json.loads(request.body)
    if req['user'] == 'student':
        response = studentEditPwd(req)
    elif req['user'] == 'teacher':
        response = TeacherEditPwd(req)
    elif req['user'] == 'classroom':
        response = ClassroomEditPwd(req)
    print(response)
    return JsonResponse(response)


def studentEditPwd(req):
    response = {}
    stu = models.StudentMessage.objects.filter(studentId=req['id'])
    if stu.exists():
        newstu = stu.first()
        newstu.studentPwd = req['pwd']
        print(stu.get().studentPwd)
        newstu.save()
        response = {
            'msg': '修改成功'
        }
    else:
        response = {'msg': '没有该用户', 'error_num': 805}
    return response


def TeacherEditPwd(req):
    response = {}
    tea = models.TeacherMessage.objects.filter(userId=req['id'])
    if tea.exists():
        newtea = tea.first()
        newtea.userPwd = req['pwd']
        print(tea.get().studentPwd)
        newtea.save()
        response = {
            'msg': '修改成功'
        }
    else:
        response = {'msg': '没有该用户', 'error_num': 805}
    return response


def ClassroomEditPwd(req):
    response = {}
    classroom = models.ClassroomMessage.objects.filter(userid=req['id'])
    if classroom.exists():
        newclassroom = classroom.first()
        newclassroom.userPassword = req['pwd']
        print(classroom.get().studentPwd)
        newclassroom.save()
        response = {
            'msg': '修改成功'
        }
    else:
        response = {'msg': '没有该用户', 'error_num': 805}
    return response
