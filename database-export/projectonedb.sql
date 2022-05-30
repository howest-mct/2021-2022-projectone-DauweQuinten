-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: projectonedb
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actie`
--

DROP TABLE IF EXISTS `actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actie` (
  `actieid` int NOT NULL AUTO_INCREMENT,
  `beschrijving` varchar(255) NOT NULL,
  PRIMARY KEY (`actieid`),
  KEY `idx_beschrijving` (`beschrijving`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actie`
--

LOCK TABLES `actie` WRITE;
/*!40000 ALTER TABLE `actie` DISABLE KEYS */;
INSERT INTO `actie` VALUES (1,'read sensor'),(2,'set actuator');
/*!40000 ALTER TABLE `actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `deviceid` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL,
  `model` varchar(45) NOT NULL DEFAULT 'onbekend',
  `merk` varchar(45) NOT NULL DEFAULT 'onbekend',
  `beschrijving` varchar(255) DEFAULT NULL,
  `type` varchar(45) NOT NULL,
  `meeteenheid` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`deviceid`),
  KEY `idx_naam` (`naam`),
  KEY `idx_model` (`model`),
  KEY `idx_type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (1,'niveausensor','DYP-A02YY','onbekend','Waterdichte ultrasoonsensor','sensor','mm'),(2,'niveauswitch','DF-FIT0212','DFRobot','Capacitieve switch voor maximum niveaudetectie','sensor',NULL),(3,'flowmeter','YF-S201','Otronic','Flowmeter, meet de hoeveelheid water dat werd bijgevuld','sensor','liter'),(4,'elektroventiel','ADA-997','Adafruit','magneetventiel die waterstroom in- of uitschakeld','actuator',NULL);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek`
--

DROP TABLE IF EXISTS `historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datum` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `waarde` float NOT NULL,
  `commentaar` varchar(255) DEFAULT NULL,
  `deviceid` int NOT NULL,
  `actieid` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_historiek_device_idx` (`deviceid`),
  KEY `fk_historiek_actie1_idx` (`actieid`),
  CONSTRAINT `fk_historiek_actie1` FOREIGN KEY (`actieid`) REFERENCES `actie` (`actieid`),
  CONSTRAINT `fk_historiek_device` FOREIGN KEY (`deviceid`) REFERENCES `device` (`deviceid`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek`
--

LOCK TABLES `historiek` WRITE;
/*!40000 ALTER TABLE `historiek` DISABLE KEYS */;
INSERT INTO `historiek` VALUES (1,'2022-05-23 14:50:07',1111,'testdata',2,1),(2,'2022-05-24 14:50:07',4118,'testdata',2,1),(3,'2022-05-25 14:50:07',2262,'testdata',2,1),(4,'2022-05-26 14:50:07',1115,'testdata',3,1),(5,'2022-05-27 14:50:07',2713,'testdata',1,1),(6,'2022-05-28 14:50:07',988,'testdata',2,1),(7,'2022-05-29 14:50:07',2072,'testdata',2,1),(8,'2022-05-30 14:50:07',3022,'testdata',3,1),(9,'2022-05-31 14:50:07',4979,'testdata',1,1),(10,'2022-06-01 14:50:07',4056,'testdata',2,1),(11,'2022-06-02 14:50:07',2962,'testdata',2,1),(12,'2022-06-03 14:50:07',3114,'testdata',3,1),(13,'2022-06-04 14:50:07',4464,'testdata',2,1),(14,'2022-06-05 14:50:07',3119,'testdata',2,1),(15,'2022-06-06 14:50:07',3371,'testdata',2,1),(16,'2022-06-07 14:50:07',3434,'testdata',2,1),(17,'2022-06-08 14:50:07',3225,'testdata',1,1),(18,'2022-06-09 14:50:07',2759,'testdata',1,1),(19,'2022-06-10 14:50:07',611,'testdata',3,1),(20,'2022-06-11 14:50:07',4692,'testdata',1,1),(21,'2022-06-12 14:50:07',1598,'testdata',3,1),(22,'2022-06-13 14:50:07',2119,'testdata',2,1),(23,'2022-06-14 14:50:07',2024,'testdata',2,1),(24,'2022-06-15 14:50:07',4668,'testdata',2,1),(25,'2022-06-16 14:50:07',4040,'testdata',3,1),(26,'2022-06-17 14:50:07',3456,'testdata',2,1),(27,'2022-06-18 14:50:07',1936,'testdata',3,1),(28,'2022-06-19 14:50:07',3056,'testdata',2,1),(29,'2022-06-20 14:50:07',1966,'testdata',3,1),(30,'2022-06-21 14:50:07',3028,'testdata',1,1),(31,'2022-06-22 14:50:07',4921,'testdata',3,1),(32,'2022-06-23 14:50:07',1509,'testdata',3,1),(33,'2022-06-24 14:50:07',1364,'testdata',2,1),(34,'2022-06-25 14:50:07',4914,'testdata',3,1),(35,'2022-06-26 14:50:07',1090,'testdata',2,1),(36,'2022-06-27 14:50:07',2819,'testdata',2,1),(37,'2022-06-28 14:50:07',1390,'testdata',2,1),(38,'2022-06-29 14:50:07',3217,'testdata',2,1),(39,'2022-06-30 14:50:07',4980,'testdata',2,1),(40,'2022-07-01 14:50:07',2746,'testdata',3,1),(41,'2022-07-02 14:50:07',1242,'testdata',2,1),(42,'2022-07-03 14:50:07',4582,'testdata',2,1),(43,'2022-07-04 14:50:07',2971,'testdata',3,1),(44,'2022-07-05 14:50:07',2468,'testdata',2,1),(45,'2022-07-06 14:50:07',859,'testdata',2,1),(46,'2022-07-07 14:50:07',1526,'testdata',1,1),(47,'2022-07-08 14:50:07',1139,'testdata',2,1),(48,'2022-07-09 14:50:07',4604,'testdata',2,1),(49,'2022-07-10 14:50:07',3830,'testdata',3,1),(50,'2022-07-11 14:50:07',2525,'testdata',3,1),(51,'2022-07-12 14:50:07',1119,'testdata',1,1),(52,'2022-07-13 14:50:07',1862,'testdata',1,1),(53,'2022-07-14 14:50:07',2618,'testdata',1,1),(54,'2022-07-15 14:50:07',2055,'testdata',2,1),(55,'2022-07-16 14:50:07',4986,'testdata',1,1),(56,'2022-07-17 14:50:07',3973,'testdata',3,1),(57,'2022-07-18 14:50:07',2114,'testdata',1,1),(58,'2022-07-19 14:50:07',1719,'testdata',2,1),(59,'2022-07-20 14:50:07',2245,'testdata',2,1),(60,'2022-07-21 14:50:07',3125,'testdata',2,1),(61,'2022-07-22 14:50:07',1,'testdata',4,2),(62,'2022-07-23 14:50:07',0,'testdata',4,2),(63,'2022-07-24 14:50:07',1,'testdata',4,2),(64,'2022-07-25 14:50:07',0,'testdata',4,2),(65,'2022-07-26 14:50:07',1,'testdata',4,2);
/*!40000 ALTER TABLE `historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-23 17:20:31
