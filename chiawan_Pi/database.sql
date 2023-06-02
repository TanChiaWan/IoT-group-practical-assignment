CREATE TABLE `entriesLog` (
    `id` int(20) NOT NULL AUTO_INCREMENT, 
    `cardID` varchar(9) NOT NULL,
    `user` varchar(50) NOT NULL,
    `status` varchar(10) NOT NULL,
    `datetime` varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE `registeredCardOwners` (
    `cardID` varchar(9) NOT NULL,
    `ownerName` varchar(50) NOT NULL,
    `role` varchar(20) NOT NULL,
    PRIMARY KEY (cardID)
);

INSERT INTO `registeredCardOwners` (`cardID`, `ownerName`, `role`) VALUES
('1AEE56AD', 'Kong Chek Fung', 'Student'),
('311CF11D', 'Teacher A', 'Teacher'),
('F2F4F919', 'Tan Chia Wan', 'Student'),
('B34FA618', 'Lawrence Lian Anak Billy', 'Student'),
('2A692940', 'Teacher B', 'Teacher'),
('E2AAB919', 'Kevin Alvaro Frandi', 'Student'),
('313EA51D', 'Universe Card User', 'Universe Card User');

CREATE TABLE `electricityLog` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `status` varchar(5) NOT NULL,
    `datetime` varchar(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE `lightingLog` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `status` varchar(5) NOT NULL,
    `datetime` varchar(50) NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE `airCondLog` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `status` varchar(10) NOT NULL,
    `datetime` varchar(50) NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE `punishmentTriggeredLog` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `triggeredDatetime` varchar(50) NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE `attendanceList` (
    `id` int(20) NOT NULL AUTO_INCREMENT,
    `date` varchar(30) NOT NULL,
    `studentName` varchar(50) NOT NULL,
    `remark` varchar(200),
    PRIMARY KEY (id)
)
