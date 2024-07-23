create database Social_APP;

USE Social_APP;

-- User Schema
CREATE SCHEMA [User];

CREATE TABLE [User].Users(
  UserID INT IDENTITY(0, 1) PRIMARY KEY,
  Fname VARCHAR(20) NOT NULL,
  Lname VARCHAR(20) NOT NULL,
  Email VARCHAR(100) NOT NULL,
  Passwords VARCHAR(100) NOT NULL,
  Job VARCHAR(100),
  University_Name VARCHAR,
  BirthDate DATE NOT NULL
);

CREATE TABLE [User].Profiles(
  profileID INT IDENTITY(0, 1) PRIMARY KEY,
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  bio TEXT,
  profile_picture_url VARCHAR,
  [location] VARCHAR,
  CONSTRAINT Unique_Profile UNIQUE (UserID)
);

CREATE TABLE [User].Friends(
  UserID int UNIQUE FOREIGN KEY REFERENCES [User].Users(UserID),
  FriendID int UNIQUE FOREIGN KEY REFERENCES [User].Users(UserID),
  Friend_status VARCHAR(50) NOT NULL CHECK (Friend_status IN ('Accepted','Rejected','Blocked','Pending')),
  CONSTRAINT Unique_Friend UNIQUE (UserID, FriendID)
);


-- Post Schema
CREATE SCHEMA Post;

CREATE TABLE Post.Posts(
  PostID INT IDENTITY(0, 1) PRIMARY KEY,
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  Post_Content TEXT NOT NULL,
  Created_at DATETIME DEFAULT GETDATE(),
);

CREATE TABLE Post.Likes(
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  PostID int FOREIGN KEY REFERENCES Post.Posts(PostID),
  CONSTRAINT Unique_Like_User UNIQUE (UserID, PostID)
);

CREATE TABLE Post.Comments(
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  PostID int FOREIGN KEY REFERENCES Post.Posts(PostID),
  commentContent TEXT NOT NULL,
  created_at DATETIME DEFAULT GETDATE()
);


-- Group Schema
CREATE SCHEMA [Group];

CREATE TABLE [Group].Groups(
  GroupID INT IDENTITY(0, 1) PRIMARY KEY,
  G_name VARCHAR(20) NOT NULL,
  G_Description TEXT NOT NULL,
  Created_at DATETIME DEFAULT GETDATE(),
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID)
);

CREATE TABLE [Group].GroupMember(
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  GroupID int FOREIGN KEY REFERENCES [Group].Groups(GroupID),
  CONSTRAINT Unique_GP_MB UNIQUE (UserID, GroupID)
);

CREATE Table [Group].GroupDiscussion(
  discussionID INT IDENTITY(0, 1) PRIMARY KEY,
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  GroupID int FOREIGN KEY REFERENCES [Group].Groups(GroupID),
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT GETDATE()
);

CREATE Table [Group].GroupDiscussionReplies(
  replyID INT IDENTITY(0, 1) PRIMARY KEY,
  discussionID int FOREIGN KEY REFERENCES [Group].GroupDiscussion(discussionID),
  UserID int FOREIGN KEY REFERENCES [User].Users(UserID),
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT GETDATE()
);


/*BACKUP DATABASE Social_APP
TO DISK = N'D:\work\DataEng_DEPI\DEPI_PROJECT\beta\SocialApp.bak'
WITH FORMAT;*/
