# College

browser
http://127.0.0.1:8000/


Django Tutorial
part 1 - https://docs.djangoproject.com/en/5.0/intro/tutorial01/
part 2 - https://docs.djangoproject.com/en/5.0/intro/tutorial02/

college\settings.py
- LANGUAGE_CODE
- TIME_ZONE


Django типы данных в Model
https://docs.djangoproject.com/en/4.2/ref/models/fields/

BD:
- тип PositiveSmallIntegerField для полей semester_num, duration
- в Final_grades изменены имена полей (нельзя имя начинать с цифры!)
- обдумать, возможно для scale_5, scale_letter и scale_word надо просто задать набор возможных значений
- тоже самое и для lesson_type в Curriculum_lesson
- для всех внешних ключей поставила on_delete=PROTECT, так как нигде не должно быть каскадного удаление, вроде бы

но внешние ключи надо проверить как работают - нужны ли они?


