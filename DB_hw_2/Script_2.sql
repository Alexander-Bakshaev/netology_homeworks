CREATE TABLE Employee (
    employee_id INT PRIMARY KEY,       -- Уникальный идентификатор сотрудника
    name VARCHAR(50) NOT NULL,         -- Имя сотрудника
    department VARCHAR(50),            -- Отдел сотрудника
    supervisor_id INT,                 -- Идентификатор начальника (ссылка на другого сотрудника)
    FOREIGN KEY (supervisor_id) REFERENCES Employee(employee_id)
);
