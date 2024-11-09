--ALTER SEQUENCE seq RESTART WITH 1;
--UPDATE table SET column_id=nextval('seq');

UPDATE curriculum_lessons SET duration = 2*duration;

DELETE FROM tt_lessons WHERE date > '14.12.2024';

INSERT INTO curriculum_lessons (curriculum_lesson_id,curriculum_id,tutor_id,lesson_type,duration) VALUES
(nextval('curriculum_lessons_curriculum_lesson_id_seq'), 1, 8, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 2, 12, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 3, 10, 'CRD', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 4, 3, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 5, 11, 'CRD', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 6, 6, 'CRD', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 7, 5, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 8, 3, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 9, 6, 'CRD', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 10, 8, 'EXM', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 11, 4, 'CRD', 2)
, (nextval('curriculum_lessons_curriculum_lesson_id_seq'), 12, 9, 'CRD', 2)
;

INSERT INTO tt_lessons (tt_lesson_id,date,day_name,week_type,classroom_id,curriculum_lesson_id,lesson_time_id) VALUES
(nextval('tt_lesson_tt_lesson_id_seq'), '25.12.2024', 'WED', 'EX', 7, 29, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '23.12.2024', 'MON', 'EX', 7, 30, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 4, 31, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '27.12.2024', 'FRI', 'EX', 1, 32, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 11, 33, 4)
, (nextval('tt_lesson_tt_lesson_id_seq'), '19.12.2024', 'THU', 'CW', 5, 34, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '28.12.2024', 'SAT', 'EX', 1, 35, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '26.12.2024', 'THU', 'EX', 1, 36, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '20.12.2024', 'FRI', 'CW', 5, 37, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '23.12.2024', 'MON', 'EX', 6, 38, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 11, 39, 4)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 5, 40, 2)
, (nextval('tt_lesson_tt_lesson_id_seq'), '25.12.2024', 'WED', 'EX', 7, 29, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '23.12.2024', 'MON', 'EX', 7, 30, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 4, 31, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '27.12.2024', 'FRI', 'EX', 1, 32, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 11, 33, 5)
, (nextval('tt_lesson_tt_lesson_id_seq'), '19.12.2024', 'THU', 'CW', 5, 34, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '28.12.2024', 'SAT', 'EX', 1, 35, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '26.12.2024', 'THU', 'EX', 1, 36, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '20.12.2024', 'FRI', 'CW', 5, 37, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '23.12.2024', 'MON', 'EX', 6, 38, 6)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 11, 39, 5)
, (nextval('tt_lesson_tt_lesson_id_seq'), '17.12.2024', 'TUE', 'CW', 5, 40, 6)
;

