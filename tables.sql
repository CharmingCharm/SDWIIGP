create table UserGroup(
    gID int auto_increment,
    groupName varchar(15) not null,
    description varchar(200),
    primary key (gID)
);

create table User(
    uID int auto_increment,
    name varchar(15),
    password varchar(30),
    primary key (uID)
);

create table PrivilegeGroup(
    pgID int auto_increment,
    privilege bigint,
    primary key (pgID)
);

create table Submission(
    sID int auto_increment,
    uID int,
    pID int,
    score numeric(6,2),
    code clob,
    isSolution boolean,
    dateAndTime timestamp,
    primary key (sID),
    foreign key (uID) references User,
    foreign key (pID) references Problem
);

create table Problem(
    pID int auto_increment,
    tsID int,
    level int,
    title varchar(20),
    description varchar(200),
    primary key (pID)
);

create table Tag(
    tagID int auto_increment,
    tagName varchar(20),
    primary key (tagID)
)

create table Task(
    taskID int auto_increment,
    taskName varchar(15),
    deadline timestamp,
    primary key (taskID)
);

create table TestSet(
    tsID int auto_increment,
    pID int,
    primary key (tsID),
    foreign key (pID) references Problem
);

create table Test(
    testID int auto_increment,
    score numeric(6,2),
    code clob,
    primary key (testID)
);

create table UserInGroup(
    uID int,
    gID int,
    foreign key (uID) references User,
    foreign key (gID) references UserGroup
);

create table UserInPGroup(
    uID int,
    pgID int,
    foreign key (uID) references User,
    foreign key (pgID) references PrivilegeGroup
);

create table TagOfProblem(
    tagID int,
    pID int,
    foreign key (tagID) references Tag,
    foreign key (pID) references Problem
);

create table TestSetHasTest(
    testID int,
    tsID int,
    foreign key (tsID) references TestSet,
    foreign key (testID) references Test
);

create table ProblemInTask(
    taskID int,
    pID int,
    foreign key (taskID) references Task,
    foreign key (pID) references Problem
);