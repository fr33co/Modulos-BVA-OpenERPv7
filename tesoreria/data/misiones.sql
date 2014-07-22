-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.1.73-1


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema ima
--

CREATE DATABASE IF NOT EXISTS ima;
USE ima;

--
-- Definition of table `ima`.`dt_nom_misiones`
--

DROP TABLE IF EXISTS `ima`.`dt_nom_misiones`;
CREATE TABLE  `ima`.`dt_nom_misiones` (
  `id_misiones` int(11) NOT NULL,
  `nombre_mision` text NOT NULL,
  PRIMARY KEY (`id_misiones`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ima`.`dt_nom_misiones`
--

/*!40000 ALTER TABLE `dt_nom_misiones` DISABLE KEYS */;
LOCK TABLES `dt_nom_misiones` WRITE;
INSERT INTO `ima`.`dt_nom_misiones` VALUES  (42,'Zamora'),
 (41,'Barrio Adentro'),
 (40,'Sucre'),
 (39,'Árbol'),
 (38,'Sonrisa'),
 (37,'Alimentación'),
 (36,'Robinson II'),
 (35,'(13 de Abril)'),
 (34,'Robinson I'),
 (33,'Transporte'),
 (32,'Ribas'),
 (31,'Nevado'),
 (30,'Revolución Energética'),
 (29,'Negro Primero'),
 (28,'Piar'),
 (27,'Madres del Barrio'),
 (26,'Niños y Niñas del Barrio'),
 (25,'Jóvenes de la Patria'),
 (24,'Niño Jesús'),
 (23,'Eléctrica Venezuela'),
 (22,'Negra Hipólita'),
 (21,'Eficiencia o Nada'),
 (20,'Música'),
 (19,'Barrio Nuevo, Barrio Tricolor'),
 (18,'Miranda'),
 (17,'Barrio Adentro Deportivo'),
 (16,'Milagro'),
 (15,'Alma Mater'),
 (14,'José Gregorio Hernández'),
 (13,'Vivienda Venezuela'),
 (12,'Identidad'),
 (11,'Saber y Trabajo'),
 (10,'Guaicaipuro'),
 (9,'Hijos e Hijas de Venezuela'),
 (8,'Cultura'),
 (7,'En Amor Mayor'),
 (6,'Cristo'),
 (5,'A Toda Vida Venezuela'),
 (4,'Ciencia'),
 (3,'AgroVenezuela'),
 (2,'Che Guevara'),
 (1,'Fiesta del Asfalto');
UNLOCK TABLES;
/*!40000 ALTER TABLE `dt_nom_misiones` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
