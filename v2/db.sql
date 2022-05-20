CREATE TABLE `room` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `capacity` smallint(6) NOT NULL,
  `start` timestamp DEFAULT '1970-01-01 00:00:00',
  `end` timestamp DEFAULT '1970-01-01 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4, AUTO_INCREMENT=1;