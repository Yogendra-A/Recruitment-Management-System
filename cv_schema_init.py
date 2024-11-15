import mysql.connector
from mysql.connector import Error

try:
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',     # Change as needed
        user='your_username', # Replace with your MySQL username
        password='your_password' # Replace with your MySQL password
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Create Schema if it doesn't exist
    cursor.execute("CREATE SCHEMA IF NOT EXISTS `Recruitment_Management_System`;")
    cursor.execute("USE Recruitment_Management_System;")

    # SQL commands for creating tables
    create_tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS Users(
            name VARCHAR(45) NOT NULL, 
            email VARCHAR(120) NOT NULL,   
            type VARCHAR(45) NOT NULL,
            password VARCHAR(45) NULL,  
            UNIQUE INDEX email_UNIQUE (email), 
            CHECK (type in ('Recruiter','Client')),
            PRIMARY KEY (email)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Recruiter(
            RID INT NOT NULL AUTO_INCREMENT,
            RName VARCHAR(45) NOT NULL,
            REmail VARCHAR(45) NOT NULL,
            CompanyName VARCHAR(45) NOT NULL,
            CompanyLocation VARCHAR(45) NOT NULL,
            RGender VARCHAR(2) NOT NULL,
            PRIMARY KEY (RID),
            UNIQUE (REmail)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Client(
            CID INT NOT NULL AUTO_INCREMENT,
            CName VARCHAR(45) NOT NULL,
            CEmail VARCHAR(45) NOT NULL,
            CAge INT NOT NULL,
            CLocation VARCHAR(45) NOT NULL,
            CGender VARCHAR(2) NOT NULL,
            CExp INT NOT NULL,
            CSkills VARCHAR(45) NOT NULL,
            CQualification VARCHAR(45) NOT NULL,
            CResume LONGBLOB,
            CResumeFileName VARCHAR(255),
            UNIQUE (CEmail),
            PRIMARY KEY (CID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Job(
            RID INT NOT NULL,
            JID INT NOT NULL AUTO_INCREMENT,
            JobRole VARCHAR(45) NOT NULL,
            JobType VARCHAR(45) NOT NULL,
            Qualification VARCHAR(45) NOT NULL,
            MinExp INT NOT NULL,
            Salary INT NOT NULL,
            FOREIGN KEY (RID) REFERENCES Recruiter(RID),
            PRIMARY KEY (JID)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Application(
            AID INT NOT NULL AUTO_INCREMENT,
            RID INT NOT NULL,
            JID INT NOT NULL,
            CID INT NOT NULL,
            Status VARCHAR(20) DEFAULT 'Pending',
            PRIMARY KEY(AID),
            FOREIGN KEY(RID) REFERENCES Recruiter(RID),
            FOREIGN KEY(JID) REFERENCES Job(JID),
            FOREIGN KEY(CID) REFERENCES Client(CID),
            CHECK (Status in ('Pending', 'Accepted', 'Rejected'))
        );
        """
    ]

    # Execute each table creation SQL command
    for command in create_tables_sql:
        cursor.execute(command)

    # Add the ApplicationCount column to Client table
    cursor.execute("ALTER TABLE Client ADD COLUMN ApplicationCount INT DEFAULT 0;")

    # Create Trigger for preventing duplicate job posting
    cursor.execute("""
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
    """)

    # Create Trigger for updating application count
    cursor.execute("""
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
    """)

    # Example query to get total applications per job role
    cursor.execute("""
    SELECT 
        j.JobRole,
        COUNT(a.AID) AS TotalApplications
    FROM 
        Application a
    JOIN 
        Job j ON a.JID = j.JID
    GROUP BY 
        j.JobRole;
    """)

    # Fetch and display results
    results = cursor.fetchall()
    for row in results:
        print(f"Job Role: {row[0]}, Total Applications: {row[1]}")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close the database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
