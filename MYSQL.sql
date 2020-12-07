CREATE TABLE comment(
	comment_id VARCHAR(64),  
    -- if comment_id is "super" means its a comment
    -- else if its a random string with length 64 then its a reply 
  	parent_id VARCHAR(64),
  	author VARCHAR(128),
  	comments_text TEXT,
    measured_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  	PRIMARY KEY(comment_id)
);