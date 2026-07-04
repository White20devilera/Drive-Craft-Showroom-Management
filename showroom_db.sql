-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 04, 2026 at 07:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `showroom_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `sales_history`
--

CREATE TABLE `sales_history` (
  `sale_id` int(11) NOT NULL,
  `customer_name` varchar(150) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `customer_nic` varchar(20) DEFAULT NULL,
  `vehicle_id` int(11) NOT NULL,
  `sale_date` date NOT NULL,
  `final_price` decimal(12,2) NOT NULL,
  `payment_mode` varchar(50) DEFAULT 'Cash'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales_history`
--

INSERT INTO `sales_history` (`sale_id`, `customer_name`, `customer_phone`, `customer_nic`, `vehicle_id`, `sale_date`, `final_price`, `payment_mode`) VALUES
(8, 'Kamal Perera', '0771234543', '200976589312', 87, '2026-07-04', 6500000.00, 'Leasing / Finance'),
(9, 'Kasun Athapaththu', '0723456543', '129786549V', 89, '2026-07-04', 12500000.00, 'Leasing / Finance'),
(10, 'Matheesha Ekanayaka', '0784564322', '199976547V', 90, '2026-07-04', 12500000.00, 'Cash'),
(11, 'Pubudu Susantha', '0772030342', '199856784V', 92, '2026-07-04', 9200000.00, 'Leasing / Finance'),
(12, 'Jordan Kent', '+94776543234', '200987658763', 97, '2026-07-04', 7200000.00, 'Cash');

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int(11) NOT NULL,
  `supplier_name` varchar(150) NOT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `country` varchar(50) DEFAULT 'Japan',
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `agent_commission` decimal(12,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `supplier_name`, `company_name`, `country`, `phone_number`, `email`, `agent_commission`) VALUES
(3, 'Mohamed Aslam', 'Assoc. Motorways (AMW)', 'Sri Lanka', '0117609609', 'aslam.m@amwmotors.com', 45000.00),
(4, 'Pradeep Perera', 'Elite Auto Imports', 'Japan', '+81355550192', 'pradeep.perera@elitejapan.jp', 75000.00),
(5, 'Nishantha Silva', 'Sinnatamby & Sons Auto', 'Sri Lanka', '0372224567', 'nsilva@sinnatamby.lk', 35000.00),
(6, 'Kenji Tanaka', 'SBT Japan Co.', 'Japan', '+81452901153', 'tanaka.k@sbtjapan.com', 60000.00),
(7, 'David Sterling', 'UK Premium Wheels LTD', 'United Kingdom', '+442079460192', 'd.sterling@ukpremiumwheels.co.uk', 90000.00),
(8, 'Chaminda Alwis', 'Alwis Auto Holdings', 'Sri Lanka', '0112345678', 'chaminda@alwisauto.lk', 40000.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `role` varchar(20) DEFAULT 'Admin',
  `status` varchar(20) DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `role`, `status`) VALUES
(2, 'admin2', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin', 'Active'),
(4, 'staff1', '10176e7b7b24d317acfcf8d2064cfd2f24e154f7b5a96603077d5ef813d6a6b6', 'Sales_Staff', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `vehicle_id` int(11) NOT NULL,
  `brand` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `manufacture_year` int(11) NOT NULL,
  `mileage` int(11) NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `status` varchar(20) DEFAULT 'Available',
  `image_path` varchar(255) DEFAULT 'no_image.png',
  `leather_seats` varchar(10) DEFAULT 'No',
  `sunroof` varchar(10) DEFAULT 'No',
  `push_start` varchar(10) DEFAULT 'No',
  `alloy_wheels` varchar(10) DEFAULT 'No',
  `reverse_camera` varchar(10) DEFAULT 'No',
  `fuel_type` varchar(50) DEFAULT 'N/A',
  `engine_cc` varchar(20) DEFAULT 'N/A',
  `transmission` varchar(50) DEFAULT 'N/A'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`vehicle_id`, `brand`, `model`, `manufacture_year`, `mileage`, `price`, `status`, `image_path`, `leather_seats`, `sunroof`, `push_start`, `alloy_wheels`, `reverse_camera`, `fuel_type`, `engine_cc`, `transmission`) VALUES
(87, 'Toyota', 'Vitz', 2018, 45000, 6500000.00, 'Sold', 'cars/toyota_vitz_2018_1783178616737.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Petrol', '', 'Automatic'),
(88, 'Toyota', 'Vitz', 2018, 45000, 6.00, 'Available', 'cars/toyota_vitz_2018_1783178616737.jpg', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Petrol', '1500', 'Automatic'),
(89, 'Honda', 'Civic', 2020, 25000, 12500000.00, 'Sold', 'cars/honda_civic_2020.png', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(90, 'Honda', 'Civic', 2020, 25000, 12500000.00, 'Sold', 'cars/honda_civic_2020.png', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(91, 'Honda', 'Civic', 2020, 25000, 12500000.00, 'Available', 'cars/honda_civic_2020.png', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(92, 'Suzuki', 'WagonR', 2017, 60000, 4800000.00, 'Sold', 'cars/suzuki_wagonr_2017.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Petrol', '1500', 'Automatic'),
(93, 'Suzuki', 'WagonR', 2017, 60000, 4800000.00, 'Available', 'cars/suzuki_wagonr_2017.jpg', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Petrol', '1500', 'Automatic'),
(94, 'Toyota', 'Aqua', 2015, 85000, 5800000.00, 'Available', 'cars/2017-2021_toyota_aqua.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(95, 'Toyota', 'Prius', 2016, 92000, 7200000.00, 'Available', 'cars/2016_toyota_prius.png', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(96, 'Toyota', 'Prius', 2016, 92000, 7200000.00, 'Available', 'cars/2016_toyota_prius.png', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(97, 'Toyota', 'Prius', 2016, 92000, 7200000.00, 'Sold', 'cars/2016_toyota_prius.png', 'Yes', 'No', 'Yes', 'Yes', 'No', 'Hybrid', '1500', 'Automatic'),
(98, 'Toyota', 'Prius', 2014, 92000, 7.00, 'Available', 'cars/2016_toyota_prius.png', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Manual'),
(99, 'Toyota', 'CH-R', 2019, 38000, 9500000.00, 'Available', 'cars/toyota_c-hr-2019_main.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Manual'),
(100, 'Toyota', 'CH-R', 2019, 38000, 9500000.00, 'Available', 'cars/toyota_c-hr-2019_main.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Manual'),
(101, 'Honda', 'CR-V', 2019, 82000, 6500000.00, 'Available', 'cars/honda_cr-v_2019.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(102, 'Honda', 'CR-V', 2019, 82000, 6500000.00, 'Available', 'cars/honda_cr-v_2019.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic'),
(103, 'Honda', 'CR-V', 2019, 82000, 6500000.00, 'Available', 'cars/honda_cr-v_2019.jpg', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Hybrid', '1500', 'Automatic');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sales_history`
--
ALTER TABLE `sales_history`
  ADD PRIMARY KEY (`sale_id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`vehicle_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sales_history`
--
ALTER TABLE `sales_history`
  MODIFY `sale_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=104;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sales_history`
--
ALTER TABLE `sales_history`
  ADD CONSTRAINT `sales_history_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
