--ALTER SEQUENCE seq RESTART WITH 1;
--UPDATE table SET column_id=nextval('seq');


/* Словари */

INSERT INTO classrooms (number,description) VALUES
('А-100', 'Лекционная аудитория')
,  ('А-305', 'Аудитория для лабораторных работ по физике')
,  ('А-306', 'Аудитория для лабораторных работ по физике')
,  ('К-207', 'Аудитория')
,  ('К-208', 'Аудитория')
,  ('В-209', 'Компьютерная аудитория')
,  ('К-710', 'Компьютерная аудитория')
,  ('Г-410', 'Лекционная аудитория')
,  ('Г-411', 'Лекционная аудитория')
,  ('А-303', 'Лекционная аудитория')
,  ('СК', 'Спортивный комплекс')
;

INSERT INTO coefficients (coef_num,description) VALUES
( 1, 'default')
, ( 3, 'Контрольная работа')
, ( 2, 'Самостаятельная работа')
, ( 1, 'Домашнее задание')
, ( 1, 'Работа на семинаре')
, ( 1, 'Выступление с докладом')
, ( 5, 'Экзамен')
, ( 5, 'Зачёт')
, ( 3, 'Коллоквиум')
, ( 2, 'Сдача нормативов')
;

INSERT INTO disciplines ("name",description) VALUES
( 'Физика', null)
, ( 'Философия', null)
, ( 'Мат. анализ', 'Высшая математика - Матемаический анализ')
, ( 'Лин. алгебра', 'Высшая математика - Линейная алгебра')
, ( 'Диффуры', 'Высшая математика - Дифференциальные уравнения')
, ( 'ЭБ', 'Экономическая безопасность')
, ( 'Налоги', 'Налогооблажение в Российской Федерации')
, ( 'ООП', 'Объектно-Ориентированное Программирование')
, ( 'ЯП', 'Языки Программирования')
, ( 'БОС', 'Безопасность Операционных Систем')
, ( 'Физкультура', null)
;

INSERT INTO groups (name) VALUES
( 'П23-100')
, ( 'Ф23-101')
, ( 'Э23-102')
, ( 'П24-100')
, ( 'Ф24-101')
;

INSERT INTO lessons_times (start_time,end_time,"name") VALUES
	 ('08:30:00','10:05:00','1 пара'),
	 ('10:15:00','11:50:00','2 пара'),
	 ('12:45:00','14:20:00','3 пара'),
	 ('14:30:00','16:05:00','4 пара'),
	 ('16:15:00','17:50:00','5 пара'),
	 ('12:00:00','13:35:00','3 пара v2'),
	 ('18:00:00','19:35:00','6 пара')
;


/* Пользователи */

INSERT INTO user_customuser ("password",last_login,is_superuser,username,email,is_staff,is_active,date_joined,first_name,last_name,second_name) VALUES
	 ('pbkdf2_sha256$720000$hmzFBl57irmmVFXyE3Phfy$A8GNP9ipSXUB78ECm/vQIF3jvf0ZDnyse9ah3x8ev2U=','2024-11-04 14:05:55.774609+03',true,'admin','admin@admin.admin',true,true,'2024-11-04 02:39:39.019125+03','','',NULL),
	 ('pbkdf2_sha256$720000$mc9yLouQxtODFijED1sSNN$uqpT53Gbu8JuoNLr5QCl2iHTpKacBqi8rxvd5UYhjek=',NULL,false,'amd001','andreykomd@mail.ru',false,true,'2024-11-04 15:17:28.128969+03','Максим','Андрейко','Дмитриевич'),
	 ('pbkdf2_sha256$720000$tmajfE2GrGMd2WomXYE8az$uJE10BVts57amV8BXMrFg7ux7ziRNGIjU7bwFMV/Des=',NULL,false,'aaa001','afanasevaaa@mail.ru',false,true,'2024-11-04 15:46:50.78656+03','Алина','Афанасьева','Александровна'),
	 ('pbkdf2_sha256$720000$qD7t1yHqbkYWWNxHG7aPhv$eDZOTXANpV0aznazSYHmAvdELyhXMAdREATBTRWRV7Y=',NULL,false,'bai001','belyaevai@mail.ru',false,true,'2024-11-04 15:47:48.226553+03','Алексей','Беляев','Игоревич'),
	 ('pbkdf2_sha256$720000$NwyzOdpCGRycKCgeHjH9ht$/pvDnsz9kaVF5FllSV4SmupKzs10Mo3kaKTal/VkEc4=',NULL,false,'zea001','zhukovea@mail.ru',false,true,'2024-11-04 15:49:42.915009+03','Егор','Жуков','Александрович'),
	 ('pbkdf2_sha256$720000$bu03ce9e5oQyBsVafz1NUm$GlDz5/VfyBkKN+nIY3kpV+8VTKq22aIq9TZGSQZAVXE=',NULL,false,'zia001','zlatovratskiyia@mail.ru',false,true,'2024-11-04 15:50:51.107522+03','Иван','Златовратский','Алексеевич'),
	 ('pbkdf2_sha256$720000$7ac9O83fOF9iYdlF0YIkil$SJEQLruyMvgO8QNUvD47o7K5TCzP+mydjNrGQfT6epQ=',NULL,false,'lto001','lobastovato@mail.ru',false,true,'2024-11-04 15:59:55.333086+03','Татьяна','Лобастова','Олеговна'),
	 ('pbkdf2_sha256$720000$5Jda7PQHSXviuH49DliNax$Mf1ZL5GBKVv6J+adUqaJW4CO5ZqpBT8MR8qaZuuiVfw=',NULL,false,'msm001','melnikovsm@mail.ru',false,true,'2024-11-04 16:04:14.626375+03','Савелий','Мельников','Михайлович'),
	 ('pbkdf2_sha256$720000$yev3eiarF6rmARmY27hzq8$Y/GuALHMPhORYMiZbX21yzkqvhxFxhz7GazPvmnii6s=',NULL,false,'pns001','prischepenkons@mail.ru',false,true,'2024-11-04 16:05:00.439863+03','Никита','Прищепенко','Сергеевич'),
	 ('pbkdf2_sha256$720000$R17AwStvzHKUtYw7nvYzUJ$ldPfh15xfp7qXP4GiyTyx4JZrLk5hPTtBq4ptChhSo4=',NULL,false,'rvp001','romanovvp@mail.ru',false,true,'2024-11-04 16:06:07.401071+03','Владислав','Романов','Павлович'),
	 ('pbkdf2_sha256$720000$z94mncp2ZkUFvK8NyIWDHa$VaWRv+yYACDF2krizAER82fd9GNbkGgCIcslVXzjD94=',NULL,false,'sad001','suxorukixad@mail.ru',false,true,'2024-11-04 16:07:34.246642+03','Анастасия','Сухоруких','Дмитриевна'),
	 ('pbkdf2_sha256$720000$m10NdDrcR0jqCxGauTHbIF$32Ypn7oWT20F8K6em80dzREcPJm3mdtvcT6SoZ9B0Hg=',NULL,false,'fms001','fokinams@mail.ru',false,true,'2024-11-04 16:08:26.075174+03','Мария','Фокина','Сергеевна'),
	 ('pbkdf2_sha256$720000$F65raGW8uoXS3IP6xEbU4f$pIneSGlQyXcttuD0n515eoIuWpOGZG/hoYSClmlKr7Y=',NULL,false,'cia001','chaltsevia@mail.ru',false,true,'2024-11-04 16:09:39.802677+03','Илья','Чальцев','Антонович'),
	 ('pbkdf2_sha256$720000$kWRhiMWwLAAgZB5clkmFYV$XOjIf5T3fR7bxLPrbNuJwJo//cw4cvqe6FIiGPUOIDM=',NULL,false,'aki001','abramov@mail.ru',false,true,'2024-11-04 16:58:24.191414+03','Кирилл','Абрамов','Игоревич'),
	 ('pbkdf2_sha256$720000$IkahT13x6JXXeX6MpUwIf1$KazMl7UN6/5O+GnxWHci6ZW1G+q7NCwqpCascib91lg=',NULL,false,'baa001','bakanov@mail.ru',false,true,'2024-11-04 17:59:32.066585+03','Артем','Баканов','Александрович'),
	 ('pbkdf2_sha256$720000$OsBnwpEFG43TGP9ISOpCiF$7+tXS725P2OcpnrXZzpDugQWoILzrNCfQedINtLYVMA=',NULL,false,'bya001','baryshnikova@mail.ru',false,true,'2024-11-04 18:03:29.024189+03','Юлия','Барышникова','Алексеевна'),
	 ('pbkdf2_sha256$720000$rS5nNjXPXcmdrYci8ZIwNh$srVoHVHbRH+5dmHx11bM+cmmaQ7vGtvis1NS37tcDCQ=',NULL,false,'vvo001','vatulin@mail.ru',false,true,'2024-11-04 18:04:56.496215+03','Валентин','Ватулин','Олегович'),
	 ('pbkdf2_sha256$720000$AcZXhgd3XH6plRFPExALGV$J3WmstlgYWZ7ersF3qMhZ4YEmJyOG25VPakKEfdPaxY=',NULL,false,'vvm001','volodin@mail.ru',false,true,'2024-11-04 18:10:54.602484+03','Владислав','Володин','Михайлович'),
	 ('pbkdf2_sha256$720000$yL7Kc1xNtBOJXz7tlyfvth$IWpe5cPr8iJHPDNWFsuJ3JpLTWK+9JZpHi7/VCfP714=',NULL,false,'das001','degtyarev@mail.ru',false,true,'2024-11-04 18:11:47.082811+03','Александр','Дегтярев','Сергеевич'),
	 ('pbkdf2_sha256$720000$XTeAJF1AtjBDReEg0Ia458$0EUOu/I/2djeDdrqZH3eROHd5qQd8uIO0WRxgkUgVu4=',NULL,false,'zap001','zaborovskaya@mail.ru',false,true,'2024-11-04 18:12:48.950934+03','Анна','Заборовская','Павловна'),
	 ('pbkdf2_sha256$720000$ayty8dhyoyACtFj2XXgErU$dHVO84wNtN/GTwsxn/0HfC1zvt4F388tVKYVwa7Xt94=',NULL,false,'ias001','inashevskiy@mail.ru',false,true,'2024-11-04 18:14:09.416716+03','Александр','Инашевский','Сергеевич'),
	 ('pbkdf2_sha256$720000$NuAXuvWb0JThI9bBrfo0GZ$tIMMjTzh2ZAyx8LHwaMviMq4w2wRDf0or39oOJ41Q24=',NULL,false,'iea001','ionova@mail.ru',false,true,'2024-11-04 18:17:17.626588+03','Екатерина','Ионова','Олеговна'),
	 ('pbkdf2_sha256$720000$XgvY2eizF5u5fxrFf9pWzX$iwTDwdediPaZUxvvDNLRs1yhCIyZnYhAQQduycbnMPs=',NULL,false,'ldd001','labzunova@mail.ru',false,true,'2024-11-04 18:18:05.928322+03','Дарья','Лабзунова','Дмитриевна'),
	 ('pbkdf2_sha256$720000$taHqSAsTbHSKNJGP9s8wDB$w9D8OGHhol7Mk6IJTKT8nn4NPhTGO/c8oEKkrBB8GjI=',NULL,false,'mor001','malyshev@mail.ru',false,true,'2024-11-04 18:18:57.922945+03','Олег','Малышев','Романович'),
	 ('pbkdf2_sha256$720000$VDxDWD1is1ctbZ11MBxOp3$3RzR/FyINcf3dTnsE33VdJmQL6YDwZoinW4VZqrcthQ=',NULL,false,'mvs001','masliy@mail.ru',false,true,'2024-11-04 18:19:47.886865+03','Владислав','Маслий','Сергеевич'),
	 ('pbkdf2_sha256$720000$icRCpZWktMSn2k1Duc6EJv$xGFzuS5VBDbwHYnJxEGrbzwdNGTAv4z7l+D1vsnx1Jk=',NULL,false,'mia001','milovidov@mail.ru',false,true,'2024-11-04 18:20:23.39538+03','Иван','Миловидов','Антонович'),
	 ('pbkdf2_sha256$720000$lPobIfAv5nDhl5OtO0sksU$rz1cDou6NwLo2w9pEgqR5IxvMo+DNArfiS1eALrgOWk=',NULL,false,'mge001','mironov@mail.ru',false,true,'2024-11-04 18:21:01.524434+03','Григорий','Миронов','Евгеньевич'),
	 ('pbkdf2_sha256$720000$Tx539BYOM7oDRSiUClcWrO$D7U7TySEhEXkTrS2u1rdz9aScS8qhNwWRQndSjd/NKQ=',NULL,false,'mma001','mitsevich@mail.ru',false,true,'2024-11-04 18:21:31.198617+03','Максим','Мицевич','Александрович'),
	 ('pbkdf2_sha256$720000$7TwnRb1Nms7zxzYQTyvLXl$e3L4/MxyIM4kTbjMxzOqacbDL4TmZ1nHQ5kPQvIe+lk=',NULL,false,'ndi001','nedoluzhko@mail.ru',false,true,'2024-11-04 18:22:18.165237+03','Денис','Недолужко','Игоревич'),
	 ('pbkdf2_sha256$720000$uunPOel1yoKTxSX3QTslrG$xxtzGTuTDiU7YGH0fa3JVZERGOPiwxRPP6sUaJEmI7I=',NULL,false,'sda001','sergeeva@mail.ru',false,true,'2024-11-04 18:22:52.498396+03','Диана','Сергеева','Алексеевна'),
	 ('pbkdf2_sha256$720000$2EGVJGW7mBFlgmVaOzuNcL$eYjYLBQFZw3iSdEqChjfVP7qOBGgVHHiaueFri4lkRM=',NULL,false,'sma001','sorokin@mail.ru',false,true,'2024-11-04 18:23:20.449557+03','Михаил','Сорокин','Андреевич'),
	 ('pbkdf2_sha256$720000$UDsMgfEQJzxHdviz3niyzb$VaPJrM/iQlm0FIyAFcfCv+8CRwgv2mMq0vqRqdKGduI=',NULL,false,'fda001','fomenko@mail.ru',false,true,'2024-11-04 18:24:23.949713+03','Данил','Фоменко','Александрович'),
	 ('pbkdf2_sha256$720000$9yQdVtUoNvNDRIGL9Yxjlv$NSejA2KvCqMXfgvaUHHu/n95DfHGgK+m5lE3sbXsXfs=',NULL,false,'fra001','fomichev@mail.ru',false,true,'2024-11-04 18:25:03.167439+03','Роман','Фомичев','Александрович'),
	 ('pbkdf2_sha256$720000$rMpRg4qPpugWMvzBpCAspE$ZgQRgEQ1G4eARd6R4mniDkfL0Fa7YzgbbgQUWDXy9kA=',NULL,false,'fia001','frolov@mail.ru',false,true,'2024-11-04 18:25:59.079535+03','Иван','Фролов','Алексеевич'),
	 ('pbkdf2_sha256$720000$NZXiK81BzgwbO2xpUqnj01$lPbqFEl6iMaz+jnITLZ74dp25HuySYJmyBZgSwP0g3c=',NULL,false,'xdn001','xarke@mail.ru',false,true,'2024-11-04 18:26:49.423257+03','Денис','Харке','Николаевич'),
	 ('pbkdf2_sha256$720000$wsD96CgtaHVVBGvNJNvzi9$nKYIKXh/LBVk4r2QuRqvtDuMHgBajWnL0srzjlcvhzI=',NULL,false,'sto001','shabrov@mai.ru',false,true,'2024-11-04 18:27:32.658921+03','Тимофей','Шабров','Олегович'),
	 ('pbkdf2_sha256$720000$uYsjUKBwOF3rutJEZ0G6E5$VWZiS7L0DB1eIjtdz4G9QE7XPblZSCNZitu//kgzrXw=',NULL,true,'dap','dolgovap@mail.ru',false,true,'2024-11-05 23:48:31.323','Александр','Долгов','Павлович'),
	 ('pbkdf2_sha256$720000$uYsjUKBwOF3rutJEZ0G6E5$VWZiS7L0DB1eIjtdz4G9QE7XPblZSCNZitu//kgzrXw=',NULL,true,'mia','mashkovaia@mail.ru',false,true,'2024-11-05 23:48:31.323','Ирина','Машкова','Алексеевна')
;

INSERT INTO tutors (date_of_birth,user_id) VALUES
('1995-08-13', 2)
, ('1989-04-17', 3)
, ('1989-01-31', 4)
, ('1985-11-06', 5)
, ('1987-04-17', 6)
, ('1991-07-01', 7)
, ('1994-12-24', 8)
, ('1987-07-07', 9)
, ('1986-05-30', 10)
, ('1992-02-01', 11)
, ('1988-07-29', 12)
, ('1994-06-25', 13)
;

INSERT INTO students (date_of_birth,user_id) VALUES
( '2001-07-14', 14)
, ( '2001-10-11', 15)
, ( '2001-01-19', 16)
, ( '2002-03-25', 17)
, ( '2001-09-12', 18)
, ( '2002-02-18', 19)
, ( '2001-02-28', 20)
, ( '2002-08-15', 21)
, ( '2001-02-26', 22)
, ( '2001-05-17', 23)
, ( '2002-06-23', 24)
, ( '2001-07-27', 25)
, ( '2002-03-11', 26)
, ( '2001-09-09', 27)
, ( '2001-10-03', 28)
, ( '2002-07-06', 29)
, ( '2002-09-01', 30)
, ( '2001-12-04', 31)
, ( '2001-11-07', 32)
, ( '2001-12-19', 33)
, ( '2002-08-13', 34)
, ( '2001-12-26', 35)
, ( '2001-05-31', 36)
;
