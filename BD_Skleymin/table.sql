CREATE TABLE street_inf (
    street_num SERIAL PRIMARY KEY,
    street VARCHAR(30) UNIQUE
);
CREATE TABLE name_inf (
    name_num SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE
);
CREATE TABLE last_name_inf (
    last_name_num SERIAL PRIMARY KEY,
    last_name VARCHAR(30) UNIQUE
);
CREATE TABLE otch_inf (
    otch_num SERIAL PRIMARY KEY,
    otch VARCHAR(30) UNIQUE
);
CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    last_name INT,
    name int,
    otch int,
    street int,
    stroenie VARCHAR(10),
    korp VARCHAR(10),
    room INT,
    phone VARCHAR(12),
    FOREIGN KEY (last_name) REFERENCES last_name_inf (last_name_num),
	FOREIGN KEY (name) REFERENCES name_inf (name_num),
	FOREIGN KEY (otch) REFERENCES otch_inf (otch_num),
	FOREIGN KEY (street) REFERENCES street_inf (street_num)
);
insert into name_inf values (1,'Erica');
insert into name_inf values (2,'Vladimir');
insert into name_inf values (3,'Andrey');
insert into name_inf values (4,'Ovik');
insert into name_inf values (5,'Levon');

insert into last_name_inf values (1,'Khutieva');
insert into last_name_inf values (2,'Vestyak');
insert into last_name_inf values (3,'Zemskov');
insert into last_name_inf values (4,'Matevosian');
insert into last_name_inf values (5,'Agamirov');

insert into otch_inf values (1,'Arsenovna');
insert into otch_inf values (2,'Anatolievich');
insert into otch_inf values (3,'Vladimirovich');
insert into otch_inf values (4,'Amayakovich');
insert into otch_inf values (5,'Levonovich');

insert into street_inf values (1,'Prospekt mira');
insert into street_inf values (2,'Viatskaya');
insert into street_inf values (3,'Dubosekovskaya');
insert into street_inf values (4,'Arbatskaya');
insert into street_inf values (5,'Sobolevski proezd');

insert into contacts values (1,1,1,1,3,89,10,10,898888888888);
insert into contacts values (2,2,2,2,1,41,5,1,88005553535);
insert into contacts values (3,3,3,3,2,4,1,88,88007777535);
insert into contacts values (4,4,4,4,4,77,8,56,89335233635);
insert into contacts values (5,5,2,5,5,71,15,11,88227758538);
insert into contacts values (6,5,5,3,5,71,15,11,88227777777);


select *
from contacts
join last_name_inf on last_name_inf.last_name_num=contacts.last_name
join name_inf on name_num=contacts.name
join otch_inf on otch_num=contacts.otch
join street_inf on street_num=contacts.street