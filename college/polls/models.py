from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'student'


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)

    class Meta:
        db_table = 'group'


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000, blank=True)

    class Meta:
        db_table = 'discipline'


class Tutor(models.Model):
    tutor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128, blank=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'tutor'


class GroupSemester(models.Model):
    group_semester_id = models.AutoField(primary_key=True)
    semester_num = models.PositiveSmallIntegerField()
    group_id = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group_id')

    class Meta:
        db_table = 'group_semester'


class GroupMember(models.Model):
    group_member_id = models.AutoField(primary_key=True)
    group_semesters = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'group_member'


class Curriculum(models.Model):
    curriculum_id = models.AutoField(primary_key=True)
    duration = models.PositiveSmallIntegerField()
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT, db_column='discipline_id')
    group_semester_id = models.ForeignKey(GroupSemester, on_delete=models.PROTECT, db_column='group_semester_id')

    class Meta:
        db_table = 'curriculum'


class FinalGrade(models.Model):
    # semester_num = models.PositiveSmallIntegerField(blank=True)
    final_grade_id = models.AutoField(primary_key=True)
    is_final = models.BooleanField()
    scale_5 = models.PositiveSmallIntegerField()
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    scale_word = models.CharField(max_length=128)
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.PROTECT, db_column='curriculum_id')

    class Meta:
        db_table = 'finalGrade'


class CurriculumLesson(models.Model):
    PRACTICE = "PRA"
    LECTURE = "LEC"
    LABORATORY = "LAB"
    CREDIT = "CRD"
    EXAM = "EXM"
    TYPE_OF_LESSON_CHOICES = [
        (PRACTICE, "Практика"),
        (LECTURE, "Лекция"),
        (LABORATORY, "Лабораторная работа"),
        (CREDIT, "Зачет"),
        (EXAM, "Экзамен")
    ]

    curriculum_lesson_id = models.AutoField(primary_key=True)
    lesson_type = models.CharField(max_length=3,
                                   choices=TYPE_OF_LESSON_CHOICES
                                   )
    curriculum_id = models.ForeignKey(Curriculum, on_delete=models.PROTECT, db_column='curriculum_id')
    tutor_id = models.ForeignKey(Tutor, on_delete=models.PROTECT, db_column='tutor_id')

    class Meta:
        db_table = 'curriculum_lesson'


class LessonTime(models.Model):
    lesson_id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = 'lessons_time'


class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=8)

    class Meta:
        db_table = 'classroom'


class TTLesson(models.Model):
    EVEN_WEEK = "EV"
    NOT_EVEN_WEEK = "NE"
    CREDIT_WEEK = "CW"
    EXAM_WEEK = "EX"
    TYPE_OF_WEEK_CHOICES = [
        (EVEN_WEEK, "Четная неделя"),
        (NOT_EVEN_WEEK, "Нечетная неделя"),
        (CREDIT_WEEK, "Зачетная неделя"),
        (EXAM_WEEK, "Экзаменационная неделя")
    ]

    MONDAY = "MON"
    TUESDAY = "TUE"
    WEDNESDAY = "WED"
    THURSDAY = "THU"
    FRIDAY = "FRI"
    SATURDAY = "SAT"
    SUNDAY = "SUN"
    DAY_OF_WEEK_CHOICES = [
        (MONDAY, "Понедельник"),
        (TUESDAY, "Вторник"),
        (WEDNESDAY, "Среда"),
        (THURSDAY, "Четверг"),
        (FRIDAY, "Пятница"),
        (SATURDAY, "Суббота"),
        (SUNDAY, "Воскресенье")
    ]

    tt_lesson_id = models.AutoField(primary_key=True)
    date = models.DateField()
    day_name = models.CharField(max_length=3,
                                choices=DAY_OF_WEEK_CHOICES
                                )
    week_type = models.CharField(max_length=2,
                                 choices=TYPE_OF_WEEK_CHOICES
                                 )
    lessons_time_id = models.ForeignKey(LessonTime, on_delete=models.PROTECT, db_column='lessons_time_id')
    classroom_id = models.ForeignKey(Classroom, on_delete=models.PROTECT, db_column='classroom_id')
    curriculum_lesson_id = models.ForeignKey(CurriculumLesson, on_delete=models.PROTECT,
                                             db_column='curriculum_lesson_id')

    class Meta:
        db_table = 'tt_lesson'


class Homework(models.Model):
    hw_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=2048)
    day_given = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_given', db_column='day_given')
    day_due = models.ForeignKey(TTLesson, on_delete=models.PROTECT, related_name='day_due', db_column='day_due')
    hw_type = models.PositiveSmallIntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'homework'


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=2048, blank=True)
    file = models.BinaryField()
    hw_id = models.ForeignKey(Homework, on_delete=models.PROTECT, db_column='hw_id')

    class Meta:
        db_table = 'file'


class StudentAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    is_present = models.BooleanField()
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_attendance'


class StudentProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    tt_lesson_id = models.ForeignKey(TTLesson, on_delete=models.PROTECT, db_column='tt_lesson_id')
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT, db_column='student_id')

    class Meta:
        db_table = 'students_progress'


class Coefficient(models.Model):
    coefficient_id = models.AutoField(primary_key=True)
    coef_num = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=64)

    class Meta:
        db_table = 'coefficient'


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    scale_5 = models.PositiveSmallIntegerField()
    scale_word = models.CharField(max_length=32)
    scale_100 = models.PositiveSmallIntegerField()
    scale_letter = models.CharField(max_length=1)
    coef_num = models.PositiveSmallIntegerField()
    coef_description = models.CharField(max_length=64)
    coefficient_id = models.ForeignKey(Coefficient, on_delete=models.PROTECT, db_column='coefficient_id')
    progress_id = models.ForeignKey(StudentProgress, on_delete=models.PROTECT, db_column='progress_id')

    class Meta:
        db_table = 'grade'
