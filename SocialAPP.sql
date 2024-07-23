create database Social_APP
create table Users(
UserID INT PRIMARY KEY NOT NULL,
Fname VARCHAR(20) NOT NULL,
Lname VARCHAR(10) NOT NULL,
Email VARCHAR(100) NOT NULL,
Passwords VARCHAR(100) NOT NULL,
Job VARCHAR(100),
University_Name VARCHAR,
BirthDate DATE
)
create table Posts(
PostID INT PRIMARY KEY NOT NUll,
UserID int FOREIGN KEY REFERENCES Users(UserID),
Post_Content TEXT,
Created_at DATE,
)
Create Table Groups(
GroupID INT PRIMARY KEY NOT NUll,
G_name VARCHAR(20) NOT NULL,
G_Description TEXT,
Created_at DATE,
UserID int FOREIGN KEY REFERENCES Users(UserID)
)
create table GroupMember(
UserID int FOREIGN KEY REFERENCES Users(UserID),
GroupID int FOREIGN KEY REFERENCES Groups(GroupID)
)
Create Table GroupDiscussion(
discussionID INT PRIMARY KEY NOT NUll,
UserID int FOREIGN KEY REFERENCES Users(UserID),
GroupID int FOREIGN KEY REFERENCES Groups(GroupID),
title VARCHAR(100),
content TEXT,
created_at DATE
)
Create Table GroupDiscussionReplies(
replyID INT PRIMARY KEY NOT NUll,
discussionID int FOREIGN KEY REFERENCES GroupDiscussion(discussionID),
UserID int FOREIGN KEY REFERENCES Users(UserID),
content TEXT,
created_at DATE
)
Create Table Profiles(
profileID INT PRIMARY KEY NOT NUll,
UserID int FOREIGN KEY REFERENCES Users(UserID),
bio TEXT,
profile_picture_url VARCHAR,
locations VARCHAR
)
Create Table Friends(
UserID int UNIQUE FOREIGN KEY REFERENCES Users(UserID),
FriendID int UNIQUE FOREIGN KEY REFERENCES Users(UserID),
Friend_status  VARCHAR(50) NOT NULL CHECK (Friend_status IN ('Accepted','Rejected','Blocked','Pending'))
)
Create Table Likes(
UserID int FOREIGN KEY REFERENCES Users(UserID),
PostID int FOREIGN KEY REFERENCES Posts(PostID)
)
Create Table Comments(
UserID int FOREIGN KEY REFERENCES Users(UserID),
PostID int FOREIGN KEY REFERENCES Posts(PostID),
commentContent TEXT,
created_at DATE
)
