-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `follower_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test@test.com','test',0,'2025-11-10 15:44:51'),(2,'lily','lily@test.com','lily',152,'2025-11-10 15:53:38'),(3,'tina','tina@test.com','tina',421,'2025-11-10 15:56:54'),(4,'justin','justin@test.com','justin',167,'2025-11-10 15:58:51'),(5,'bob','bob@test.com','bob',75,'2025-11-10 15:59:35'),(7,'Jennie','Jennie@test.com','Jennie',0,'2025-11-18 20:55:48'),(8,'Kelly','Kelly@test.com','Kelly',0,'2025-11-20 11:18:31'),(9,'文歆','hunn@test.com','hunn',0,'2025-11-20 14:15:08'),(10,'Ben','ben@test.com','ben',0,'2025-11-20 14:27:35'),(11,'John','John@test.com','John',0,'2025-11-21 17:58:30');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int unsigned NOT NULL,
  `content` text NOT NULL,
  `like_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,2,'Hi~  大家好嗎?',63,'2025-11-11 12:48:25'),(3,4,'Hello! 今天天氣真的很好呢!!',75,'2025-11-11 12:50:56'),(4,1,'今天天氣雖然還不錯，但風很強啊!',45,'2025-11-11 13:33:14'),(5,1,'而且也看不到藍藍的天空，都被雲給覆蓋了',245,'2025-11-11 13:34:06'),(6,4,'沒錯~ 但這樣也不會太曬或是太熱，也不錯啦!! 哈哈哈',145,'2025-11-11 13:35:01'),(12,7,'大家好啊~ 我是Jennie',0,'2025-11-19 22:21:33'),(13,1,'Hi Hi~ Jennie，我是test2 哈哈',0,'2025-11-19 22:58:58'),(16,7,'你好~  test2',0,'2025-11-20 12:24:21'),(17,7,'今天天氣很好呢~',0,'2025-11-20 12:33:33'),(19,7,'而且太陽也很大~ 讚讚',0,'2025-11-20 13:57:11'),(24,2,'大家好~ Jennie也來了!!!',0,'2025-11-20 14:13:49'),(26,9,'Hello! 我是文歆，今天天氣很舒服',0,'2025-11-20 14:16:30'),(27,9,'而且很適合睡覺XDD',0,'2025-11-20 14:17:19'),(28,2,'對啊!!',0,'2025-11-20 14:26:59'),(31,8,'各位好~ 我是Kelly',0,'2025-11-21 15:41:05'),(32,11,'Hello~ 大家好呀!!',0,'2025-11-21 18:01:50');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search`
--

DROP TABLE IF EXISTS `search`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `be_queried_id` int unsigned NOT NULL,
  `query_id` int unsigned NOT NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `be_queried_id` (`be_queried_id`),
  KEY `query_id` (`query_id`),
  CONSTRAINT `search_ibfk_1` FOREIGN KEY (`be_queried_id`) REFERENCES `member` (`id`),
  CONSTRAINT `search_ibfk_2` FOREIGN KEY (`query_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search`
--

LOCK TABLES `search` WRITE;
/*!40000 ALTER TABLE `search` DISABLE KEYS */;
INSERT INTO `search` VALUES (1,5,8,'2025-11-26 17:55:55'),(3,8,1,'2025-11-26 21:05:12'),(4,8,5,'2025-11-27 11:25:51'),(5,8,7,'2025-11-27 11:26:13'),(6,8,1,'2025-11-27 12:09:23'),(7,8,3,'2025-11-27 12:09:42'),(8,8,3,'2025-11-27 12:09:49'),(9,8,2,'2025-11-27 12:10:35'),(10,8,5,'2025-11-27 12:11:21'),(11,8,5,'2025-11-27 12:11:32'),(12,8,4,'2025-11-27 12:11:48'),(13,8,4,'2025-11-27 12:11:55'),(14,8,7,'2025-11-27 12:13:36'),(15,9,7,'2025-11-27 12:13:39'),(16,8,9,'2025-11-27 12:14:01'),(17,8,1,'2025-11-27 12:15:51');
/*!40000 ALTER TABLE `search` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 12:25:30
