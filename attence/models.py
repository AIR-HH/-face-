from django.db import models


# Create your models here.


# 学生信息
class StudentMessage(models.Model):
    name = models.CharField(max_length=20)
    birthday = models.DateField(auto_created=False)
    gender_choices = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(choices=gender_choices, default=1)
    studentId = models.CharField(unique=True, max_length=10)
    studentPwd = models.CharField(max_length=20)
    classMessage = models.ForeignKey('ClassMessage', on_delete=models.CASCADE, null=False)
    faceImage = models.ImageField('学生人脸', upload_to='uploadImages')
    faceId = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '学生'


# 老师信息
class TeacherMessage(models.Model):
    name = models.CharField(max_length=20)
    userId = models.CharField(unique=True, max_length=20, )
    userPwd = models.CharField(max_length=20)
    isAdmin = models.BooleanField(default=False)
    gender_choices = (
        (0, "男"),
        (1, "女"),
    )
    gender = models.IntegerField(choices=gender_choices, default=1)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '老师'


# 班级
class ClassMessage(models.Model):
    name = models.CharField(max_length=20)
    college = models.ForeignKey('CollegeMessage', on_delete=models.CASCADE)
    teacher = models.ForeignKey('TeacherMessage', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '班级'


# 学院
class CollegeMessage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '学院'


# 教室信息
class ClassroomMessage(models.Model):
    name = models.CharField(max_length=20, unique=True)
    userid = models.CharField(max_length=10, unique=True)
    userPassword = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '教室'


# 课程信息
class CourseMessage(models.Model):
    name = models.CharField(max_length=20)
    teacher = models.ForeignKey('TeacherMessage', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Mate:
        verbose_name = '课程信息'


class Course(models.Model):

    order_choices = (
        (1, '第一节课'), (2, '第二节课'), (3, '第三节课'), (4, '第四节课'), (5, '第五节课')
    )
    classOrder = models.IntegerField(choices=order_choices, default=1)
    weekDay = ((1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期日'))
    classDay = models.IntegerField(choices=weekDay, default=1)
    course = models.ForeignKey('CourseMessage', on_delete=models.CASCADE)
    classroom = models.ForeignKey('ClassroomMessage', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.name

    class Mate:
        verbose_name = '课程'


# 课表
class Schedule(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    classMessage = models.ForeignKey('ClassMessage', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.classMessage) + '--' + str(self.course)

    class Mate:
        verbose_name = '课表'


# 打卡时间
class Attence(models.Model):
    attenceTime = models.DateTimeField(auto_now_add=True)
    classRoom = models.ForeignKey('ClassroomMessage', on_delete=models.CASCADE)
    student = models.ForeignKey('StudentMessage', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.name + self.classRoom.name + str(self.attenceTime)

    class Mate:
        verbose_name = '打卡信息'
