--ALTER SEQUENCE seq RESTART WITH 1;
--UPDATE table SET column_id=nextval('seq');


/* Словари */

INSERT INTO classrooms (classroom_id,number,description) VALUES
(nextval('classroom_classroom_id_seq'), 'А-100', 'Лекционная аудитория')
, (nextval('classroom_classroom_id_seq'), 'А-305', 'Аудитория для лабораторных работ по физике')
, (nextval('classroom_classroom_id_seq'), 'А-306', 'Аудитория для лабораторных работ по физике')
, (nextval('classroom_classroom_id_seq'), 'К-207', 'Аудитория')
, (nextval('classroom_classroom_id_seq'), 'К-208', 'Аудитория')
, (nextval('classroom_classroom_id_seq'), 'В-209', 'Компьютерная аудитория')
, (nextval('classroom_classroom_id_seq'), 'К-710', 'Компьютерная аудитория')
, (nextval('classroom_classroom_id_seq'), 'Г-410', 'Лекционная аудитория')
, (nextval('classroom_classroom_id_seq'), 'Г-411', 'Лекционная аудитория')
, (nextval('classroom_classroom_id_seq'), 'А-303', 'Лекционная аудитория')
, (nextval('classroom_classroom_id_seq'), 'СК', 'Спортивный комплекс')
;

INSERT INTO coefficients (coefficient_id,coef_num,description) VALUES
(nextval('coefficient_coefficient_id_seq'), 1, 'default')
, (nextval('coefficient_coefficient_id_seq'), 3, 'Контрольная работа')
, (nextval('coefficient_coefficient_id_seq'), 2, 'Самостаятельная работа')
, (nextval('coefficient_coefficient_id_seq'), 1, 'Домашнее задание')
, (nextval('coefficient_coefficient_id_seq'), 1, 'Работа на семинаре')
, (nextval('coefficient_coefficient_id_seq'), 1, 'Выступление с докладом')
, (nextval('coefficient_coefficient_id_seq'), 5, 'Экзамен')
, (nextval('coefficient_coefficient_id_seq'), 5, 'Зачёт')
, (nextval('coefficient_coefficient_id_seq'), 3, 'Коллоквиум')
, (nextval('coefficient_coefficient_id_seq'), 2, 'Сдача нормативов')
;

INSERT INTO disciplines (discipline_id,"name",description) VALUES
(nextval('disciplines_discipline_id_seq'), 'Физика', null)
, (nextval('disciplines_discipline_id_seq'), 'Философия', null)
, (nextval('disciplines_discipline_id_seq'), 'Мат. анализ', 'Высшая математика - Матемаический анализ')
, (nextval('disciplines_discipline_id_seq'), 'Лин. алгебра', 'Высшая математика - Линейная алгебра')
, (nextval('disciplines_discipline_id_seq'), 'Диффуры', 'Высшая математика - Дифференциальные уравнения')
, (nextval('disciplines_discipline_id_seq'), 'ЭБ', 'Экономическая безопасность')
, (nextval('disciplines_discipline_id_seq'), 'Налоги', 'Налогооблажение в Российской Федерации')
, (nextval('disciplines_discipline_id_seq'), 'ООП', 'Объектно-Ориентированное Программирование')
, (nextval('disciplines_discipline_id_seq'), 'ЯП', 'Языки Программирования')
, (nextval('disciplines_discipline_id_seq'), 'БОС', 'Безопасность Операционных Систем')
, (nextval('disciplines_discipline_id_seq'), 'Физкультура', null)
;

INSERT INTO groups (group_id,name) VALUES
(nextval('groups_group_id_seq'), 'П23-100')
, (nextval('groups_group_id_seq'), 'Ф23-101')
, (nextval('groups_group_id_seq'), 'Э23-102')
, (nextval('groups_group_id_seq'), 'П24-100')
, (nextval('groups_group_id_seq'), 'Ф24-101')
;

INSERT INTO lessons_times (lesson_id,start_time,end_time,"name") VALUES
	 (nextval('lessons_time_lesson_id_seq'),'08:30:00','10:05:00','1 пара'),
	 (nextval('lessons_time_lesson_id_seq'),'10:15:00','11:50:00','2 пара'),
	 (nextval('lessons_time_lesson_id_seq'),'12:45:00','14:20:00','3 пара'),
	 (nextval('lessons_time_lesson_id_seq'),'14:30:00','16:05:00','4 пара'),
	 (nextval('lessons_time_lesson_id_seq'),'16:15:00','17:50:00','5 пара'),
	 (nextval('lessons_time_lesson_id_seq'),'12:00:00','13:35:00','3 пара v2'),
	 (nextval('lessons_time_lesson_id_seq'),'18:00:00','19:35:00','6 пара')
;


/* Пользователи */

INSERT INTO timetable_customuser (id,"password",last_login,is_superuser,username,email,is_staff,is_active,date_joined,first_name,last_name,second_name) VALUES
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$hmzFBl57irmmVFXyE3Phfy$A8GNP9ipSXUB78ECm/vQIF3jvf0ZDnyse9ah3x8ev2U=','2024-11-04 14:05:55.774609+03',true,'admin','admin@admin.admin',true,true,'2024-11-04 02:39:39.019125+03','','',NULL),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$mc9yLouQxtODFijED1sSNN$uqpT53Gbu8JuoNLr5QCl2iHTpKacBqi8rxvd5UYhjek=',NULL,false,'amd001','andreykomd@mail.ru',false,true,'2024-11-04 15:17:28.128969+03','Максим','Андрейко','Дмитриевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$tmajfE2GrGMd2WomXYE8az$uJE10BVts57amV8BXMrFg7ux7ziRNGIjU7bwFMV/Des=',NULL,false,'aaa001','afanasevaaa@mail.ru',false,true,'2024-11-04 15:46:50.78656+03','Алина','Афанасьева','Александровна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$qD7t1yHqbkYWWNxHG7aPhv$eDZOTXANpV0aznazSYHmAvdELyhXMAdREATBTRWRV7Y=',NULL,false,'bai001','belyaevai@mail.ru',false,true,'2024-11-04 15:47:48.226553+03','Алексей','Беляев','Игоревич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$NwyzOdpCGRycKCgeHjH9ht$/pvDnsz9kaVF5FllSV4SmupKzs10Mo3kaKTal/VkEc4=',NULL,false,'zea001','zhukovea@mail.ru',false,true,'2024-11-04 15:49:42.915009+03','Егор','Жуков','Александрович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$bu03ce9e5oQyBsVafz1NUm$GlDz5/VfyBkKN+nIY3kpV+8VTKq22aIq9TZGSQZAVXE=',NULL,false,'zia001','zlatovratskiyia@mail.ru',false,true,'2024-11-04 15:50:51.107522+03','Иван','Златовратский','Алексеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$7ac9O83fOF9iYdlF0YIkil$SJEQLruyMvgO8QNUvD47o7K5TCzP+mydjNrGQfT6epQ=',NULL,false,'lto001','lobastovato@mail.ru',false,true,'2024-11-04 15:59:55.333086+03','Татьяна','Лобастова','Олеговна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$5Jda7PQHSXviuH49DliNax$Mf1ZL5GBKVv6J+adUqaJW4CO5ZqpBT8MR8qaZuuiVfw=',NULL,false,'msm001','melnikovsm@mail.ru',false,true,'2024-11-04 16:04:14.626375+03','Савелий','Мельников','Михайлович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$yev3eiarF6rmARmY27hzq8$Y/GuALHMPhORYMiZbX21yzkqvhxFxhz7GazPvmnii6s=',NULL,false,'pns001','prischepenkons@mail.ru',false,true,'2024-11-04 16:05:00.439863+03','Никита','Прищепенко','Сергеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$R17AwStvzHKUtYw7nvYzUJ$ldPfh15xfp7qXP4GiyTyx4JZrLk5hPTtBq4ptChhSo4=',NULL,false,'rvp001','romanovvp@mail.ru',false,true,'2024-11-04 16:06:07.401071+03','Владислав','Романов','Павлович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$z94mncp2ZkUFvK8NyIWDHa$VaWRv+yYACDF2krizAER82fd9GNbkGgCIcslVXzjD94=',NULL,false,'sad001','suxorukixad@mail.ru',false,true,'2024-11-04 16:07:34.246642+03','Анастасия','Сухоруких','Дмитриевна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$m10NdDrcR0jqCxGauTHbIF$32Ypn7oWT20F8K6em80dzREcPJm3mdtvcT6SoZ9B0Hg=',NULL,false,'fms001','fokinams@mail.ru',false,true,'2024-11-04 16:08:26.075174+03','Мария','Фокина','Сергеевна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$F65raGW8uoXS3IP6xEbU4f$pIneSGlQyXcttuD0n515eoIuWpOGZG/hoYSClmlKr7Y=',NULL,false,'cia001','chaltsevia@mail.ru',false,true,'2024-11-04 16:09:39.802677+03','Илья','Чальцев','Антонович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$kWRhiMWwLAAgZB5clkmFYV$XOjIf5T3fR7bxLPrbNuJwJo//cw4cvqe6FIiGPUOIDM=',NULL,false,'aki001','abramov@mail.ru',false,true,'2024-11-04 16:58:24.191414+03','Кирилл','Абрамов','Игоревич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$IkahT13x6JXXeX6MpUwIf1$KazMl7UN6/5O+GnxWHci6ZW1G+q7NCwqpCascib91lg=',NULL,false,'baa001','bakanov@mail.ru',false,true,'2024-11-04 17:59:32.066585+03','Артем','Баканов','Александрович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$OsBnwpEFG43TGP9ISOpCiF$7+tXS725P2OcpnrXZzpDugQWoILzrNCfQedINtLYVMA=',NULL,false,'bya001','baryshnikova@mail.ru',false,true,'2024-11-04 18:03:29.024189+03','Юлия','Барышникова','Алексеевна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$rS5nNjXPXcmdrYci8ZIwNh$srVoHVHbRH+5dmHx11bM+cmmaQ7vGtvis1NS37tcDCQ=',NULL,false,'vvo001','vatulin@mail.ru',false,true,'2024-11-04 18:04:56.496215+03','Валентин','Ватулин','Олегович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$AcZXhgd3XH6plRFPExALGV$J3WmstlgYWZ7ersF3qMhZ4YEmJyOG25VPakKEfdPaxY=',NULL,false,'vvm001','volodin@mail.ru',false,true,'2024-11-04 18:10:54.602484+03','Владислав','Володин','Михайлович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$yL7Kc1xNtBOJXz7tlyfvth$IWpe5cPr8iJHPDNWFsuJ3JpLTWK+9JZpHi7/VCfP714=',NULL,false,'das001','degtyarev@mail.ru',false,true,'2024-11-04 18:11:47.082811+03','Александр','Дегтярев','Сергеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$XTeAJF1AtjBDReEg0Ia458$0EUOu/I/2djeDdrqZH3eROHd5qQd8uIO0WRxgkUgVu4=',NULL,false,'zap001','zaborovskaya@mail.ru',false,true,'2024-11-04 18:12:48.950934+03','Анна','Заборовская','Павловна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$ayty8dhyoyACtFj2XXgErU$dHVO84wNtN/GTwsxn/0HfC1zvt4F388tVKYVwa7Xt94=',NULL,false,'ias001','inashevskiy@mail.ru',false,true,'2024-11-04 18:14:09.416716+03','Александр','Инашевский','Сергеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$NuAXuvWb0JThI9bBrfo0GZ$tIMMjTzh2ZAyx8LHwaMviMq4w2wRDf0or39oOJ41Q24=',NULL,false,'iea001','ionova@mail.ru',false,true,'2024-11-04 18:17:17.626588+03','Екатерина','Ионова','Олеговна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$XgvY2eizF5u5fxrFf9pWzX$iwTDwdediPaZUxvvDNLRs1yhCIyZnYhAQQduycbnMPs=',NULL,false,'ldd001','labzunova@mail.ru',false,true,'2024-11-04 18:18:05.928322+03','Дарья','Лабзунова','Дмитриевна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$taHqSAsTbHSKNJGP9s8wDB$w9D8OGHhol7Mk6IJTKT8nn4NPhTGO/c8oEKkrBB8GjI=',NULL,false,'mor001','malyshev@mail.ru',false,true,'2024-11-04 18:18:57.922945+03','Олег','Малышев','Романович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$VDxDWD1is1ctbZ11MBxOp3$3RzR/FyINcf3dTnsE33VdJmQL6YDwZoinW4VZqrcthQ=',NULL,false,'mvs001','masliy@mail.ru',false,true,'2024-11-04 18:19:47.886865+03','Владислав','Маслий','Сергеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$icRCpZWktMSn2k1Duc6EJv$xGFzuS5VBDbwHYnJxEGrbzwdNGTAv4z7l+D1vsnx1Jk=',NULL,false,'mia001','milovidov@mail.ru',false,true,'2024-11-04 18:20:23.39538+03','Иван','Миловидов','Антонович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$lPobIfAv5nDhl5OtO0sksU$rz1cDou6NwLo2w9pEgqR5IxvMo+DNArfiS1eALrgOWk=',NULL,false,'mge001','mironov@mail.ru',false,true,'2024-11-04 18:21:01.524434+03','Григорий','Миронов','Евгеньевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$Tx539BYOM7oDRSiUClcWrO$D7U7TySEhEXkTrS2u1rdz9aScS8qhNwWRQndSjd/NKQ=',NULL,false,'mma001','mitsevich@mail.ru',false,true,'2024-11-04 18:21:31.198617+03','Максим','Мицевич','Александрович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$7TwnRb1Nms7zxzYQTyvLXl$e3L4/MxyIM4kTbjMxzOqacbDL4TmZ1nHQ5kPQvIe+lk=',NULL,false,'ndi001','nedoluzhko@mail.ru',false,true,'2024-11-04 18:22:18.165237+03','Денис','Недолужко','Игоревич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$uunPOel1yoKTxSX3QTslrG$xxtzGTuTDiU7YGH0fa3JVZERGOPiwxRPP6sUaJEmI7I=',NULL,false,'sda001','sergeeva@mail.ru',false,true,'2024-11-04 18:22:52.498396+03','Диана','Сергеева','Алексеевна'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$2EGVJGW7mBFlgmVaOzuNcL$eYjYLBQFZw3iSdEqChjfVP7qOBGgVHHiaueFri4lkRM=',NULL,false,'sma001','sorokin@mail.ru',false,true,'2024-11-04 18:23:20.449557+03','Михаил','Сорокин','Андреевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$UDsMgfEQJzxHdviz3niyzb$VaPJrM/iQlm0FIyAFcfCv+8CRwgv2mMq0vqRqdKGduI=',NULL,false,'fda001','fomenko@mail.ru',false,true,'2024-11-04 18:24:23.949713+03','Данил','Фоменко','Александрович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$9yQdVtUoNvNDRIGL9Yxjlv$NSejA2KvCqMXfgvaUHHu/n95DfHGgK+m5lE3sbXsXfs=',NULL,false,'fra001','fomichev@mail.ru',false,true,'2024-11-04 18:25:03.167439+03','Роман','Фомичев','Александрович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$rMpRg4qPpugWMvzBpCAspE$ZgQRgEQ1G4eARd6R4mniDkfL0Fa7YzgbbgQUWDXy9kA=',NULL,false,'fia001','frolov@mail.ru',false,true,'2024-11-04 18:25:59.079535+03','Иван','Фролов','Алексеевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$NZXiK81BzgwbO2xpUqnj01$lPbqFEl6iMaz+jnITLZ74dp25HuySYJmyBZgSwP0g3c=',NULL,false,'xdn001','xarke@mail.ru',false,true,'2024-11-04 18:26:49.423257+03','Денис','Харке','Николаевич'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$wsD96CgtaHVVBGvNJNvzi9$nKYIKXh/LBVk4r2QuRqvtDuMHgBajWnL0srzjlcvhzI=',NULL,false,'sto001','shabrov@mai.ru',false,true,'2024-11-04 18:27:32.658921+03','Тимофей','Шабров','Олегович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$uYsjUKBwOF3rutJEZ0G6E5$VWZiS7L0DB1eIjtdz4G9QE7XPblZSCNZitu//kgzrXw=',NULL,true,'dap','dolgovap@mail.ru',false,true,'2024-11-05 23:48:31.323','Александр','Долгов','Павлович'),
	 (nextval('timetable_customuser_id_seq'),'pbkdf2_sha256$720000$uYsjUKBwOF3rutJEZ0G6E5$VWZiS7L0DB1eIjtdz4G9QE7XPblZSCNZitu//kgzrXw=',NULL,true,'mia','mashkovaia@mail.ru',false,true,'2024-11-05 23:48:31.323','Ирина','Машкова','Алексеевна')
;

INSERT INTO tutors (tutor_id,date_of_birth,user_id) VALUES
(nextval('tutors_tutor_id_seq'), '1995-08-13', 2)
, (nextval('tutors_tutor_id_seq'), '1989-04-17', 3)
, (nextval('tutors_tutor_id_seq'), '1989-01-31', 4)
, (nextval('tutors_tutor_id_seq'), '1985-11-06', 5)
, (nextval('tutors_tutor_id_seq'), '1987-04-17', 6)
, (nextval('tutors_tutor_id_seq'), '1991-07-01', 7)
, (nextval('tutors_tutor_id_seq'), '1994-12-24', 8)
, (nextval('tutors_tutor_id_seq'), '1987-07-07', 9)
, (nextval('tutors_tutor_id_seq'), '1986-05-30', 10)
, (nextval('tutors_tutor_id_seq'), '1992-02-01', 11)
, (nextval('tutors_tutor_id_seq'), '1988-07-29', 12)
, (nextval('tutors_tutor_id_seq'), '1994-06-25', 13)
;

INSERT INTO students (student_id,date_of_birth,user_id) VALUES
(nextval('students_student_id_seq'), '2001-07-14', 14)
, (nextval('students_student_id_seq'), '2001-10-11', 15)
, (nextval('students_student_id_seq'), '2001-01-19', 16)
, (nextval('students_student_id_seq'), '2002-03-25', 17)
, (nextval('students_student_id_seq'), '2001-09-12', 18)
, (nextval('students_student_id_seq'), '2002-02-18', 19)
, (nextval('students_student_id_seq'), '2001-02-28', 20)
, (nextval('students_student_id_seq'), '2002-08-15', 21)
, (nextval('students_student_id_seq'), '2001-02-26', 22)
, (nextval('students_student_id_seq'), '2001-05-17', 23)
, (nextval('students_student_id_seq'), '2002-06-23', 24)
, (nextval('students_student_id_seq'), '2001-07-27', 25)
, (nextval('students_student_id_seq'), '2002-03-11', 26)
, (nextval('students_student_id_seq'), '2001-09-09', 27)
, (nextval('students_student_id_seq'), '2001-10-03', 28)
, (nextval('students_student_id_seq'), '2002-07-06', 29)
, (nextval('students_student_id_seq'), '2002-09-01', 30)
, (nextval('students_student_id_seq'), '2001-12-04', 31)
, (nextval('students_student_id_seq'), '2001-11-07', 32)
, (nextval('students_student_id_seq'), '2001-12-19', 33)
, (nextval('students_student_id_seq'), '2002-08-13', 34)
, (nextval('students_student_id_seq'), '2001-12-26', 35)
, (nextval('students_student_id_seq'), '2001-05-31', 36)
;
