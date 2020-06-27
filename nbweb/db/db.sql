create table users(
  usr_id serial primary key,
  usr_name varchar(20) unique not null,
  usr_group varchar(50) null,
  usr_mobile char(11) unique null,
  usr_email varchar(128) unique null,
  usr_ip char(16) unique not null,
  usr_status boolean not null default '1',
  usr_ctime timestamp not null
);

create table notes(
  nt_id serial primary key,
  nt_usr_id bigint not null references users(usr_id),
  nt_text text not null
);
