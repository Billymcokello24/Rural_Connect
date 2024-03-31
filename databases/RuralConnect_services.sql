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
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `id` int NOT NULL AUTO_INCREMENT,
  `service_id` varchar(45) NOT NULL,
  `image` blob NOT NULL,
  `name` varchar(45) NOT NULL,
  `category` varchar(45) NOT NULL,
  `description` longtext NOT NULL,
  `Amount` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `phonenumber` varchar(45) NOT NULL,
  `location` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  PRIMARY KEY (`id`,`service_id`),
  KEY `fk_book_service_1_idx1` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (26,'service003',_binary 'templates/Pages/uploads/Ecoworld-Hexagons13.jpg','Tents for Hire','events and planning','We bring shade to your events','','in140005220@kisiiuniversity.ac.ke','0759815490','Kisii - Town','active'),(31,'service001',_binary 'templates/Pages/uploads/w1.png','Billy Ochieng','Education','retd','','billyochiengokello@gmail.com','0759815490','Nyamage - Kisii','active'),(32,'service010',_binary 'templates/Pages/uploads/V3.jpeg','Animal Veterinary','Health','Your Pet Companion','Kshs. 2000','billyochiengo@gmail.com','0759815490','Nyamage - Kisii','active'),(33,'plumb002',_binary 'templates/Pages/uploads/p2.jpeg','Leakages Repair','Plumbing','The best plumber in town','2000.0','in140004120@kisiiuniversity.ac.ke','0759815490','Kisumu','active'),(34,'saloon001',_binary 'templates/Pages/uploads/B2.jpeg','Wema Salonist','Beauty and Saloon','we offer good services','2000.0','billyochiengokello@gmail.com','0759815490','Kisumu','active'),(35,'saloon010',_binary 'templates/Pages/uploads/B3.jpeg','Mama Wendy Saloon','Beauty and Saloon','we are the definition of beauty','2000.0','in140005220@kisiiuniversity.ac.ke','0759815490','Kisumu','active');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
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
