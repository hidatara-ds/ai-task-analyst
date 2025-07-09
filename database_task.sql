CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  nama TEXT
);
CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY,
  task TEXT,
  start_date TEXT,
  end_date TEXT
);
CREATE TABLE IF NOT EXISTS activity (
  id INTEGER PRIMARY KEY,
  activity TEXT,
  task_id INTEGER,
  start_date TEXT,
  end_date TEXT,
  status TEXT
);

INSERT INTO user (id, nama) VALUES (1, 'Andi');
INSERT INTO user (id, nama) VALUES (2, 'Siti');
INSERT INTO user (id, nama) VALUES (3, 'Budi');
INSERT INTO task (id, task, start_date, end_date) VALUES (1, 'Develop Backend API', '2025-06-10', '2025-06-21');
INSERT INTO task (id, task, start_date, end_date) VALUES (2, 'Database Optimization', '2025-06-20', '2025-06-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (3, 'UI Design Dashboard', '2025-06-10', '2025-06-20');
INSERT INTO task (id, task, start_date, end_date) VALUES (4, 'Frontend Dev React', '2025-06-20', '2025-06-30');
INSERT INTO task (id, task, start_date, end_date) VALUES (5, 'Client Support System', '2025-06-10', '2025-06-23');
INSERT INTO task (id, task, start_date, end_date) VALUES (6, 'Internal Training Material', '2025-06-20', '2025-06-29');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (1, 'Create endpoint /users', 1, '2025-06-10', '2025-06-12', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (2, 'Add JWT auth', 1, '2025-06-13', '2025-06-17', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (3, 'Write tests', 1, '2025-06-18', '2025-06-20', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (4, 'Analyze slow queries', 2, '2025-06-20', '2025-06-22', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (5, 'Add index + benchmark', 2, '2025-06-23', '2025-06-27', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (6, 'Final testing', 2, '2025-06-28', '2025-06-29', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (7, 'Sketch wireframe', 3, '2025-06-10', '2025-06-11', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (8, 'Figma High-Fidelity', 3, '2025-06-12', '2025-06-16', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (9, 'User Testing & Revision', 3, '2025-06-17', '2025-06-19', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (10, 'Component Layout', 4, '2025-06-20', '2025-06-22', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (11, 'Form Handling + Validation', 4, '2025-06-23', '2025-06-26', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (12, 'Style polish', 4, '2025-06-27', '2025-06-29', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (13, 'Build ticket module', 5, '2025-06-10', '2025-06-13', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (14, 'Setup email alert', 5, '2025-06-14', '2025-06-17', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (15, 'Bug fixing + deploy', 5, '2025-06-18', '2025-06-22', 'completed');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (16, 'Draft content', 6, '2025-06-20', '2025-06-22', 'in_progress');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (17, 'Review + format', 6, '2025-06-23', '2025-06-25', 'pending');
INSERT INTO activity (id, activity, task_id, start_date, end_date, status) VALUES (18, 'Publish', 6, '2025-06-26', '2025-06-28', 'pending');
