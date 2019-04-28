/*
drop database if exists oj;

create database oj;
grant all privileges on oj.* to 'sdwii'@'%' identified by 'sdwii';
flush privileges;
*/

use oj;

create table UserGroup(
    gID int not null auto_increment,
    groupName varchar(64) not null,
    description text not null default '',
    primary key (gID)
);

create table User(
    uID int not null auto_increment,
    name varchar(64) not null,
    password varchar(256) not null,
    primary key (uID),
	unique key uq_User_name (name)
);

create table PrivilegeGroup(
    pgID int not null auto_increment,
    privilege bigint not null,
    primary key (pgID)
);

create table Problem(
    pID int not null auto_increment,
    tsID int default null,
    level int not null,
    title varchar(64) not null,
    description text not null,
    primary key (pID)
);

create table Submission(
    sID int not null auto_increment,
    uID int not null,
    pID int not null,
    score numeric(6,2) default null,
    code text not null,
    isSolution boolean not null default False,
    datetime timestamp not null default CURRENT_TIMESTAMP,
    primary key (sID),
    constraint `fk_Submission_uID` foreign key (uID) references User (uID),
    constraint `fk_Submission_pID` foreign key (pID) references Problem (pID)
);

create table Tag(
    tagID int not null auto_increment,
    tagName varchar(64) not null,
    primary key (tagID)
);

create table Task(
    taskID int not null auto_increment,
    taskName varchar(64) not null,
    deadline timestamp not null,
    primary key (taskID)
);

create table TestSet(
    tsID int not null auto_increment,
    pID int not null,
    primary key (tsID),
    constraint `fk_TestSet_pID` foreign key (pID) references Problem (pID)
);

create table Test(
    testID int not null auto_increment,
    score numeric(6,2) not null,
    code text not null,
    primary key (testID)
);

create table UserInGroup(
    uID int not null,
    gID int not null,
    constraint `fk_UserInGroup_uID` foreign key (uID) references User (uID),
    constraint `fk_UserInGroup_gID` foreign key (gID) references UserGroup (gID)
);

create table UserInPGroup(
    uID int not null,
    pgID int not null,
    constraint `fk_UserInPGroup_uID` foreign key (uID) references User (uID),
    constraint `fk_UserInPGroup_pgID` foreign key (pgID) references PrivilegeGroup (pgID)
);

create table TagOfProblem(
    tagID int not null,
    pID int not null,
    constraint `fk_TagOfProblem_tagID` foreign key (tagID) references Tag (tagID),
    constraint `fk_TagOfProblem_pID` foreign key (pID) references Problem (pID)
);

create table TestSetHasTest(
    tsID int not null,
    testID int not null,
    constraint `fk_TestSetHasTest_tsID` foreign key (tsID) references TestSet (tsID),
    constraint `fk_TestSetHasTest_testID` foreign key (testID) references Test (testID)
);

create table ProblemInTask(
    taskID int not null,
    pID int not null,
    constraint `fk_ProblemInTask_taskID` foreign key (taskID) references Task (taskID),
    constraint `fk_ProblemInTask_pID` foreign key (pID) references Problem (pID)
);
