CREATE EXTENSION IF NOT EXISTS postgis;


create table users(
	username text primary key,
	hashed_password text not null
);



create table if not exists job(
	job_number text primary KEY
	,project text
	,client text
);


drop table core;
create table if not exists core
(	sample_number int primary key
	,location_1 text
	,location_2 text
	,location_3 text
	,job_number text
	,core_number int
	,sec text
	,chainage float
	,direction text
	,wheelpath text
	,left_offset float
	,pt geometry(Point,27700)
	,surface_defect text
	,sampled_date date
	,logged_date date
	,sampled_by text
	,logged_by text
	,unique(core_number,job_number)
 	,foreign key(job_number) references job(job_number) on delete cascade on update cascade
);