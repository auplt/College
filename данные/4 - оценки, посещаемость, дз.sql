--ALTER SEQUENCE seq RESTART WITH 1;
--UPDATE table SET column_id=nextval('seq');

--delete from tt_lessons;
--
--ALTER SEQUENCE tt_lesson_tt_lesson_id_seq RESTART WITH 1;
--UPDATE tt_lessons SET tt_lesson_id=nextval('tt_lesson_tt_lesson_id_seq');


/* Посещения */

INSERT INTO students_attendances (attendance_id,is_present,student_id,tt_lesson_id) VALUES
;




/* Оценки */


INSERT INTO students_progresses (progress_id,student_id,tt_lesson_id,grade_id) VALUES
;

INSERT INTO grades (grade_id,scale_5,scale_word,scale_100,scale_letter,coef_num,coef_description,coefficient_id) VALUES
;

INSERT INTO final_grades () VALUES
;


/* Домашки */

INSERT INTO files () VALUES
;

INSERT INTO homeworks () VALUES
;

