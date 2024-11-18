--ALTER SEQUENCE seq RESTART WITH 1;
--UPDATE table SET column_id=nextval('seq');

DELETE FROM tt_lessons WHERE date > '14.12.2024';

UPDATE tt_lessons SET lesson_time_id = 1 WHERE tt_lesson_id IN (
select tt_lesson_id from tt_lessons tl
	inner join curriculum_lessons cl on tl.curriculum_lesson_id = cl.curriculum_lesson_id 
	inner join curriculums c on cl.curriculum_id = c.curriculum_id  
where day_name = 'MON'and c.group_semester_id = 6 and lesson_type = 'LEC' and lesson_time_id = 6
);

UPDATE curriculum_lessons cll SET duration = (
select 2*count(*) from tt_lessons tl 
	inner join curriculum_lessons cl on tl.curriculum_lesson_id = cl.curriculum_lesson_id 
where cl.curriculum_lesson_id = cll.curriculum_lesson_id 
);

INSERT INTO curriculum_lessons (curriculum_id,tutor_id,lesson_type,duration) VALUES
(1, 8, 'EXM', 4)
, (2, 12, 'EXM', 4)
, (3, 10, 'CRD', 4)
, (4, 3, 'EXM', 4)
, (5, 11, 'CRD', 4)
, (6, 6, 'CRD', 4)
, (7, 5, 'EXM', 4)
, (8, 3, 'EXM', 4)
, (9, 6, 'CRD', 4)
, (10, 8, 'EXM', 4)
, (11, 4, 'CRD', 4)
, (12, 9, 'CRD', 4)
;

INSERT INTO tt_lessons (date,day_name,week_type,classroom_id,curriculum_lesson_id,lesson_time_id) VALUES
( '25.12.2024', 'WED', 'EX', 7, 29, 2)
, ( '23.12.2024', 'MON', 'EX', 7, 30, 2)
, ( '17.12.2024', 'TUE', 'CW', 4, 31, 2)
, ( '27.12.2024', 'FRI', 'EX', 1, 32, 2)
, ( '17.12.2024', 'TUE', 'CW', 11, 33, 4)
, ( '19.12.2024', 'THU', 'CW', 5, 34, 2)
, ( '28.12.2024', 'SAT', 'EX', 1, 35, 2)
, ( '26.12.2024', 'THU', 'EX', 1, 36, 2)
, ( '20.12.2024', 'FRI', 'CW', 5, 37, 2)
, ( '23.12.2024', 'MON', 'EX', 6, 38, 2)
, ( '17.12.2024', 'TUE', 'CW', 11, 39, 4)
, ( '17.12.2024', 'TUE', 'CW', 5, 40, 2)
, ( '25.12.2024', 'WED', 'EX', 7, 29, 6)
, ( '23.12.2024', 'MON', 'EX', 7, 30, 6)
, ( '17.12.2024', 'TUE', 'CW', 4, 31, 6)
, ( '27.12.2024', 'FRI', 'EX', 1, 32, 6)
, ( '17.12.2024', 'TUE', 'CW', 11, 33, 5)
, ( '19.12.2024', 'THU', 'CW', 5, 34, 6)
, ( '28.12.2024', 'SAT', 'EX', 1, 35, 6)
, ( '26.12.2024', 'THU', 'EX', 1, 36, 6)
, ( '20.12.2024', 'FRI', 'CW', 5, 37, 6)
, ( '23.12.2024', 'MON', 'EX', 6, 38, 6)
, ( '17.12.2024', 'TUE', 'CW', 11, 39, 5)
, ( '17.12.2024', 'TUE', 'CW', 5, 40, 6)
;


