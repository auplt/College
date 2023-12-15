from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'student'


class Group(models.Model):
    name = models.CharField(max_length=16)

    class Meta:
        db_table = 'group'


class Discipline(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000, blank=True)

    class Meta:
        db_table = 'discipline'


class Tutor(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'tutor'


class GroupSemester(models.Model):
    semester_num = models.PositiveSmallIntegerField()
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    class Meta:
        db_table = 'group_semester'


class GroupMember(models.Model):
    group_semesters = models.ForeignKey(GroupSemester, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)

    class Meta:
        db_table = 'group_member'


class Curriculum(models.Model):
    duration = models.PositiveSmallIntegerField()
    discipline = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    group_semester = models.ForeignKey(GroupSemester, on_delete=models.PROTECT)

    class Meta:
        db_table = 'curriculum'


class FinalGrade(models.Model):
    # semester_num = models.PositiveSmallIntegerField(blank=True)
    is_final = models.BooleanField()
    scale_5 = models.PositiveSmallIntegerField()
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    scale_word = models.CharField(max_length=128)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)

    class Meta:
        db_table = 'finalGrade'


class CurriculumLesson(models.Model):
    lesson_type = models.PositiveSmallIntegerField()
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT)

    class Meta:
        db_table = 'curriculum_Lesson'


class LessonTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'lessons_time'


class Classroom(models.Model):
    number = models.CharField(max_length=8)

    class Meta:
        db_table = 'classroom'


class TTLesson(models.Model):
    date = models.DateField()
    day_name = models.PositiveSmallIntegerField()
    week_type = models.PositiveSmallIntegerField()
    lessons_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT)
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT)
    curriculum_lesson_id = models.ForeignKey(CurriculumLesson, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tt_lesson'


class Homework(models.Model):
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT)
    hw_type = models.PositiveSmallIntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)

    class Meta:
        db_table = 'homework'


class File(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True)
    file = models.BinaryField()
    hw_id = models.ForeignKey(Homework, on_delete=models.PROTECT)

    class Meta:
        db_table = 'file'


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
        db_table = 'coefficient'


class Grade(models.Model):
    scale_5 = models.PositiveSmallIntegerField()
    scale_word = models.CharField(max_length=32)
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    coef_num = models.PositiveSmallIntegerField()
    coef_description = models.CharField(max_length=64)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT)
    progress_id = models.ForeignKey(StudentProgress, on_delete=models.PROTECT)

    class Meta:
        db_table = 'grade'
