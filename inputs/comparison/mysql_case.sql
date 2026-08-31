CREATE DATABASE IF NOT EXISTS platform_case CHARACTER SET utf8mb4;
USE platform_case;
CREATE TABLE events(event_id BIGINT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(30) NOT NULL, happened_at TIMESTAMP NOT NULL, duration_ms INT NOT NULL CHECK(duration_ms >= 0));
INSERT INTO events(category,happened_at,duration_ms) VALUES ('read','2026-08-01 10:00:00',18),('write','2026-08-01 10:01:00',44),('read','2026-08-01 10:02:00',22),('read','2026-08-01 10:03:00',31);
CREATE ROLE platform_reader;
GRANT SELECT ON platform_case.* TO platform_reader;
SELECT category, COUNT(*) AS event_count, ROUND(AVG(duration_ms),2) AS avg_ms FROM events GROUP BY category ORDER BY category;
SELECT USER(), CURRENT_USER();
SHOW STATUS LIKE 'Threads_connected';
