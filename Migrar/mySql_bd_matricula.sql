-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.21-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para bd_matricula
CREATE DATABASE IF NOT EXISTS `bd_matricula` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `bd_matricula`;

-- Volcando estructura para tabla bd_matricula.curso
CREATE TABLE IF NOT EXISTS `curso` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `credito` int(11) NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla bd_matricula.curso: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` (`codigo`, `nombre`, `credito`) VALUES
	('ISA304', 'Fisica', 3),
	('ISA803', 'Computación en la nube', 3),
	('ISAE03', 'Administración de Redes', 3);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;

-- Volcando estructura para tabla bd_matricula.escuela
CREATE TABLE IF NOT EXISTS `escuela` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `duracion` int(11) NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla bd_matricula.escuela: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `escuela` DISABLE KEYS */;
INSERT INTO `escuela` (`codigo`, `nombre`, `duracion`) VALUES
	('ADMI', 'Administración Empresas', 10),
	('EAPIIS', 'Ingeniería Informatica y Sistemas', 10),
	('MINAS', 'Ingeniería de Minas', 10);
/*!40000 ALTER TABLE `escuela` ENABLE KEYS */;

-- Volcando estructura para tabla bd_matricula.estudiante
CREATE TABLE IF NOT EXISTS `estudiante` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DNI` int(11) NOT NULL,
  `apellidos` varchar(200) NOT NULL,
  `nombres` varchar(200) NOT NULL,
  `feNacimiento` varchar(30) NOT NULL,
  `sexo` varchar(1) NOT NULL,
  `codEscuela` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `codEscuela` (`codEscuela`),
  CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`codEscuela`) REFERENCES `escuela` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla bd_matricula.estudiante: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `estudiante` DISABLE KEYS */;
INSERT INTO `estudiante` (`id`, `DNI`, `apellidos`, `nombres`, `feNacimiento`, `sexo`, `codEscuela`) VALUES
	(1, 73658684, 'Pfuño Alccahuamani', 'Luis Albert', '24/10/2001', 'M', 'EAPIIS'),
	(3, 60078845, 'Molina ', 'Oscar', '10/08/2000', 'M', 'MINAS'),
	(5, 70085397, 'Ñahui Vargas', 'Edizon', '03/09/2001', 'M', 'ADMI');
/*!40000 ALTER TABLE `estudiante` ENABLE KEYS */;

-- Volcando estructura para tabla bd_matricula.matricula
CREATE TABLE IF NOT EXISTS `matricula` (
  `codigo` int(11) NOT NULL AUTO_INCREMENT,
  `codEstudiante` int(11) DEFAULT NULL,
  `codCurso` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codigo`),
  KEY `codEstudiante` (`codEstudiante`),
  KEY `codCurso` (`codCurso`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`codEstudiante`) REFERENCES `estudiante` (`id`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`codCurso`) REFERENCES `curso` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla bd_matricula.matricula: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `matricula` DISABLE KEYS */;
INSERT INTO `matricula` (`codigo`, `codEstudiante`, `codCurso`) VALUES
	(101, 1, 'ISA803'),
	(102, 5, 'ISA304');
/*!40000 ALTER TABLE `matricula` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
