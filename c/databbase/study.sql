drop database study;

create database study default charset=utf8mb4 default collate utf8mb4_unicode_ci;

use study;

create table user(
    user_id bigint unsigned auto_increment,
    user_name varchar(64) not null,
    user_passwd varchar(128) not null,
    user_mobile char(11) not null,
    user_email varchar(128) not null,
    user_ip char(16) not null,
    user_status boolean default 1,
    user_ctime datetime not null default current_timestamp,
    primary key (user_id),
    unique (user_name),
    unique (user_mobile),
    unique (user_email),
    unique (user_ip)
)engine=InnoDB default charset=utf8;

create table type(
    type_id bigint unsigned auto_increment,
    type_name varchar(64) not null,
    type_ctime datetime not null default current_timestamp,
    type_utime datetime not null default current_timestamp on update current_timestamp,
    primary key (type_id),
    unique (type_name)
)engine=InnoDB default charset=utf8;

create table article(
    article_id bigint unsigned auto_increment,
    article_title varchar(128) not null,
    article_type varchar(64) not null,
    article_user_id bigint unsigned not null,
    article_user_name varchar(64) not null,
    article_body text not null,
    article_rdnum bigint not null default 0,
    article_ctime datetime not null default current_timestamp,
    article_utime datetime not null default current_timestamp on update current_timestamp,
    primary key (article_id),
    constraint foreign key (article_user_id) references user(user_id)
)engine=InnoDB default charset=utf8;

create table comments(
    comments_id bigint unsigned auto_increment,
    comments_user_id bigint unsigned not null,
    comments_text text not null,
    comments_ctime datetime not null default current_timestamp,
    primary key (comments_id),
    constraint foreign key (comments_user_id) references user(user_id)
)engine=InnoDB default charset=utf8;

