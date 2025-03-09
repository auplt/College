-- РАСПИСАНИЕ В ДИАПАЗОНЕ ДАТ
select 
	tl.tt_lesson_id, tl.day_name, lt."name", cl.lesson_type, d."name", tc.last_name, c.group_semester_id 
from tt_lessons tl 
	inner join lessons_times lt on tl.lesson_time_id = lt.lesson_id 
	inner join curriculum_lessons cl on tl.curriculum_lesson_id = cl.curriculum_lesson_id 
	inner join curriculums c on cl.curriculum_id = c.curriculum_id 
	inner join disciplines d on c.discipline_id = d.discipline_id 
	inner join tutors t on cl.tutor_id = t.tutor_id 
	inner join user_customuser tc on t.user_id = tc.id
where date between '02.12.2024' and '13.12.2024'
order by c.group_semester_id, tl."date" ;


-- СПИСОК СТУДЕНТОВ В ГРУППЕ В АЛФАВИТНОМ ПОРЯДКЕ
select s.student_id, tc.last_name, tc.first_name, tc.second_name, gm.group_semester_id 
from user_customuser tc
	inner join students s on s.user_id = tc.id
	left join group_members gm on gm.student_id = s.student_id
where gm.group_semester_id = 3
order by gm.group_semester_id, tc.last_name, tc.first_name, tc.second_name;

-- СПИСОК РЕДМЕТОВ ГРУППЫ В АЛФАВИТНОМ ПОРЯДКЕ
select  d."name" 
from group_semesters gs 
	inner join curriculums c on c.group_semester_id = gs.group_semester_id
	inner join disciplines d on c.discipline_id = d.discipline_id 
where gs.group_semester_id = 6
order by d."name";


-- удаление любимой БДшки :((
SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity
	WHERE pg_stat_activity.datname = 'college' 
AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS college;

CREATE DATABASE college;


