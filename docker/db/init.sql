CREATE DATABASE test;
USE test;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(200) NOT NULL,
  `password` varchar(100) NOT NULL,
  'email' varchar(200),
  'token' varchar(50)
);

DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
  `id` int UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `titulo` varchar(200) NOT NULL,
  `conteudo` varchar(100) NOT NULL,
  'link' varchar(200)
);