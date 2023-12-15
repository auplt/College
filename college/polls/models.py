from django.db import models



class Students(models.Model):
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
    student = models.ForeignKey(Students, on_delete=models.PROTECT)

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
    student = models.ForeignKey(Students, on_delete=models.PROTECT)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)

class Curriculum_lesson(models.Model):
    lesson_type = models.PositiveSmallIntegerField()
    curriculum = models.ForeignKey(Curriculum, on_delete=models.PROTECT)
    tutor = models.ForeignKey(Tutors, on_delete=models.PROTECT)


