create table users(
  user_id serial primary key,
  user_name varchar(10) unique not null,
  passwd varchar(50) not null
);
