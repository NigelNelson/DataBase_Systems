-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema video
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema video
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `video` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `video` ;

-- -----------------------------------------------------
-- Table `video`.`directors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`directors` (
  `name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`ratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`ratings` (
  `rating` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`rating`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_categories_new`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_categories_new` (
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_recordings_new`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_recordings_new` (
  `recording_id` INT NOT NULL,
  `director` VARCHAR(40) NULL DEFAULT NULL,
  `title` VARCHAR(40) NULL DEFAULT NULL,
  `category` VARCHAR(30) NULL DEFAULT NULL,
  `image_name` VARCHAR(40) NULL DEFAULT NULL,
  `duration` FLOAT NULL DEFAULT NULL,
  `rating` VARCHAR(10) NULL DEFAULT NULL,
  `year_released` FLOAT NULL DEFAULT NULL,
  `price` FLOAT NULL DEFAULT NULL,
  `stock_count` FLOAT(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`recording_id`),
  INDEX `rating` (`rating` ASC) VISIBLE,
  INDEX `director` (`director` ASC) VISIBLE,
  INDEX `category` (`category` ASC) VISIBLE,
  CONSTRAINT `video_recordings_new_ibfk_1`
    FOREIGN KEY (`rating`)
    REFERENCES `video`.`ratings` (`rating`),
  CONSTRAINT `video_recordings_new_ibfk_2`
    FOREIGN KEY (`director`)
    REFERENCES `video`.`directors` (`name`),
  CONSTRAINT `video_recordings_new_ibfk_3`
    FOREIGN KEY (`category`)
    REFERENCES `video`.`video_categories_new` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_actors_new`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_actors_new` (
  `name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`features`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`features` (
  `recording_id` INT NULL DEFAULT NULL,
  `actor_name` VARCHAR(40) NULL DEFAULT NULL,
  INDEX `recording_id` (`recording_id` ASC) VISIBLE,
  INDEX `actor_name` (`actor_name` ASC) VISIBLE,
  CONSTRAINT `features_ibfk_1`
    FOREIGN KEY (`recording_id`)
    REFERENCES `video`.`video_recordings_new` (`recording_id`),
  CONSTRAINT `features_ibfk_2`
    FOREIGN KEY (`actor_name`)
    REFERENCES `video`.`video_actors_new` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_categories` (
  `id` FLOAT NULL DEFAULT NULL,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_recordings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_recordings` (
  `recording_id` FLOAT NOT NULL,
  `director` VARCHAR(40) NULL DEFAULT NULL,
  `title` VARCHAR(40) NULL DEFAULT NULL,
  `category` VARCHAR(30) NULL DEFAULT NULL,
  `image_name` VARCHAR(40) NULL DEFAULT NULL,
  `duration` FLOAT NULL DEFAULT NULL,
  `rating` VARCHAR(10) NULL DEFAULT NULL,
  `year_released` FLOAT NULL DEFAULT NULL,
  `price` FLOAT NULL DEFAULT NULL,
  `stock_count` FLOAT(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`recording_id`),
  INDEX `category` (`category` ASC) VISIBLE,
  CONSTRAINT `video_recordings_ibfk_1`
    FOREIGN KEY (`category`)
    REFERENCES `video`.`video_categories` (`name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `video`.`video_actors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `video`.`video_actors` (
  `id` FLOAT NOT NULL,
  `name` VARCHAR(40) NULL DEFAULT NULL,
  `recording_id` FLOAT(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `recording_id` (`recording_id` ASC) VISIBLE,
  CONSTRAINT `video_actors_ibfk_1`
    FOREIGN KEY (`recording_id`)
    REFERENCES `video`.`video_recordings` (`recording_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
