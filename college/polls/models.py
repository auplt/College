from django.db import models



class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()

class Groups(models.Model):
    name = models.CharField(max_length=16)

class Disciplines(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000, blank=True)

class Tutors(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()


class Group_semesters(models.Model):
    semester_num = models.PositiveSmallIntegerField()
    group = models.ForeignKey(Groups, on_delete=models.PROTECT)

class Group_members(models.Model):
    group_semesters = models.ForeignKey(Group_semesters, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)

class Curriculum(models.Model):
    duration = models.PositiveSmallIntegerField()
    discipline = models.ForeignKey(Disciplines, on_delete=models.PROTECT)
    group_semester = models.ForeignKey(Group_semesters, on_delete=models.PROTECT)

class Final_grades(models.Model):
    # semester_num = models.PositiveSmallIntegerField(blank=True)
    is_final = models.BooleanField()
    scale_5 = models.PositiveSmallIntegerField()
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    scale_word = models.CharField(max_length=128)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)

class Curriculum_lesson(models.Model):
    lesson_type = models.PositiveSmallIntegerField()
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    tutor = models.ForeignKey(Tutors, on_delete=models.PROTECT)

class LessonTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'lessons_time'

class Classroom(models.Model):
    number = models.CharField(max_length=8)

    class Meta:
        db_table = 'classrooms'

class TTLesson(models.Model):
    date = models.DateField()
    day_name = models.PositiveSmallIntegerField()
    week_type = models.PositiveSmallIntegerField()
    lessons_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT)
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT)
    curriculum_lesson_id = models.ForeignKey(Curriculum_lesson, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tt_lesson'
class Homework(models.Model):
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    hw_type = models.PositiveSmallIntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    class Meta:
        db_table = 'homeworks'

class Files(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True)
    file = models.BinaryField()
    hw_id = models.ForeignKey(Homework, on_delete=models.PROTECT)

    class Meta:
        db_table = 'files'

class StudentAttendance(models.Model):
    is_present = models.BooleanField()
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    class Meta:
        db_table = 'students_attendance'

class StudentProgress(models.Model):
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    class Meta:
        db_table = 'students_progress'

class Coefficient(models.Model):
    coef_num = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficients'

class Grades(models.Model):
    scale_5 = models.PositiveSmallIntegerField()
    scale_word = models.CharField(max_length=32)
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    coef_num = models.PositiveSmallIntegerField()
    coef_description = models.CharField(max_length=64)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT)
    progress_id = models.ForeignKey(StudentProgress, on_delete=models.PROTECT)

    class Meta:
        db_table = 'grades'
