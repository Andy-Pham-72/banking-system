-- ANDY PHAM BANKING SYSTEM PROJECT --

# UNKNOWN BANK MANAGEMENT DATABASE

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `bankingsys`
--

CREATE database bankingsys;
USE bankingsys;

##################################################

--
-- Table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `acc_no` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` char(30) DEFAULT NULL,
  `last_name` char(30) DEFAULT NULL,
  `dob` varchar(100) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `acc_type` varchar(20) DEFAULT NULL,
  `status` char(15) DEFAULT NULL,
  `balance` float(15,2) DEFAULT NULL,
  PRIMARY KEY (`acc_no`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

--
-- Inserting data for table `customer`
--

INSERT INTO `customer` (`acc_no`, `first_name`, `last_name`, `dob`, `phone`, `email`, `acc_type`, `status`, `balance`) VALUES
(1, 'John', 'Pham', '02-07-1991', '647-901-8899', 'johnpham@gmail.com', 'checking', 'active', 65200.00),
(2, 'Niki', 'Johanson', '08-04-1982', '466-894-3452', 'niki@hotmail.com', 'saving', 'active', 18000.00),
(3, 'Alexa', 'Mongor', '10-09-1962', '776-364-7689', 'alexa@shopify.com', 'saving', 'active', 90530.60),
(4, 'Michael', 'Xavier', '12-24-1977', '967-438-2651', 'xavierm@gmail.com', 'saving', 'close', 7430.12),
(5, 'Alice', 'Horenfrew', '09-23-1999', '457-859-2490', 'aliceholre@yahoo.com', 'checking', 'active', 689.06);

##################################################

--
-- Table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `amount` float(10) DEFAULT NULL,
  `type` char(20) DEFAULT NULL,
  `acc_no` int(10) DEFAULT NULL,
  PRIMARY KEY (`index`),
  FOREIGN KEY (`acc_no`) REFERENCES customer(`acc_no`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Inserting data for table `transaction`
--

INSERT INTO `transaction` (`index`, `date`, `amount`, `type`, `acc_no`) VALUES
(1, '2021-10-16', 3000, 'deposit', 1),
(2, '2021-10-15', 10000, 'deposit', 2),
(3, '2021-10-18', 2400, 'withdraw', 1),
(4, '2021-11-30', 900, 'deposit', 4),
(5, '2021-11-30', 1500, 'withdraw', 3),
(6, '2021-11-30', 70, 'withdraw', 5);

##################################################
