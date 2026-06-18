from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `password` VARCHAR(128) NOT NULL,
                `last_login` DATETIME NULL,
                `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
                `username` VARCHAR(50) NOT NULL UNIQUE,
                `first_name` VARCHAR(100) NULL,
                `email` VARCHAR(100) NULL UNIQUE,
                `is_organizer` TINYINT(1) NOT NULL DEFAULT 0,
                `created_at` DATETIME NOT NULL,
                `is_admin` TINYINT(1) NOT NULL DEFAULT 0,
                `is_staff` TINYINT(1) NOT NULL DEFAULT 0
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `users_groups` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `users_id` INT NOT NULL,
                `group_id` INT NOT NULL,
                FOREIGN KEY (`users_id`) REFERENCES `users`(`id`),
                FOREIGN KEY (`group_id`) REFERENCES `auth_group`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `users_user_permissions` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `users_id` INT NOT NULL,
                `permission_id` INT NOT NULL,
                FOREIGN KEY (`users_id`) REFERENCES `users`(`id`),
                FOREIGN KEY (`permission_id`) REFERENCES `auth_permission`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `profiles` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL UNIQUE,
                `rating` FLOAT NOT NULL DEFAULT 0,
                `games_created` INT NOT NULL DEFAULT 0,
                `games_completed` INT NOT NULL DEFAULT 0,
                `is_trusted` TINYINT(1) NOT NULL DEFAULT 0,
                `phone` VARCHAR(20) NULL,
                `avatar` VARCHAR(100) NULL,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `organizer_requests` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `name` VARCHAR(100) NOT NULL,
                `phone` VARCHAR(20) NOT NULL,
                `email` VARCHAR(254) NOT NULL,
                `message` TEXT NOT NULL,
                `status` VARCHAR(10) NOT NULL DEFAULT 'pending',
                `created_at` DATETIME NOT NULL,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `sportshall` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(255) NOT NULL,
                `address` VARCHAR(255) NOT NULL,
                `phone` VARCHAR(50) NULL,
                `price` INT NOT NULL DEFAULT 0
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `games` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `title` VARCHAR(255) NOT NULL,
                `game_date` DATE NOT NULL,
                `game_time` TIME NOT NULL,
                `location` VARCHAR(255) NOT NULL,
                `image` VARCHAR(100) NULL,
                `format` VARCHAR(50) NULL,
                `level` VARCHAR(50) NULL,
                `status` VARCHAR(50) NOT NULL DEFAULT 'active',
                `max_players` INT NOT NULL DEFAULT 12,
                `players_count` INT NOT NULL DEFAULT 0,
                `sportshall_id` INT NULL,
                `price` INT NOT NULL DEFAULT 0,
                `created_by_id` INT NOT NULL,
                `created_at` DATETIME NOT NULL,
                `notification_sent` TINYINT(1) NOT NULL DEFAULT 0,
                FOREIGN KEY (`sportshall_id`) REFERENCES `sportshall`(`id`),
                FOREIGN KEY (`created_by_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `game_participants` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `game_id` INT NOT NULL,
                `user_id` INT NOT NULL,
                `joined_at` DATETIME NOT NULL,
                FOREIGN KEY (`game_id`) REFERENCES `games`(`id`),
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `game_confirmations` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `game_id` INT NOT NULL,
                `user_id` INT NOT NULL,
                `confirmed_at` DATETIME NOT NULL,
                FOREIGN KEY (`game_id`) REFERENCES `games`(`id`),
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `products` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(100) NOT NULL,
                `brand` VARCHAR(50) NULL,
                `size` VARCHAR(20) NULL,
                `price` DECIMAL(10,2) NOT NULL,
                `description` TEXT NULL,
                `image` VARCHAR(255) NULL,
                `created_at` DATETIME NOT NULL
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `product_sizes` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `product_id` INT NOT NULL,
                `size` VARCHAR(10) NOT NULL,
                `quantity` INT NOT NULL DEFAULT 0,
                FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `rentals` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(255) NOT NULL,
                `price` DECIMAL(10,2) NOT NULL,
                `description` TEXT NULL,
                `is_available` TINYINT(1) NOT NULL DEFAULT 1,
                `image` VARCHAR(100) NULL,
                `quantity` INT NOT NULL DEFAULT 1
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `rental_sizes` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `rental_id` INT NOT NULL,
                `size` VARCHAR(20) NOT NULL,
                `quantity` INT UNSIGNED NOT NULL DEFAULT 0,
                FOREIGN KEY (`rental_id`) REFERENCES `rentals`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `user_rentals` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `item_id` INT NOT NULL,
                `size_id` INT NULL,
                `start_datetime` DATETIME NOT NULL,
                `end_datetime` DATETIME NOT NULL,
                `status` VARCHAR(20) NOT NULL DEFAULT 'booked',
                `created_at` DATETIME NOT NULL,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
                FOREIGN KEY (`item_id`) REFERENCES `rentals`(`id`),
                FOREIGN KEY (`size_id`) REFERENCES `rental_sizes`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `notifications` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `type` VARCHAR(50) NOT NULL,
                `text` TEXT NOT NULL,
                `link` VARCHAR(255) NULL,
                `is_read` TINYINT(1) NOT NULL DEFAULT 0,
                `created_at` DATETIME NOT NULL,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `cart_items` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `product_id` INT NOT NULL,
                `quantity` INT NOT NULL DEFAULT 1,
                `selected_size` VARCHAR(10) NULL,
                FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `orders` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `pvz` VARCHAR(255) NOT NULL,
                `pickup_time` VARCHAR(255) NULL,
                `comment` TEXT NULL,
                `total_price` DECIMAL(10,2) NOT NULL,
                `status` VARCHAR(20) NOT NULL DEFAULT 'new',
                `created_at` DATETIME NOT NULL,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
        """),
        migrations.RunSQL("""
            CREATE TABLE IF NOT EXISTS `order_items` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `order_id` INT NOT NULL,
                `product_id` INT NOT NULL,
                `quantity` INT NOT NULL DEFAULT 1,
                `size` VARCHAR(10) NULL,
                `price` DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`),
                FOREIGN KEY (`product_id`) REFERENCES `products`(`id`)
            );
        """),
    ]
