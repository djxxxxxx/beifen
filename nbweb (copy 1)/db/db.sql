create table users(
  uid serial primary key,
  uname varchar(20) unique not null,
  upasswd varchar(50) not null,
  ugroup varchar(50) null,
  umobile char(11) unique null,
  uemail varchar(128) unique null,
  uip char(16) unique not null,
  ustatus boolean not null default '1',
  uctime timestamp not null
);

create table types(
  tid serial primary key,
  tname varchar(20)
);

create table groups(
  gid serial primary key,
  gname varchar(50),
  gctime timestamp not null
);

create table notes(
  nid serial primary key,
  ntitle varchar(128) not null,
  nuname varchar(20) not null references users(uname),
  ntype varchar(20) not null,
  ngroup varchar(50) null,
  ntext text not null,
  nctime timestamp not null,
  nutime timestamp not null
);

create table info(
  iid serial primary key,
  iip char(15) unique not null,
  iurl varchar(128) not null,
  itime timestamp not null
);
