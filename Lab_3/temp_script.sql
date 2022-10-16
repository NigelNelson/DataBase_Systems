create table Video_Recordings_New(
recording_id int,
director varchar(40),
title varchar(40),
category varchar(30),
image_name varchar(40),
duration float,
rating varchar(10),
year_released float,
price float,
stock_count float(10,2)
);

create table ratings(
rating varchar(10)
);

create table directors(
name varchar(40)
);

create table video_categories_new(
name varchar(30)
);

create table features(
recording_id int,
actor_name varchar(40)
);

create table Video_Actors_New(
name varchar(40)
);

insert into video_recordings_new 
select recording_id, director, title,
category, image_name, duration, rating,
 year_released, price, stock_count
from video_recordings
where recording_id is not null;

insert into ratings 
select distinct rating
from video_recordings;

insert into directors 
select distinct director
from video_recordings;

insert into video_categories_new 
select distinct category
from video_recordings;

insert into features 
select recording_id, name
from video_actors;

insert into video_actors_new 
select distinct name
from video_actors;

alter table video_recordings_new add constraint primary key(recording_id);

alter table video_actors_new add constraint primary key(name);

alter table ratings add constraint primary key(rating);

alter table directors add constraint primary key(name);

alter table video_categories_new add constraint primary key(name);

alter table video_recordings_new add constraint foreign key(rating) references ratings(rating);

alter table video_recordings_new add constraint foreign key(director) references directors(name);

alter table video_recordings_new add constraint foreign key(category) references video_categories_new(name);

alter table features add constraint foreign key(recording_id) references video_recordings_new(recording_id);

alter table features add constraint foreign key(actor_name) references video_actors_new(name);

alter table features add constraint primary key(recording_id, actor_name);
 

 
