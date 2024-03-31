-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: RuralConnect
-- ------------------------------------------------------
-- Server version	8.0.36-cluster

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
-- Table structure for table `book_service`
--

DROP TABLE IF EXISTS `book_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_service` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_number` varchar(45) NOT NULL,
  `service_id` varchar(45) NOT NULL,
  `service_booked` varchar(45) NOT NULL,
  `Amount_Payable` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `phonenumber` varchar(45) NOT NULL,
  `location` varchar(45) NOT NULL,
  `urgency` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_book_service_1_idx` (`service_booked`),
  KEY `fk_book_service_2_idx` (`id_number`),
  KEY `fk_book_service_3_idx` (`id_number`),
  KEY `fk_book_service_2_idx1` (`id_number`,`id`),
  KEY `fk_book_service_1_idx1` (`service_id`),
  KEY `index7` (`id_number`),
  CONSTRAINT `fk_book_service_1` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_service`
--

LOCK TABLES `book_service` WRITE;
/*!40000 ALTER TABLE `book_service` DISABLE KEYS */;
INSERT INTO `book_service` VALUES (35,'39016716','service010','Animal Veterinary',2000,'Billy Ochieng','billyochiengokello@gmail.com','0759815490','Nyamage - Kisii','very'),(36,'38854551','service010','Animal Veterinary',2000,'Billy Ochieng','billyochiengokello@gmail.com','0759815490','Nyamage - Kisii','very'),(39,'39016716','plumb002','Leakages repair',2000,'Billy Ochieng','billyochiengokello@gmail.com','0759815490','Kisumu','very'),(40,'39016716','saloon001','Wema Salonist',2000,'Frankline Onyango','frankonyi60@gmail.com','0759815490','Kisumu','very');
/*!40000 ALTER TABLE `book_service` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-25 14:59:54
