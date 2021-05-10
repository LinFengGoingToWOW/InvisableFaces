-- Project Name : noname
-- Date/Time    : 2021/05/10 14:27:45
-- Author       : gao_xiaolin
-- RDBMS Type   : Microsoft SQL Server 2008 ～
-- Application  : A5:SQL Mk-2

-- 职员表
drop table if exists staffs;

create table staffs (
  no int not null IDENTITY(1,1)
  , url nvarchar(200) not null
  , type nchar(1) not null
  , name nvarchar(20) not null
  , gender nchar(1) not null
  , birthyear numeric(4, 0) not null
  , constraint staffs_PKC primary key (no)
) ;

create index staffs_IX1
  on staffs(url,type);

-- 演员
drop table if exists actors;

create table actors (
  no int not null IDENTITY(1,1)
  , url nvarchar(200) not null
  , name nvarchar(20) not null
  , gender nchar(1) not null
  , birthyear numeric(4, 0) not null
  , constraint actors_PKC primary key (no)
) ;

create index actors_IX1
  on actors(url);

create index actors_IX2
  on actors(name);

create index actors_IX3
  on actors(birthyear);

-- 爬取清单
drop table if exists checklists;

create table checklists (
  no int not null IDENTITY(1,1)
  , table_name nvarchar(45) not null
  , url nvarchar(200) not null
  , is_checked bit not null
  , has_items bit not null
  , constraint checklists_PKC primary key (no)
) ;

create index checklists_IX1
  on checklists(table_name,url);

-- 电视剧
drop table if exists tv_dramas;

create table tv_dramas (
  no int not null IDENTITY(1,1)
  , url nvarchar(200) not null
  , name nvarchar(200) not null
  , original_release_year numeric(4, 0) not null
  , production_year numeric(4, 0) not null
  , area nvarchar(50)
  , constraint tv_dramas_PKC primary key (no)
) ;

create index tv_dramas_IX1
  on tv_dramas(url);

create index tv_dramas_IX2
  on tv_dramas(name);

-- 电视剧演职员
drop table if exists tv_dramas_actors_staffs;

create table tv_dramas_actors_staffs (
  no int not null IDENTITY(1,1)
  , tv_drama_url nvarchar(200) not null
  , type nchar(1) not null
  , actor_staff_url nvarchar(200) not null
  , constraint tv_dramas_actors_staffs_PKC primary key (no)
) ;

create index tv_dramas_actors_staffs_IX1
  on tv_dramas_actors_staffs(tv_drama_url);

create index tv_dramas_actors_staffs_IX2
  on tv_dramas_actors_staffs(actor_staff_url);

execute sp_addextendedproperty N'MS_Description', N'职员表', N'SCHEMA', N'dbo', N'TABLE', N'staffs', null, null;
execute sp_addextendedproperty N'MS_Description', N'no', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'no';
execute sp_addextendedproperty N'MS_Description', N'url', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'url';
execute sp_addextendedproperty N'MS_Description', N'类型:导演：1，编剧：2', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'type';
execute sp_addextendedproperty N'MS_Description', N'名字', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'name';
execute sp_addextendedproperty N'MS_Description', N'性别:女：0，男：1， 不明：9', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'gender';
execute sp_addextendedproperty N'MS_Description', N'出生年份', N'SCHEMA', N'dbo', N'TABLE', N'staffs', N'COLUMN', N'birthyear';

execute sp_addextendedproperty N'MS_Description', N'演员', N'SCHEMA', N'dbo', N'TABLE', N'actors', null, null;
execute sp_addextendedproperty N'MS_Description', N'no', N'SCHEMA', N'dbo', N'TABLE', N'actors', N'COLUMN', N'no';
execute sp_addextendedproperty N'MS_Description', N'url', N'SCHEMA', N'dbo', N'TABLE', N'actors', N'COLUMN', N'url';
execute sp_addextendedproperty N'MS_Description', N'名字', N'SCHEMA', N'dbo', N'TABLE', N'actors', N'COLUMN', N'name';
execute sp_addextendedproperty N'MS_Description', N'性别:女：０、男：１、不明：9', N'SCHEMA', N'dbo', N'TABLE', N'actors', N'COLUMN', N'gender';
execute sp_addextendedproperty N'MS_Description', N'出生年份', N'SCHEMA', N'dbo', N'TABLE', N'actors', N'COLUMN', N'birthyear';

execute sp_addextendedproperty N'MS_Description', N'爬取清单', N'SCHEMA', N'dbo', N'TABLE', N'checklists', null, null;
execute sp_addextendedproperty N'MS_Description', N'no', N'SCHEMA', N'dbo', N'TABLE', N'checklists', N'COLUMN', N'no';
execute sp_addextendedproperty N'MS_Description', N'表名', N'SCHEMA', N'dbo', N'TABLE', N'checklists', N'COLUMN', N'table_name';
execute sp_addextendedproperty N'MS_Description', N'Url', N'SCHEMA', N'dbo', N'TABLE', N'checklists', N'COLUMN', N'url';
execute sp_addextendedproperty N'MS_Description', N'爬取状态', N'SCHEMA', N'dbo', N'TABLE', N'checklists', N'COLUMN', N'is_checked';
execute sp_addextendedproperty N'MS_Description', N'有无义项', N'SCHEMA', N'dbo', N'TABLE', N'checklists', N'COLUMN', N'has_items';

execute sp_addextendedproperty N'MS_Description', N'电视剧', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', null, null;
execute sp_addextendedproperty N'MS_Description', N'no', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'no';
execute sp_addextendedproperty N'MS_Description', N'作品Url', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'url';
execute sp_addextendedproperty N'MS_Description', N'作品名', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'name';
execute sp_addextendedproperty N'MS_Description', N'首播年份', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'original_release_year';
execute sp_addextendedproperty N'MS_Description', N'制作年份', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'production_year';
execute sp_addextendedproperty N'MS_Description', N'制片地区', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas', N'COLUMN', N'area';

execute sp_addextendedproperty N'MS_Description', N'电视剧演职员', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas_actors_staffs', null, null;
execute sp_addextendedproperty N'MS_Description', N'no', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas_actors_staffs', N'COLUMN', N'no';
execute sp_addextendedproperty N'MS_Description', N'作品Url', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas_actors_staffs', N'COLUMN', N'tv_drama_url';
execute sp_addextendedproperty N'MS_Description', N'演职员类型:0.演员，1.导演，2.编剧', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas_actors_staffs', N'COLUMN', N'type';
execute sp_addextendedproperty N'MS_Description', N'演职员Url', N'SCHEMA', N'dbo', N'TABLE', N'tv_dramas_actors_staffs', N'COLUMN', N'actor_staff_url';

