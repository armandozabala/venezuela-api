-- AlterTable
ALTER TABLE `City` ADD COLUMN `description` TEXT NULL,
    ADD COLUMN `population` INTEGER NULL,
    ADD COLUMN `postal_code` VARCHAR(191) NULL,
    ADD COLUMN `surface` DOUBLE NULL;

-- AlterTable
ALTER TABLE `State` ADD COLUMN `phone_prefix` VARCHAR(191) NULL,
    ADD COLUMN `population` INTEGER NULL,
    ADD COLUMN `region` VARCHAR(191) NULL,
    ADD COLUMN `surface` DOUBLE NULL;

-- CreateTable
CREATE TABLE `TouristAttraction` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,
    `description` TEXT NULL,
    `images` TEXT NULL,
    `state_id` INTEGER NULL,
    `city_id` INTEGER NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Airport` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,
    `iata_code` VARCHAR(191) NULL,
    `icao_code` VARCHAR(191) NULL,
    `state_id` INTEGER NULL,
    `city_id` INTEGER NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `President` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(191) NOT NULL,
    `description` TEXT NULL,
    `start_date` DATETIME(3) NULL,
    `end_date` DATETIME(3) NULL,
    `state_id` INTEGER NULL,

    PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey
ALTER TABLE `TouristAttraction` ADD CONSTRAINT `TouristAttraction_state_id_fkey` FOREIGN KEY (`state_id`) REFERENCES `State`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `TouristAttraction` ADD CONSTRAINT `TouristAttraction_city_id_fkey` FOREIGN KEY (`city_id`) REFERENCES `City`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Airport` ADD CONSTRAINT `Airport_state_id_fkey` FOREIGN KEY (`state_id`) REFERENCES `State`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Airport` ADD CONSTRAINT `Airport_city_id_fkey` FOREIGN KEY (`city_id`) REFERENCES `City`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `President` ADD CONSTRAINT `President_state_id_fkey` FOREIGN KEY (`state_id`) REFERENCES `State`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
