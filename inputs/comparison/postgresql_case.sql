CREATE SCHEMA platform_case;
CREATE TABLE platform_case.events(event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, category VARCHAR(30) NOT NULL, happened_at TIMESTAMPTZ NOT NULL, duration_ms INTEGER NOT NULL CHECK(duration_ms >= 0));
INSERT INTO platform_case.events(category,happened_at,duration_ms) VALUES ('read','2026-08-01 10:00:00+00',18),('write','2026-08-01 10:01:00+00',44),('read','2026-08-01 10:02:00+00',22),('read','2026-08-01 10:03:00+00',31);
CREATE ROLE platform_reader NOLOGIN;
GRANT USAGE ON SCHEMA platform_case TO platform_reader;
GRANT SELECT ON platform_case.events TO platform_reader;
SELECT category, COUNT(*) AS event_count, ROUND(AVG(duration_ms),2) AS avg_ms FROM platform_case.events GROUP BY category ORDER BY category;
SELECT current_user, session_user;
SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state ORDER BY state;
