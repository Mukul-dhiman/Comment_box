CREATE TABLE comment(
	comment_id VARCHAR(64),
  	parent_id VARCHAR(64),  
    -- if parent_id is "super" means its a comment
    -- else if its a random string with length=16 then its a reply 
  	author VARCHAR(128),
  	comments_text TEXT,
    comment_on VARCHAR(16),
  	PRIMARY KEY(comment_id)
);