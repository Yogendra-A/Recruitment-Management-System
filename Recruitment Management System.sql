CREATE SCHEMA IF NOT EXISTS `Recruitment_Management_System`;

use Recruitment_Management_System;

CREATE TABLE IF NOT EXISTS Recruitment_Management_System.Users( 
    name VARCHAR(45) NOT NULL, 
    email VARCHAR(120) NOT NULL,   
    type VARCHAR(45) NOT NULL,
    password VARCHAR(45) NULL,  
    UNIQUE INDEX email_UNIQUE (email), 
    CHECK (type in ('Recruiter','Client')),
    PRIMARY KEY (email)
);

CREATE TABLE IF NOT EXISTS Recruitment_Management_System.Recruiter(
    RID INT NOT NULL AUTO_INCREMENT,
    RName VARCHAR(45) NOT NULL,
    REmail VARCHAR(45) NOT NULL,
    CompanyName VARCHAR(45) NOT NULL,
    CompanyLocation VARCHAR(45) NOT NULL,
    RGender VARCHAR(2) NOT NULL,
    PRIMARY KEY (RID),
    UNIQUE (REmail)
);

CREATE TABLE IF NOT EXISTS Recruitment_Management_System.Client (
    CID INT NOT NULL AUTO_INCREMENT,
    CName VARCHAR(45) NOT NULL,
    CEmail VARCHAR(45) NOT NULL,
    CAge INT NOT NULL,
    CLocation VARCHAR(45) NOT NULL,
    CGender VARCHAR(2) NOT NULL,
    CExp varchar(45) not NUll,
    CSkills VARCHAR(45) NOT NULL,
    CQualification VARCHAR(45) NOT NULL,
    CResume LONGBLOB,
    CResumeFileName VARCHAR(255),
    UNIQUE (CEmail),
    PRIMARY KEY (CID)
);

CREATE TABLE IF NOT EXISTS Recruitment_Management_System.Job (
    RID INT NOT NULL,
    JID INT NOT NULL AUTO_INCREMENT,
    JobRole VARCHAR(45) NOT NULL,
    JobType VARCHAR(45) NOT NULL,
    Qualification VARCHAR(45) NOT NULL,
    MinExp varchar(45) NOT NULL,
    Salary INT NOT NULL,
    FOREIGN KEY (RID) REFERENCES Recruitment_Management_System.Recruiter(RID),
    PRIMARY KEY (JID)
);

CREATE TABLE IF NOT EXISTS Recruitment_Management_System.Application(
    AID INT NOT NULL AUTO_INCREMENT,
    RID INT NOT NULL,
    JID INT NOT NULL,
    CID INT NOT NULL,
    Status VARCHAR(20) DEFAULT 'Pending',
    PRIMARY KEY(AID),
    FOREIGN KEY(RID) REFERENCES Recruitment_Management_System.Recruiter(RID),
    FOREIGN KEY(JID) REFERENCES Recruitment_Management_System.Job(JID),
    FOREIGN KEY(CID) REFERENCES Recruitment_Management_System.Client(CID),
    CHECK (Status in ('Pending', 'Accepted', 'Rejected'))
);




DELIMITER //

CREATE TRIGGER prevent_duplicate_job_posting
BEFORE INSERT ON Job
FOR EACH ROW
BEGIN
    DECLARE job_count INT;
    SELECT COUNT(*) INTO job_count
    FROM Job
    WHERE RID = NEW.RID 
      AND JobRole = NEW.JobRole
      AND JobType = NEW.JobType
      AND Qualification = NEW.Qualification
      AND MinExp = NEW.MinExp
      AND Salary = NEW.Salary;
    
    IF job_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate job posting is not allowed';
    END IF;
END;
//

DELIMITER ;


ALTER TABLE Recruitment_Management_System.Client
ADD COLUMN ApplicationCount INT DEFAULT 0;



DELIMITER //

CREATE TRIGGER update_application_count
AFTER INSERT ON Application
FOR EACH ROW
BEGIN
    UPDATE Client
    SET ApplicationCount = (SELECT COUNT(*) FROM Application WHERE CID = NEW.CID)
    WHERE CID = NEW.CID;
END;
//
DELIMITER ;



SELECT 
    j.JobRole,
    COUNT(a.AID) AS TotalApplications
FROM 
    Recruitment_Management_System.Application a
JOIN 
    Recruitment_Management_System.Job j ON a.JID = j.JID
GROUP BY 
    j.JobRole;


use Recruitment_Management_System;
DELIMITER //

CREATE PROCEDURE DeleteJob(
    IN p_JID INT
)
BEGIN
    -- Delete related applications first to maintain referential integrity
    DELETE FROM Application WHERE JID = p_JID;
    
    -- Delete the job itself
    DELETE FROM Job WHERE JID = p_JID;
    
    -- Optionally, you can add a message or logging mechanism here
    -- to confirm the deletion or log the action.
END //

DELIMITER ;

CALL DeleteJob(3);  -- Replace 123 with the actual job ID you want to delete

