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
-- Table structure for table `received`
--

DROP TABLE IF EXISTS `received`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `received` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_number` varchar(45) NOT NULL,
  `service_id` varchar(45) NOT NULL,
  `Amount` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_received_1_idx` (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `received`
--

LOCK TABLES `received` WRITE;
/*!40000 ALTER TABLE `received` DISABLE KEYS */;
INSERT INTO `received` VALUES (2,'39016716','service010','2000'),(3,'39016716','service010','2000'),(4,'39016716','service010','2000'),(5,'39016716','service003','0'),(6,'39016716','service010','2000'),(7,'39016716','service010','2000'),(8,'39016716','service010','2000'),(9,'39016716','service010','2000'),(10,'39016716','service010','2000'),(11,'38854551','service010','2000'),(12,'38854551','service010','2000'),(13,'38854551','service010','2000'),(14,'38854551','service010','2000'),(15,'38854551','service010','2000'),(16,'38854551','service003','2000'),(17,'39016716','plumb002','2000'),(18,'39016716','service010','2000'),(19,'39016716','service010','2000'),(20,'39016716','service010','2000'),(21,'39016716','service010','2000'),(22,'39016716','service010','2000'),(23,'39016716','service010','2000'),(24,'39016716','service010','2000'),(25,'39016716','service010','2000'),(26,'39016716','service010','2000'),(27,'39016716','service010','2000'),(28,'39016716','service010','2000'),(29,'39016716','saloon001','2000'),(30,'39016716','service010','2000');
/*!40000 ALTER TABLE `received` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-25 14:59:53
