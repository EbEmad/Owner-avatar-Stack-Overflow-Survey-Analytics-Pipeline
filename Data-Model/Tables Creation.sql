create TABLE Developer (
    DeveloperKey INT PRIMARY KEY,
    DeveloperStatus VARCHAR(100),
    AgeRange VARCHAR(20),
    Country VARCHAR(100),
    EducationLevel VARCHAR(100),
    DeveloperType VARCHAR(255),
    RemoteWork VARCHAR(20),
    YearsCoding VARCHAR(50),
    YearsCodingProfessionally VARCHAR(50),
    OrganizationSize VARCHAR(50),
    Industry VARCHAR(100)
);

CREATE TABLE FactResponses (
    ResponseKey INT PRIMARY KEY,
    ResponseId INT NOT NULL,
    Year INT,
    DeveloperKey INT,
    Salary FLOAT,
    WorkExperience INT,
    FOREIGN KEY (DeveloperKey) REFERENCES Developer(DeveloperKey)
);

CREATE TABLE ResponseEmploymentStatus (
    ResponseKey INT,
    EmploymentStatusDescription VARCHAR(255),
	PRIMARY KEY(ResponseKey, EmploymentStatusDescription),
    FOREIGN KEY (ResponseKey) REFERENCES FactResponses(ResponseKey)
);

CREATE TABLE ResponseTechnologies (
    ResponseKey INT,
    TechnologyType VARCHAR(50),
    TechnologyName VARCHAR(100),
    PRIMARY KEY (ResponseKey, TechnologyType, TechnologyName),
    FOREIGN KEY (ResponseKey) REFERENCES FactResponses(ResponseKey)
);
