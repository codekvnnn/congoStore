CREATE DATABASE  IF NOT EXISTS `congo_schema` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `congo_schema`;
-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: congo_schema
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.22.04.1

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
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `isPaid` varchar(10) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_carts_users1_idx` (`user_id`),
  CONSTRAINT `fk_carts_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` double DEFAULT NULL,
  `img_url` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_products_users_idx` (`user_id`),
  CONSTRAINT `fk_products_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (2,1,'sofa','A nice piece of living room furniture','furniture',2,800,'somepictureurl','2023-08-16 23:14:56','2023-08-17 00:20:56'),(4,1,'Plant api edit after review','Testing api edit. Defintitely not furniture','Garden, Housewares',44,20,'https://example.com/product-image.jpg','2023-08-17 02:21:28','2023-08-17 16:00:18'),(5,11,'Testy9000','Testing api create. Defintitely not furniture','Misc',1,29999.99,'https://example.com/product-image.jpg','2023-08-17 16:43:04','2023-08-17 16:43:04'),(6,11,'Testy9001','New model','Misc',1,59999.99,'https://example.com/product-image.jpg','2023-08-17 16:52:29','2023-08-17 16:52:29');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_in_carts`
--

DROP TABLE IF EXISTS `products_in_carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_in_carts` (
  `product_id` int NOT NULL,
  `cart_id` int NOT NULL,
  PRIMARY KEY (`product_id`,`cart_id`),
  KEY `fk_products_has_carts_carts1_idx` (`cart_id`),
  KEY `fk_products_has_carts_products1_idx` (`product_id`),
  CONSTRAINT `fk_products_has_carts_carts1` FOREIGN KEY (`cart_id`) REFERENCES `carts` (`id`),
  CONSTRAINT `fk_products_has_carts_products1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_in_carts`
--

LOCK TABLES `products_in_carts` WRITE;
/*!40000 ALTER TABLE `products_in_carts` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_in_carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `rating` varchar(5) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_users1_idx` (`user_id`),
  KEY `fk_reviews_products1_idx` (`product_id`),
  CONSTRAINT `fk_reviews_products1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `fk_reviews_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (3,1,4,'These plants are awesome!','*****','2023-08-17 15:59:29','2023-08-17 15:59:29'),(4,11,4,'This is the first API review','*****','2023-08-17 17:27:03','2023-08-17 17:27:03'),(8,11,4,'Another review for item 4','*****','2023-08-17 17:51:13','2023-08-17 17:51:13');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(72) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Michael','DeJac','92 Troupe St Buffalo, NY 14210','dejacm@gmail.com','$2b$12$RnzBUEz52XTeA7zOQTDt1O2Ns3h8aC.XPDpGB9Las79PuDFLPLuhW','2023-08-16 20:00:00','2023-08-16 20:00:00'),(2,'Testy','McTesterson','123 Test St','testy@gmail.com','$2b$12$y8gdTudr7uLete.Nn1li1uVG/Rubz9z29Sy3IjJypqDCVvSeY4aZC','2023-08-16 20:39:32','2023-08-16 20:39:32'),(3,'Testy','McTesterson II','123 Test St','testy2@gmail.com','$2b$12$heeIkpy4.s.VFyhC3py5JetIjn0afpFZtKXlT8dbdLbqlBws2qFCK','2023-08-16 20:47:20','2023-08-17 03:38:50'),(4,'Testy','McTesterson III','123 Test St','testy3@gmail.com','$2b$12$ueLP/Qx9OUkEWbDWPOev5O0E985RSI2XV0yXOQjEUX6l/iG3GjKta','2023-08-16 20:50:16','2023-08-16 20:50:16'),(5,'Gary','Busey','123 Point Break Ave','gbusey@gmail.com','$2b$12$MCRrMTIxx3odapl5UEKi0u/XGg3DIns646mTXa05kKGlBsXduSFXm','2023-08-17 02:31:29','2023-08-17 02:31:29'),(6,'Testy','McTesterson IV','123 Point Break Ave','testy4@gmail.com','$2b$12$zwxPDYF0sSeQ6oIq6OXAMu6/J1bRZzoBbmAP8RFb9qGx8RSDynjUq','2023-08-17 02:56:40','2023-08-17 02:56:40'),(7,'Testy','McTesterson V','123 Test St','testy5@gmail.com','$2b$12$hmVFdNoHA2gk7zQIshnFyevHrREmPSkxcls2wTP1EISLVB5I9jDve','2023-08-17 03:39:27','2023-08-17 03:39:27'),(8,'Testy','McTesterson VI','123 Test St','testy6@gmail.com','$2b$12$KKs7YdIXXbnT7yxTFZhgLen0M9RqbqWwvcQPpzUoy0fRsszkt/aLu','2023-08-17 03:41:48','2023-08-17 03:41:48'),(9,'Testy','McTesterson VII','123 Test St','testy7@gmail.com','$2b$12$pQcEViHT77Hk2.XyPmfHNeH0FfAVbaCJFiEa1/KN5KajjJkG8OFAS','2023-08-17 04:19:51','2023-08-17 04:19:51'),(10,'Testy','McTesterson VIII','123 Test St','testy8@gmail.com','$2b$12$nrDvemwPwxxmGzKsqcM3wuyVOHQXxxjcQq3/wBiU1WbOANKkT5CWW','2023-08-17 04:20:57','2023-08-17 04:20:57'),(11,'Testy','McTesterson VIIII','123 Test St','testy9@gmail.com','$2b$12$c7.wNZjr7e4kXRIgak/CoegVkNt7BADpGQZMl5rcMuW2Tdq//uU0q','2023-08-17 05:09:05','2023-08-17 05:09:05');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-17 21:30:24
