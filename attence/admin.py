from django.contrib import admin
from .models import (StudentMessage, TeacherMessage, Course, CollegeMessage, CourseMessage, ClassroomMessage, ClassMessage, Schedule, Attence)
from . import face
import time


class StudentMessageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):

        name = str(obj.faceImage)
        obj.faceImage.name = obj.name + obj.studentId + name[name.find('.'):]
        super().save_model(request, obj, form, change=True)
        time.sleep(0.5)
        path = 'E:/python/web/FaceImage/' + obj.faceImage.name
        obj.faceId = face.Detect(path)
        face.AddFace('Student', obj.faceId)
        super().save_model(request, obj, form, change=True)


# Register your models here.
admin.site.register(TeacherMessage)
admin.site.register(StudentMessage, StudentMessageAdmin)
admin.site.register(Course)
admin.site.register(CollegeMessage)
admin.site.register(CourseMessage)
admin.site.register(ClassroomMessage)
admin.site.register(ClassMessage)
admin.site.register(Schedule)
admin.site.register(Attence)
admin.AdminSite.site_header = "考勤系统管理员"
