-- =================================================================
-- SKEMA TABEL DATABASE (Struktur tidak diubah sesuai permintaan)
-- =================================================================

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
-- DATA TUGAS (TASK) - Proyek Tahunan 2024
-- =================================================================
-- Proyek Q1-Q2
INSERT INTO task (id, task, start_date, end_date) VALUES (1, 'E-commerce Platform - Client Alpha', '2024-01-15', '2024-06-28');
INSERT INTO task (id, task, start_date, end_date) VALUES (2, 'Company Profile Website - Client Beta', '2024-02-05', '2024-04-26');

-- Proyek Q2-Q3
INSERT INTO task (id, task, start_date, end_date) VALUES (3, 'Mobile Banking App - Client Gamma', '2024-04-08', '2024-09-27');
INSERT INTO task (id, task, start_date, end_date) VALUES (4, 'Upgrade Sistem CRM Internal', '2024-05-20', '2024-08-30');

-- Proyek Q3-Q4
INSERT INTO task (id, task, start_date, end_date) VALUES (5, 'Sistem Manajemen Logistik - Client Delta', '2024-07-22', '2024-12-20');
INSERT INTO task (id, task, start_date, end_date) VALUES (6, 'Pengembangan API Gateway Internal', '2024-08-05', '2024-11-22');

-- Tugas Berkelanjutan (Maintenance)
INSERT INTO task (id, task, start_date, end_date) VALUES (7, 'Server Maintenance & Security Audit Q1-Q2', '2024-01-01', '2024-06-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (8, 'Server Maintenance & Security Audit Q3-Q4', '2024-07-01', '2024-12-31');


-- =================================================================
-- DATA AKTIVITAS (ACTIVITY) - Detail untuk setiap proyek
-- =================================================================
-- --- Aktivitas untuk Proyek 1: E-commerce Platform ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (1, 'Requirement Gathering & Analysis', 1, '2024-01-15', '2024-01-26', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (2, 'UI/UX Research & Wireframing', 1, '2024-01-29', '2024-02-16', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (3, 'High-Fidelity Design & Prototyping', 1, '2024-02-19', '2024-03-08', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (4, 'Backend: User & Auth Module', 1, '2024-03-11', '2024-04-05', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (5, 'Backend: Product & Order Module', 1, '2024-04-08', '2024-05-03', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (6, 'Frontend: UI Component Implementation', 1, '2024-04-08', '2024-05-10', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (7, 'Integration & Payment Gateway Setup', 1, '2024-05-06', '2024-05-24', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (8, 'System Integration Testing (SIT)', 1, '2024-05-27', '2024-06-07', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (9, 'User Acceptance Testing (UAT)', 1, '2024-06-10', '2024-06-21', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (10, 'Deployment & Go-Live', 1, '2024-06-24', '2024-06-28', 'pending');

-- --- Aktivitas untuk Proyek 3: Mobile Banking App ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (11, 'Kick-off & Workshop dengan Client', 3, '2024-04-08', '2024-04-12', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (12, 'Analisis Kebutuhan & Regulasi Finansial', 3, '2024-04-15', '2024-05-03', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (13, 'Security Design & Threat Modeling', 3, '2024-05-06', '2024-05-24', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (14, 'Core Banking API Integration Plan', 3, '2024-05-27', '2024-06-14', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (15, 'Android: Development Sprint 1', 3, '2024-06-17', '2024-07-12', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (16, 'iOS: Development Sprint 1', 3, '2024-06-17', '2024-07-12', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (17, 'QA: Test Case & Scenario Planning', 3, '2024-06-17', '2024-07-05', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (18, 'Android: Development Sprint 2', 3, '2024-07-15', '2024-08-09', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (19, 'iOS: Development Sprint 2', 3, '2024-07-15', '2024-08-09', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (20, 'Penetration Testing', 3, '2024-08-26', '2024-09-13', 'pending');

-- --- Aktivitas untuk Proyek 5: Sistem Manajemen Logistik ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (21, 'Analisis Alur Kerja Logistik Klien', 5, '2024-07-22', '2024-08-09', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (22, 'Desain Arsitektur Sistem (Microservices)', 5, '2024-08-12', '2024-08-30', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (23, 'Backend: Warehouse & Inventory Service', 5, '2024-09-02', '2024-09-27', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (24, 'Backend: Shipment & Tracking Service', 5, '2024-09-30', '2024-10-25', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (25, 'Frontend: Dashboard Admin', 5, '2024-09-16', '2024-10-18', 'pending');

-- --- Aktivitas untuk Tugas 8: Maintenance Q3-Q4 ---
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (26, 'Patching OS & Software Juli', 8, '2024-07-01', '2024-07-05', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (27, 'Backup & Recovery Drill Q3', 8, '2024-08-19', '2024-08-23', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (28, 'Vulnerability Scanning Oktober', 8, '2024-10-07', '2024-10-11', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (29, 'Performance Review & Tuning Desember', 8, '2024-12-02', '2024-12-13', 'pending');


-- =================================================================
-- DATA PENUGASAN (User-Task Assignments)
-- =================================================================
-- Proyek 1: E-commerce (Tim besar)
INSERT INTO user_task (user_id, task_id) VALUES (1, 1);  -- Andi (PM)
INSERT INTO user_task (user_id, task_id) VALUES (9, 1);  -- Maya (Business Analyst)
INSERT INTO user_task (user_id, task_id) VALUES (15, 1); -- Lina (UX Researcher)
INSERT INTO user_task (user_id, task_id) VALUES (4, 1);  -- Toni (UI/UX Designer)
INSERT INTO user_task (user_id, task_id) VALUES (2, 1);  -- Siti (Sr. Backend)
INSERT INTO user_task (user_id, task_id) VALUES (6, 1);  -- Rina (Jr. Backend)
INSERT INTO user_task (user_id, task_id) VALUES (3, 1);  -- Budi (Sr. Frontend)
INSERT INTO user_task (user_id, task_id) VALUES (7, 1);  -- Dian (Jr. Frontend)
INSERT INTO user_task (user_id, task_id) VALUES (5, 1);  -- Faizal (QA)
INSERT INTO user_task (user_id, task_id) VALUES (12, 1); -- Gilang (QA Automation)
INSERT INTO user_task (user_id, task_id) VALUES (8, 1);  -- Iqbal (DevOps)
INSERT INTO user_task (user_id, task_id) VALUES (13, 1); -- Hesti (Tech Writer)
INSERT INTO user_task (user_id, task_id) VALUES (14, 1); -- Joko (DBA)

-- Proyek 2: Company Profile (Tim kecil)
INSERT INTO user_task (user_id, task_id) VALUES (1, 2);  -- Andi (PM)
INSERT INTO user_task (user_id, task_id) VALUES (4, 2);  -- Toni (UI/UX Designer)
INSERT INTO user_task (user_id, task_id) VALUES (7, 2);  -- Dian (Jr. Frontend)
INSERT INTO user_task (user_id, task_id) VALUES (5, 2);  -- Faizal (QA)

-- Proyek 3: Mobile Banking (Tim Mobile & Backend)
INSERT INTO user_task (user_id, task_id) VALUES (1, 3);  -- Andi (PM)
INSERT INTO user_task (user_id, task_id) VALUES (9, 3);  -- Maya (Business Analyst)
INSERT INTO user_task (user_id, task_id) VALUES (2, 3);  -- Siti (Sr. Backend)
INSERT INTO user_task (user_id, task_id) VALUES (10, 3); -- Santo (Android)
INSERT INTO user_task (user_id, task_id) VALUES (11, 3); -- Cindy (iOS)
INSERT INTO user_task (user_id, task_id) VALUES (5, 3);  -- Faizal (QA)
INSERT INTO user_task (user_id, task_id) VALUES (8, 3);  -- Iqbal (DevOps)
INSERT INTO user_task (user_id, task_id) VALUES (14, 3); -- Joko (DBA)

-- Proyek 4: CRM Internal (Tim Internal)
INSERT INTO user_task (user_id, task_id) VALUES (1, 4);  -- Andi (PM)
INSERT INTO user_task (user_id, task_id) VALUES (2, 4);  -- Siti (Sr. Backend)
INSERT INTO user_task (user_id, task_id) VALUES (3, 4);  -- Budi (Sr. Frontend)

-- Proyek 5: Logistik (Akan dimulai)
INSERT INTO user_task (user_id, task_id) VALUES (1, 5);
INSERT INTO user_task (user_id, task_id) VALUES (9, 5);
INSERT INTO user_task (user_id, task_id) VALUES (2, 5);
INSERT INTO user_task (user_id, task_id) VALUES (3, 5);

-- Proyek 6: API Gateway (Akan dimulai)
INSERT INTO user_task (user_id, task_id) VALUES (1, 6);
INSERT INTO user_task (user_id, task_id) VALUES (2, 6);
INSERT INTO user_task (user_id, task_id) VALUES (8, 6);

-- Maintenance (Tim Infrastruktur)
INSERT INTO user_task (user_id, task_id) VALUES (8, 7);  -- Iqbal (DevOps)
INSERT INTO user_task (user_id, task_id) VALUES (14, 7); -- Joko (DBA)
INSERT INTO user_task (user_id, task_id) VALUES (8, 8);  -- Iqbal (DevOps)
INSERT INTO user_task (user_id, task_id) VALUES (14, 8); -- Joko (DBA)