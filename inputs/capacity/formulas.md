# Формулы учебной оценки

- Данные к концу периода: `current_data + monthly_growth × planning_months`.
- Диск с резервом: `projected_data × 1.35 + projected_data × 0.15 × retention_copies`.
- Рабочий набор: `projected_data × active_share_pct / 100`.
- Память: `working_set × 0.35 + max_connections × per_connection_MiB / 1024 + 8 GiB`.
- Сеть: `daily_transfer_GiB × 8192 / (peak_window_hours × 3600) × 1.4` Мбит/с.

Формулы — учебная модель. В выводе укажите, какое допущение сильнее всего меняет выбор.
