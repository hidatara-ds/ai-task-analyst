-- =================================================================
-- SKEMA TABEL DATABASE
-- =================================================================

-- Hapus tabel jika sudah ada untuk eksekusi ulang (opsional)
DROP TABLE IF EXISTS user_task;
DROP TABLE IF EXISTS activity;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS user;

-- Tabel untuk menyimpan data pengguna
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  nama TEXT NOT NULL
);

-- Tabel untuk menyimpan data tugas/proyek utama
CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY,
  task TEXT NOT NULL,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL
);

-- Tabel untuk menyimpan detail aktivitas di dalam setiap tugas
CREATE TABLE IF NOT EXISTS activity (
  id INTEGER PRIMARY KEY,
  activity TEXT NOT NULL,
  task_id INTEGER NOT NULL,
  start_date TEXT NOT NULL,
  end_date TEXT NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (task_id) REFERENCES task(id)
);

-- Tabel penghubung untuk menugaskan tugas kepada pengguna
CREATE TABLE IF NOT EXISTS user_task (
  user_id INTEGER NOT NULL,
  task_id INTEGER NOT NULL,
  PRIMARY KEY (user_id, task_id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (task_id) REFERENCES task(id)
);


-- =================================================================
-- DATA PENGGUNA (USER) - 15 Karyawan
-- =================================================================
INSERT INTO user (id, nama) VALUES (1, 'Andi - Project Manager');
INSERT INTO user (id, nama) VALUES (2, 'Siti - Sr. Backend Dev');
INSERT INTO user (id, nama) VALUES (3, 'Budi - Sr. Frontend Dev');
INSERT INTO user (id, nama) VALUES (4, 'Toni - UI/UX Designer');
INSERT INTO user (id, nama) VALUES (5, 'Faizal - QA Engineer');
INSERT INTO user (id, nama) VALUES (6, 'Rina - Jr. Backend Dev');
INSERT INTO user (id, nama) VALUES (7, 'Dian - Jr. Frontend Dev');
INSERT INTO user (id, nama) VALUES (8, 'Iqbal - DevOps Engineer');
INSERT INTO user (id, nama) VALUES (9, 'Maya - Business Analyst');
INSERT INTO user (id, nama) VALUES (10, 'Santo - Mobile Dev (Android)');
INSERT INTO user (id, nama) VALUES (11, 'Cindy - Mobile Dev (iOS)');
INSERT INTO user (id, nama) VALUES (12, 'Gilang - QA Automation');
INSERT INTO user (id, nama) VALUES (13, 'Hesti - Technical Writer');
INSERT INTO user (id, nama) VALUES (14, 'Joko - Database Admin');
INSERT INTO user (id, nama) VALUES (15, 'Lina - UI/UX Researcher');


-- =================================================================
-- DATA TUGAS (TASK) - Proyek Tahunan 2024 - 2025
-- =================================================================
-- Proyek 2024
INSERT INTO task (id, task, start_date, end_date) VALUES (1, 'E-commerce Platform - Client Alpha', '2024-01-15', '2024-06-28');
INSERT INTO task (id, task, start_date, end_date) VALUES (2, 'Company Profile Website - Client Beta', '2024-02-05', '2024-04-26');
INSERT INTO task (id, task, start_date, end_date) VALUES (3, 'Mobile Banking App - Client Gamma', '2024-04-08', '2024-09-27');
INSERT INTO task (id, task, start_date, end_date) VALUES (4, 'Upgrade Sistem CRM Internal', '2024-05-20', '2024-08-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (5, 'Sistem Manajemen Logistik - Client Delta', '2024-07-22', '2024-12-20');
INSERT INTO task (id, task, start_date, end_date) VALUES (6, 'Pengembangan API Gateway Internal', '2024-08-05', '2024-11-22');
INSERT INTO task (id, task, start_date, end_date) VALUES (7, 'Server Maintenance & Security Audit Q1-Q2 2024', '2024-01-01', '2024-06-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (8, 'Server Maintenance & Security Audit Q3-Q4 2024', '2024-07-01', '2024-12-31');
-- [BARU] Proyek tambahan untuk memperpadat jadwal 2024
INSERT INTO task (id, task, start_date, end_date) VALUES (9, 'Mobile App Feature Enhancement - Client Gamma', '2024-10-07', '2024-12-13');

-- Proyek 2025
INSERT INTO task (id, task, start_date, end_date) VALUES (10, 'Data Analytics Dashboard - Client Epsilon', '2025-01-20', '2025-06-27');
INSERT INTO task (id, task, start_date, end_date) VALUES (11, 'Website Revamp - Client Zeta', '2025-02-10', '2025-05-16');
INSERT INTO task (id, task, start_date, end_date) VALUES (12, 'Internal Knowledge Base System', '2025-04-07', '2025-06-20');
-- [BARU] Proyek tambahan untuk memperpadat jadwal 2025
INSERT INTO task (id, task, start_date, end_date) VALUES (13, 'CI/CD Pipeline Optimization Internal', '2025-01-13', '2025-03-21');
INSERT INTO task (id, task, start_date, end_date) VALUES (14, 'ERP System Integration - Client Theta', '2025-07-14', '2025-12-19');
INSERT INTO task (id, task, start_date, end_date) VALUES (15, 'Server Maintenance & Security Audit Q1-Q2 2025', '2025-01-01', '2025-06-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (16, 'Server Maintenance & Security Audit Q3-Q4 2025', '2025-07-01', '2025-12-31');


-- =================================================================
-- DATA AKTIVITAS (ACTIVITY) - Detail untuk setiap proyek
-- =================================================================
-- --- Aktivitas Proyek 1: E-commerce Platform ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (1, 'Requirement Gathering & Analysis', 1, '2024-01-15', '2024-01-26', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (2, 'UI/UX Research & Wireframing', 1, '2024-01-29', '2024-02-16', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (3, 'High-Fidelity Design & Prototyping', 1, '2024-02-19', '2024-03-08', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (4, 'Backend: User & Auth Module', 1, '2024-03-11', '2024-04-05', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (5, 'Backend: Product & Order Module', 1, '2024-04-08', '2024-05-03', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (6, 'Frontend: UI Component Implementation', 1, '2024-04-08', '2024-05-10', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (7, 'Integration & Payment Gateway Setup', 1, '2024-05-06', '2024-05-24', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (8, 'System Integration Testing (SIT)', 1, '2024-05-27', '2024-06-07', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (9, 'User Acceptance Testing (UAT)', 1, '2024-06-10', '2024-06-21', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (10, 'Deployment & Go-Live', 1, '2024-06-24', '2024-06-28', 'completed');

-- --- Aktivitas Proyek 3: Mobile Banking App ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (11, 'Kick-off & Workshop dengan Client', 3, '2024-04-08', '2024-04-12', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (12, 'Analisis Kebutuhan & Regulasi Finansial', 3, '2024-04-15', '2024-05-03', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (13, 'Security Design & Threat Modeling', 3, '2024-05-06', '2024-05-24', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (14, 'Core Banking API Integration Plan', 3, '2024-05-27', '2024-06-14', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (15, 'Android: Development Sprint 1', 3, '2024-06-17', '2024-07-12', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (16, 'iOS: Development Sprint 1', 3, '2024-06-17', '2024-07-12', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (17, 'QA: Test Case & Scenario Planning', 3, '2024-06-17', '2024-07-05', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (18, 'Android: Development Sprint 2', 3, '2024-07-15', '2024-08-09', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (19, 'iOS: Development Sprint 2', 3, '2024-07-15', '2024-08-09', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (20, 'Penetration Testing', 3, '2024-08-26', '2024-09-13', 'completed');

-- --- Aktivitas Proyek 5: Sistem Manajemen Logistik ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (21, 'Analisis Alur Kerja Logistik Klien', 5, '2024-07-22', '2024-08-09', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (22, 'Desain Arsitektur Sistem (Microservices)', 5, '2024-08-12', '2024-08-30', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (23, 'Backend: Warehouse & Inventory Service', 5, '2024-09-02', '2024-09-27', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (24, 'Backend: Shipment & Tracking Service', 5, '2024-09-30', '2024-10-25', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (25, 'Frontend: Dashboard Admin', 5, '2024-09-16', '2024-10-18', 'completed');

-- --- Aktivitas Tugas 8: Maintenance Q3-Q4 2024 ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (26, 'Patching OS & Software Juli', 8, '2024-07-01', '2024-07-05', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (27, 'Backup & Recovery Drill Q3', 8, '2024-08-19', '2024-08-23', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (28, 'Vulnerability Scanning Oktober', 8, '2024-10-07', '2024-10-11', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (29, 'Performance Review & Tuning Desember', 8, '2024-12-02', '2024-12-13', 'completed');

-- --- [BARU] Aktivitas Proyek 9: Mobile Feature Enhancement ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (30, 'Analisis & Perancangan Fitur Baru', 9, '2024-10-07', '2024-10-18', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (31, 'Pengembangan Modul Notifikasi & Transaksi', 9, '2024-10-21', '2024-11-22', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (32, 'Pengujian Regresi & Fitur Baru', 9, '2024-11-25', '2024-12-06', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (33, 'Rilis Bertahap ke Pengguna', 9, '2024-12-09', '2024-12-13', 'completed');

-- --- [BARU] Aktivitas Proyek 10: Data Analytics Dashboard ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (34, 'Requirement & Data Source Analysis', 10, '2025-01-20', '2025-01-31', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (35, 'Planning Data Source Integration', 10, '2025-02-03', '2025-02-21', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (36, 'Dashboard UI/UX Design', 10, '2025-02-24', '2025-03-14', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (37, 'Backend: Data Processing Pipeline', 10, '2025-03-17', '2025-04-25', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (38, 'Frontend: Data Visualization', 10, '2025-04-28', '2025-05-30', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (39, 'Final Testing & Deployment', 10, '2025-06-02', '2025-06-27', 'in_progress');

-- --- [BARU] Aktivitas Proyek 11: Website Revamp ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (40, 'UX Research & Content Strategy', 11, '2025-02-10', '2025-02-28', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (41, 'New Design Mockups & Prototype', 11, '2025-03-03', '2025-03-21', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (42, 'Frontend Development Phase', 11, '2025-03-24', '2025-04-25', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (43, 'CMS Integration & Content Entry', 11, '2025-04-28', '2025-05-09', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (44, 'Final Review & Go-Live', 11, '2025-05-12', '2025-05-16', 'completed');

-- --- [BARU] Aktivitas Proyek 13: CI/CD Pipeline Optimization ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (45, 'Audit Pipeline & Tools Saat Ini', 13, '2025-01-13', '2025-01-24', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (46, 'Implementasi Scripting & Automated Testing', 13, '2025-01-27', '2025-02-28', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (47, 'Integrasi ke Proyek Pilot', 13, '2025-03-03', '2025-03-14', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (48, 'Dokumentasi & Sosialisasi Alur Baru', 13, '2025-03-17', '2025-03-21', 'completed');

-- --- [BARU] Aktivitas Proyek 14: ERP System Integration ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (49, 'Kick-off & Business Process Mapping', 14, '2025-07-14', '2025-08-01', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (50, 'System Architecture Design', 14, '2025-08-04', '2025-08-22', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (51, 'Module Development: Keuangan', 14, '2025-08-25', '2025-09-26', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (52, 'Module Development: SDM', 14, '2025-09-29', '2025-10-31', 'pending');

-- --- [BARU] Aktivitas Tugas 15: Maintenance Q1-Q2 2025 ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (53, 'Patching OS & Software Januari', 15, '2025-01-06', '2025-01-10', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (54, 'Backup & Recovery Drill Q1', 15, '2025-03-17', '2025-03-21', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (55, 'Vulnerability Scanning April', 15, '2025-04-07', '2025-04-11', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (56, 'Performance Review & Tuning Juni', 15, '2025-06-02', '2025-06-06', 'completed');

-- --- [BARU] Aktivitas Tugas 16: Maintenance Q3-Q4 2025 ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (57, 'Patching OS & Software Juli', 16, '2025-07-07', '2025-07-11', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (58, 'Backup & Recovery Drill Q3', 16, '2025-08-18', '2025-08-22', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (59, 'Vulnerability Scanning Oktober', 16, '2025-10-06', '2025-10-10', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (60, 'Performance Review & Tuning Desember', 16, '2025-12-01', '2025-12-12', 'pending');


-- =================================================================
-- DATA PENUGASAN (User-Task Assignments)
-- =================================================================
-- Proyek 1: E-commerce
INSERT INTO user_task (user_id, task_id) VALUES (1, 1); INSERT INTO user_task (user_id, task_id) VALUES (9, 1); INSERT INTO user_task (user_id, task_id) VALUES (15, 1); INSERT INTO user_task (user_id, task_id) VALUES (4, 1); INSERT INTO user_task (user_id, task_id) VALUES (2, 1); INSERT INTO user_task (user_id, task_id) VALUES (6, 1); INSERT INTO user_task (user_id, task_id) VALUES (3, 1); INSERT INTO user_task (user_id, task_id) VALUES (7, 1); INSERT INTO user_task (user_id, task_id) VALUES (5, 1); INSERT INTO user_task (user_id, task_id) VALUES (12, 1); INSERT INTO user_task (user_id, task_id) VALUES (8, 1); INSERT INTO user_task (user_id, task_id) VALUES (13, 1); INSERT INTO user_task (user_id, task_id) VALUES (14, 1);

-- Proyek 2: Company Profile
INSERT INTO user_task (user_id, task_id) VALUES (1, 2); INSERT INTO user_task (user_id, task_id) VALUES (4, 2); INSERT INTO user_task (user_id, task_id) VALUES (7, 2); INSERT INTO user_task (user_id, task_id) VALUES (5, 2);

-- Proyek 3: Mobile Banking
INSERT INTO user_task (user_id, task_id) VALUES (1, 3); INSERT INTO user_task (user_id, task_id) VALUES (9, 3); INSERT INTO user_task (user_id, task_id) VALUES (2, 3); INSERT INTO user_task (user_id, task_id) VALUES (10, 3); INSERT INTO user_task (user_id, task_id) VALUES (11, 3); INSERT INTO user_task (user_id, task_id) VALUES (5, 3); INSERT INTO user_task (user_id, task_id) VALUES (8, 3); INSERT INTO user_task (user_id, task_id) VALUES (14, 3);

-- Proyek 4: CRM Internal
INSERT INTO user_task (user_id, task_id) VALUES (1, 4); INSERT INTO user_task (user_id, task_id) VALUES (2, 4); INSERT INTO user_task (user_id, task_id) VALUES (3, 4);

-- Proyek 5: Logistik
INSERT INTO user_task (user_id, task_id) VALUES (1, 5); INSERT INTO user_task (user_id, task_id) VALUES (9, 5); INSERT INTO user_task (user_id, task_id) VALUES (2, 5); INSERT INTO user_task (user_id, task_id) VALUES (3, 5);

-- Proyek 6: API Gateway
INSERT INTO user_task (user_id, task_id) VALUES (1, 6); INSERT INTO user_task (user_id, task_id) VALUES (2, 6); INSERT INTO user_task (user_id, task_id) VALUES (8, 6);

-- Maintenance 2024
INSERT INTO user_task (user_id, task_id) VALUES (8, 7); INSERT INTO user_task (user_id, task_id) VALUES (14, 7); INSERT INTO user_task (user_id, task_id) VALUES (8, 8); INSERT INTO user_task (user_id, task_id) VALUES (14, 8);

-- [BARU] Proyek 9: Mobile Feature Enhancement
INSERT INTO user_task (user_id, task_id) VALUES (1, 9); INSERT INTO user_task (user_id, task_id) VALUES (10, 9); INSERT INTO user_task (user_id, task_id) VALUES (11, 9); INSERT INTO user_task (user_id, task_id) VALUES (5, 9);

-- [BARU] Proyek 10: Analytics Dashboard
INSERT INTO user_task (user_id, task_id) VALUES (1, 10); INSERT INTO user_task (user_id, task_id) VALUES (9, 10); INSERT INTO user_task (user_id, task_id) VALUES (2, 10); INSERT INTO user_task (user_id, task_id) VALUES (6, 10); INSERT INTO user_task (user_id, task_id) VALUES (3, 10); INSERT INTO user_task (user_id, task_id) VALUES (14, 10); INSERT INTO user_task (user_id, task_id) VALUES (5, 10);

-- [BARU] Proyek 11: Website Revamp
INSERT INTO user_task (user_id, task_id) VALUES (1, 11); INSERT INTO user_task (user_id, task_id) VALUES (15, 11); INSERT INTO user_task (user_id, task_id) VALUES (4, 11); INSERT INTO user_task (user_id, task_id) VALUES (7, 11);

-- [BARU] Proyek 12: Knowledge Base
INSERT INTO user_task (user_id, task_id) VALUES (1, 12); INSERT INTO user_task (user_id, task_id) VALUES (13, 12); INSERT INTO user_task (user_id, task_id) VALUES (6, 12); INSERT INTO user_task (user_id, task_id) VALUES (7, 12);

-- [BARU] Proyek 13: CI/CD Optimization
INSERT INTO user_task (user_id, task_id) VALUES (8, 13); INSERT INTO user_task (user_id, task_id) VALUES (2, 13); INSERT INTO user_task (user_id, task_id) VALUES (3, 13); INSERT INTO user_task (user_id, task_id) VALUES (12, 13);

-- [BARU] Proyek 14: ERP System
INSERT INTO user_task (user_id, task_id) VALUES (1, 14); INSERT INTO user_task (user_id, task_id) VALUES (9, 14); INSERT INTO user_task (user_id, task_id) VALUES (2, 14); INSERT INTO user_task (user_id, task_id) VALUES (3, 14); INSERT INTO user_task (user_id, task_id) VALUES (5, 14); INSERT INTO user_task (user_id, task_id) VALUES (8, 14); INSERT INTO user_task (user_id, task_id) VALUES (13, 14); INSERT INTO user_task (user_id, task_id) VALUES (14, 14);

-- [BARU] Maintenance 2025
INSERT INTO user_task (user_id, task_id) VALUES (8, 15); INSERT INTO user_task (user_id, task_id) VALUES (14, 15);
INSERT INTO user_task (user_id, task_id) VALUES (8, 16); INSERT INTO user_task (user_id, task_id) VALUES (14, 16);