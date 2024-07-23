# DEPI_SOCIAL_PROJECT

## Team Members

- Omar Baher 
- Eyad Gamal
- Yahia Mohamed

## ERD
![DEPI_ERD_PROJECT_page-0001](https://github.com/user-attachments/assets/af7d00ea-1150-443f-8c42-1707a00f94f2)
# Relational Entity-Relationship Diagram (ERD)

This is a Relational Entity-Relationship Diagram (ERD). It illustrates the relationships and structure of a relational database for a data engineering project. The diagram shows various entities (tables), their attributes (columns), and the relationships between them using primary keys (PK), foreign keys (FK), and composite keys (CK).

## Main Components

### Entities (Tables)
Represented by rectangles. Each table contains attributes and their data types.

- **Users**: Contains user details like userID, first name, last name, email, password, job, university name, and birthdate.
- **Groups**: Contains group details like groupID, name, description, created_at, and userID (foreign key from Users).
- **Posts**: Contains post details like postID, userID (foreign key from Users), postContent, and created_at.
- **Profiles**: Contains profile details like profileID, userID (foreign key from Users), bio, profile_picture_url, and location.
- **Comments**: Contains comment details like userID (foreign key from Users), postID (foreign key from Posts), commentContent, and created_at.
- **GroupDiscussion**: Contains discussion details like discussionID, groupID (foreign key from Groups), userID (foreign key from Users), title, content, and created_at.
- **GroupDiscussionReplies**: Contains reply details like replyID, discussionID (foreign key from GroupDiscussion), userID (foreign key from Users), content, and created_at.
- **GroupMember**: Contains membership details like groupID (foreign key from Groups) and userID (foreign key from Users).
- **Likes**: Contains details like userID (foreign key from Users) and postID (foreign key from Posts).
- **Friends**: Contains friendship details like userID (foreign key from Users), friendID (foreign key from Users), and status.

### Relationships
Illustrated using lines connecting the tables with symbols indicating the type of relationship (one-to-many, many-to-many, etc.).

### Keys
- **Primary Keys (PK)**: Unique identifiers for each table are shown in purple.
- **Foreign Keys (FK)**: Attributes that create a link between tables, shown in blue.
- **Composite Keys (CK)**: A combination of two or more columns in the table used to identify a row, shown in green uniquely.

The diagram uses standard ERD notation to help visualize and understand the database structure, its entities, and how they relate.


## Physical Database Diagram 
![physical database diagram](https://github.com/user-attachments/assets/4f0a36cc-c3e3-40d2-9907-9b913a3a36fb)

The image represents a Physical Database Diagram. This type of diagram illustrates the specific implementation of the database schema in a Database Management System (DBMS). It includes details like table names, columns, data types, and the relationships between tables with primary and foreign keys.

## Breakdown of the Components in the Diagram

### Tables and Columns

- **Users**: 
  - userID (PK)
  - Fname
  - Lname
  - email
  - password
  - job
  - university_name
  - birthDate
- **Posts**: 
  - postID (PK)
  - userID (FK)
  - post_content
  - created_at
- **Comments**: 
  - userID (FK)
  - postID (FK)
  - commentContent
  - created_at
- **Groups**: 
  - groupID (PK)
  - name
  - description
  - created_at
  - userID (FK)
- **GroupMember**: 
  - userID (FK)
  - groupID (FK)
- **GroupDiscussion**: 
  - discussionID (PK)
  - groupID (FK)
  - userID (FK)
  - title
  - content
  - created_at
- **GroupDiscussionReplies**: 
  - replyID (PK)
  - discussionID (FK)
  - userID (FK)
  - content
  - created_at
- **Profiles**: 
  - profileID (PK)
  - userID (FK)
  - bio
  - profile_picture_url
  - location
- **Likes**: 
  - userID (FK)
  - postID (FK)
- **Friends**: 
  - userID (FK)
  - friendID (FK)
  - status

### Relationships

- Lines connecting tables indicate the relationships between them, typically foreign key constraints.
- The symbols at the ends of the lines (crow's feet, circles) indicate the type of relationship (one-to-many, many-to-many).

### Keys

- **Primary Keys (PK)**: Uniquely identify records within a table, usually underlined or marked with a key symbol.
- **Foreign Keys (FK)**: Establish relationships between tables by referring to primary keys in other tables.

This diagram provides a detailed view of how the database tables are structured, their columns, and the data types used. It also shows how the tables are connected through foreign keys, illustrating the referential integrity constraints within the database.
