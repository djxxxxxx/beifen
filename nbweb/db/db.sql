create table users(
  usr_id serial primary key,
  usr_name varchar(20) unique not null,
  usr_group varchar(50) null,
  usr_mobile char(11) unique null,
  usr_email varchar(128) unique null,
  usr_ip char(16) unique not null,
  usr_status boolean not null default '1',
  usr_ctime time not null default current_timestamp
);

create table groups(
  grp_id serial primary key,
  grp_name varchar(50) unique not null,
  grp_ctime time not null default current_timestamp
);

create table notes(
  nt_id serial primary key,
  nt_usr_id bigint not null,
  nt_txt text not null,
  nt_ctime time not null default current_timestamp
);

create table types(
  typ_id serial primary key,
  typ_name varchar(20) not null
);

create table articles(
  atc_id serial primary key,
  atc_usr_id bigint not null,
  atc_title varchar(128) not null,
  atc_type varchar(20) not null,
  atc_group varchar(50) null,
  atc_text text not null,
  atc_ctime time not null default current_timestamp
);

create table comments(
  cmt_id serial primary key,
  cmt_tpc_id bigint not null,
  cmt_text text,
  cmt_ctime time not null default current_timestamp
);

create table topics(
  tpc_id serial primary key,
  tpc_usr_id bigint not null,
  tpc_title varchar(128) not null,
  tpc_type varchar(20) not null,
  tpc_text text not null,
  tpc_ctime time not null default current_timestamp
);
