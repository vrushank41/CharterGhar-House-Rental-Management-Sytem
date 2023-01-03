-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2022 at 03:55 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `house_rental`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `age_dob` (IN `dob` DATE, OUT `age` INT)   begin
    SELECT DATE_FORMAT(FROM_DAYS(DATEDIFF(NOW(), dob)), '%Y') + 0 AS age
into age;
end$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `end_date_calc` (IN `start_date` DATE, IN `duration` INT, OUT `end_date` DATE)   begin
    select date_add(`start_date`, INTERVAL `duration` MONTH) into end_date;
    
end$$

--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `rent_remain` (`Amount` DOUBLE, `Total` DOUBLE) RETURNS DOUBLE DETERMINISTIC BEGIN
     DECLARE remain double;
        return Total-Amount;
    END$$

CREATE DEFINER=`root`@`localhost` FUNCTION `totalrent` (`duration` INT, `Total` DOUBLE) RETURNS DOUBLE DETERMINISTIC BEGIN
    --  DECLARE remain double;
        return duration*Total;
    END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `contract`
--

CREATE TABLE `contract` (
  `Contract_ID` int(6) NOT NULL,
  `Start_Date` date DEFAULT NULL,
  `Duration` int(2) NOT NULL DEFAULT 1,
  `Rent_Cost_Duration` int(10) DEFAULT NULL,
  `Owner_ID` int(6) DEFAULT NULL,
  `Tenant_ID` int(6) DEFAULT NULL,
  `House_ID` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contract`
--

INSERT INTO `contract` (`Contract_ID`, `Start_Date`, `Duration`, `Rent_Cost_Duration`, `Owner_ID`, `Tenant_ID`, `House_ID`) VALUES
(400001, '2022-11-16', 6, 42000, 100002, 300020, 200009),
(400003, '2022-11-28', 18, 360000, 100004, 300000, 200011),
(400009, '2022-11-29', 9, 76500, 100004, 300003, 200015),
(400010, '2022-11-29', 9, 225000, 100004, 300000, 200011);

--
-- Triggers `contract`
--
DELIMITER $$
CREATE TRIGGER `all_details` AFTER INSERT ON `contract` FOR EACH ROW BEGIN
insert into contract_save select contract_Id,start_date,Owner.Owner_ID,owner.F_Name,Owner.L_Name,owner_ph.Ph_No,House.House_ID,House.House_Addr,House.Htype,BHK,tenant.Tenant_ID,tenant.F_Name,tenant.L_Name,tenant_ph.Ph_No, tenant.Status=1 from contract INNER join owner on contract.Owner_ID=owner.Owner_ID inner join tenant on contract.Tenant_ID=tenant.Tenant_ID inner join house on contract.House_ID=house.House_ID inner join house_type on house.Htype=house_type.Type_No inner join owner_ph on owner.Owner_ID=owner_ph.Owner_ID INNER JOIN tenant_ph on tenant.Tenant_ID=tenant_ph.Tenant_ID where Contract_ID=new.Contract_ID;
UPDATE contract_save set status=1;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `contract_save`
--

CREATE TABLE `contract_save` (
  `Contract_ID` int(11) NOT NULL,
  `Start_Date` date NOT NULL,
  `Owner_ID` int(11) NOT NULL,
  `O_Fname` varchar(50) NOT NULL,
  `O_Lname` varchar(50) NOT NULL,
  `O_Ph` varchar(10) NOT NULL,
  `House_ID` int(11) NOT NULL,
  `House_Addr` varchar(50) NOT NULL,
  `Htype` int(11) NOT NULL,
  `BHK` varchar(10) NOT NULL,
  `Tenant_ID` int(11) NOT NULL,
  `T_Fname` varchar(50) NOT NULL,
  `T_Lname` varchar(50) NOT NULL,
  `T_Ph` varchar(10) NOT NULL,
  `Status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contract_save`
--

INSERT INTO `contract_save` (`Contract_ID`, `Start_Date`, `Owner_ID`, `O_Fname`, `O_Lname`, `O_Ph`, `House_ID`, `House_Addr`, `Htype`, `BHK`, `Tenant_ID`, `T_Fname`, `T_Lname`, `T_Ph`, `Status`) VALUES
(400009, '2022-11-29', 100004, 'Om', 'Prasad', '9780678542', 200015, 'Near Electronic City Campus', 4, '4 BHK', 300003, 'Prathap', 'P', '9768457902', 1),
(400010, '2022-11-29', 100004, 'Om', 'Prasad', '9780678542', 200011, 'jaynagar', 4, '4 BHK', 300000, 'Sathvik', 'A', '9067825372', 1);

-- --------------------------------------------------------

--
-- Table structure for table `house`
--

CREATE TABLE `house` (
  `House_ID` int(11) NOT NULL,
  `House_Addr` varchar(50) NOT NULL,
  `Htype` int(2) DEFAULT NULL,
  `Rent_Cost` int(10) DEFAULT NULL,
  `Owner_ID` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `house`
--

INSERT INTO `house` (`House_ID`, `House_Addr`, `Htype`, `Rent_Cost`, `Owner_ID`) VALUES
(200007, 'Bellary', 3, 10000, 100000),
(200008, 'gauribidanur', 2, 8000, 100001),
(200009, 'puttur', 1, 7000, 100002),
(200010, 'rr nagar', 5, 15000, 100003),
(200011, 'jaynagar', 4, 25000, 100004),
(200015, 'Near Electronic City Campus', 4, 8500, 100004);

-- --------------------------------------------------------

--
-- Table structure for table `house_type`
--

CREATE TABLE `house_type` (
  `Type_No` int(2) NOT NULL,
  `BHK` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `house_type`
--

INSERT INTO `house_type` (`Type_No`, `BHK`) VALUES
(1, '1 BHK'),
(2, '2 BHK'),
(3, '3 BHK'),
(4, '4 BHK'),
(5, '5 BHK');

-- --------------------------------------------------------

--
-- Table structure for table `owner`
--

CREATE TABLE `owner` (
  `Owner_ID` int(6) NOT NULL,
  `F_Name` varchar(10) NOT NULL,
  `L_Name` varchar(10) NOT NULL,
  `Username` varchar(10) NOT NULL,
  `Password` varchar(10) NOT NULL,
  `Owner_Addr` varchar(50) DEFAULT NULL,
  `DOB` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `owner`
--

INSERT INTO `owner` (`Owner_ID`, `F_Name`, `L_Name`, `Username`, `Password`, `Owner_Addr`, `DOB`) VALUES
(100000, 'Vrushank', 'G', 'vrush41', '12345', '2nd cross,millerpet,bellary', '2002-08-12'),
(100001, 'Hemanth', 'N', 'hemanth28', '23456', '4th cross,gauribidanur,chikkaballapur', '2002-01-28'),
(100002, 'Dhanush', 'M D', 'mdebro', '34567', '2nd cross,puttur,mangaluru', '2002-06-01'),
(100003, 'Srinivas', 'Y', 'vasu03', '45678', '3rd cross,rr nagar,bengaluru', '2002-03-27'),
(100004, 'Om', 'Prasad', 'om123', '56789', '2nd cross,jaynagar,bengaluru', '2002-05-10'),
(100017, 'Sundeep', 'A', 'sundy123', '12345', 'Avambhavi,Bellary', '2012-11-14');

-- --------------------------------------------------------

--
-- Table structure for table `owner_ph`
--

CREATE TABLE `owner_ph` (
  `Owner_ID` int(6) DEFAULT NULL,
  `Ph_No` char(10) NOT NULL
) ;

--
-- Dumping data for table `owner_ph`
--

INSERT INTO `owner_ph` (`Owner_ID`, `Ph_No`) VALUES
(100000, '9876929479'),
(100002, '9087565643'),
(100003, '9884143767'),
(100004, '9780678542'),
(100017, '9876543211'),
(100001, '7676110011');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `Payment_ID` int(11) NOT NULL,
  `Pay_From` varchar(20) NOT NULL,
  `Payment_Date` date DEFAULT NULL,
  `Amount` int(10) NOT NULL,
  `Tenant_ID` int(6) DEFAULT NULL,
  `Contract_ID` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`Payment_ID`, `Pay_From`, `Payment_Date`, `Amount`, `Tenant_ID`, `Contract_ID`) VALUES
(500000, 'Nayan', '2022-11-16', 1500, 300020, 400001),
(500004, 'Nayan', '2022-11-19', 2000, 300020, 400001),
(500010, 'Sathvik', '2022-11-24', 20000, 300000, 400003);

--
-- Triggers `payment`
--
DELIMITER $$
CREATE TRIGGER `amount_exceed` AFTER INSERT ON `payment` FOR EACH ROW BEGIN IF (select sum(Amount)+new.Amount from Payment where Contract_ID=400001) > 42000 THEN SIGNAL SQLSTATE '45000' SET message_text="Amount can't exceed total Rent Cost";END IF;END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `tenant`
--

CREATE TABLE `tenant` (
  `Tenant_ID` int(6) NOT NULL,
  `F_Name` varchar(10) NOT NULL,
  `L_Name` varchar(10) NOT NULL,
  `Username` varchar(10) NOT NULL,
  `Password` varchar(10) NOT NULL,
  `Tenant_Addr` varchar(50) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Status` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tenant`
--

INSERT INTO `tenant` (`Tenant_ID`, `F_Name`, `L_Name`, `Username`, `Password`, `Tenant_Addr`, `DOB`, `Status`) VALUES
(300000, 'Sathvik', 'A', 'sathvik12', 'sat123', 'jaynagar', '2002-04-03', 1),
(300001, 'Teja', 'Kanala', 'teja123', 'tej123', 'None', '2002-07-21', 0),
(300002, 'Soumith', 'B', 'soumpi', 'sou123', 'bellary', '2002-01-23', 0),
(300003, 'Prathap', 'P', 'ptp45', '12988', 'Near Electronic City Campus', '2002-07-09', 1),
(300020, 'Nayan', 'K', 'nyn987', '09876', 'puttur', '2002-04-03', 1),
(300021, 'Soumith', 'Sai', 'saisou123', '12345', 'Ashok complex,Bellary', '2002-01-23', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tenant_ph`
--

CREATE TABLE `tenant_ph` (
  `Tenant_ID` int(6) DEFAULT NULL,
  `Ph_No` char(10) NOT NULL
) ;

--
-- Dumping data for table `tenant_ph`
--

INSERT INTO `tenant_ph` (`Tenant_ID`, `Ph_No`) VALUES
(300000, '9067825372'),
(300001, '6273682936'),
(300002, '9808577578'),
(300003, '9768457902'),
(300020, '9000900090'),
(300021, '8134156789');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contract`
--
ALTER TABLE `contract`
  ADD PRIMARY KEY (`Contract_ID`),
  ADD KEY `fk_house_id` (`House_ID`),
  ADD KEY `fk_owner_id3` (`Owner_ID`),
  ADD KEY `fk_tenant_id2` (`Tenant_ID`);

--
-- Indexes for table `house`
--
ALTER TABLE `house`
  ADD PRIMARY KEY (`House_ID`,`House_Addr`),
  ADD KEY `fk_owner_id2` (`Owner_ID`),
  ADD KEY `fk_house_type` (`Htype`);

--
-- Indexes for table `house_type`
--
ALTER TABLE `house_type`
  ADD PRIMARY KEY (`Type_No`,`BHK`),
  ADD UNIQUE KEY `Type_No` (`Type_No`);

--
-- Indexes for table `owner`
--
ALTER TABLE `owner`
  ADD PRIMARY KEY (`Owner_ID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD UNIQUE KEY `Owner_Addr` (`Owner_Addr`);

--
-- Indexes for table `owner_ph`
--
ALTER TABLE `owner_ph`
  ADD KEY `fk_owner_id` (`Owner_ID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`Payment_ID`),
  ADD KEY `fk_contract_id` (`Contract_ID`),
  ADD KEY `fk_tenant_id3` (`Tenant_ID`);

--
-- Indexes for table `tenant`
--
ALTER TABLE `tenant`
  ADD PRIMARY KEY (`Tenant_ID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `tenant_ph`
--
ALTER TABLE `tenant_ph`
  ADD KEY `fk_tenant_id` (`Tenant_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contract`
--
ALTER TABLE `contract`
  MODIFY `Contract_ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=400011;

--
-- AUTO_INCREMENT for table `house`
--
ALTER TABLE `house`
  MODIFY `House_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=200016;

--
-- AUTO_INCREMENT for table `owner`
--
ALTER TABLE `owner`
  MODIFY `Owner_ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100020;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `Payment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=500011;

--
-- AUTO_INCREMENT for table `tenant`
--
ALTER TABLE `tenant`
  MODIFY `Tenant_ID` int(6) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=300022;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `contract`
--
ALTER TABLE `contract`
  ADD CONSTRAINT `fk_house_id` FOREIGN KEY (`House_ID`) REFERENCES `house` (`House_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_owner_id3` FOREIGN KEY (`Owner_ID`) REFERENCES `owner` (`Owner_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_tenant_id2` FOREIGN KEY (`Tenant_ID`) REFERENCES `tenant` (`Tenant_ID`) ON DELETE CASCADE;

--
-- Constraints for table `house`
--
ALTER TABLE `house`
  ADD CONSTRAINT `fk_house_type` FOREIGN KEY (`Htype`) REFERENCES `house_type` (`Type_No`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_owner_id2` FOREIGN KEY (`Owner_ID`) REFERENCES `owner` (`Owner_ID`) ON DELETE CASCADE;

--
-- Constraints for table `owner_ph`
--
ALTER TABLE `owner_ph`
  ADD CONSTRAINT `fk_owner_id` FOREIGN KEY (`Owner_ID`) REFERENCES `owner` (`Owner_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `fk_contract_id` FOREIGN KEY (`Contract_ID`) REFERENCES `contract` (`Contract_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_tenant_id3` FOREIGN KEY (`Tenant_ID`) REFERENCES `tenant` (`Tenant_ID`) ON DELETE CASCADE;

--
-- Constraints for table `tenant_ph`
--
ALTER TABLE `tenant_ph`
  ADD CONSTRAINT `fk_tenant_id` FOREIGN KEY (`Tenant_ID`) REFERENCES `tenant` (`Tenant_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
