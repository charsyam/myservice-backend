DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique id',
  `email` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'email',
  `password` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'password',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '회원 상태값',
  `registered_at` datetime DEFAULT NULL COMMENT '가입일자',
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  UNIQUE KEY `idx_email` (`email`),
  KEY `idx_registered_at` (`registered_at`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='계정';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `public_key` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'public_key',
  `private_key` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'private_key',
  `encrypt_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'private_key',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '회원 상태값',
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='공개키';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shorturls`
--

DROP TABLE IF EXISTS `shorturls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shorturls` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique id',
  `user_id` bigint NOT NULL,
  `user_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user uid',
  `source` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'access_token',
  `shorturl` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'refresh_token',
  `shard_id` int DEFAULT NULL COMMENT `logical_shard_id`,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '회원상태값',
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  UNIQUE KEY `idx_shorturl` (`shorturl`),
  KEY `idx_source` (`source`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='shorturls';
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `sharded_shorturls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sharded_shorturls` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique id',
  `user_id` bigint NOT NULL,
  `user_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user uid',
  `source` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'access_token',
  `shorturl` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'refresh_token',
  `shard_id` int DEFAULT NULL COMMENT `logical_shard_id`,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '회원상태값',
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  UNIQUE KEY `idx_shorturl` (`shorturl`),
  KEY `idx_source` (`source`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='sharded_shorturls';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tokens` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique id',
  `user_id` bigint NOT NULL,
  `user_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'user uid',
  `access_token` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'access_token',
  `refresh_token` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'refresh_token',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '회원상태값',
  `access_token_expired_at` datetime DEFAULT NULL COMMENT '액세스토큰만료일자',
  `refresh_token_expired_at` datetime DEFAULT NULL COMMENT '리프레시토큰만료일자',
  `request_ip` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ip',
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  UNIQUE KEY `idx_access_token` (`access_token`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='token';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visit_history`
--

DROP TABLE IF EXISTS `visit_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visit_history` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'index id',
  `uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'unique id',
  `shorturl_id` bigint NOT NULL,
  `shorturl_uid` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `request_ip` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ip',
  `agent` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'agent',
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime DEFAULT NULL COMMENT '생성일자',
  `updated_at` datetime DEFAULT NULL COMMENT '수정일자',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uid` (`uid`),
  KEY `idx_shorturl_id` (`shorturl_id`),
  KEY `idx_shorturl_uid` (`shorturl_uid`),
  KEY `idx_createdat` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='visit_history';
