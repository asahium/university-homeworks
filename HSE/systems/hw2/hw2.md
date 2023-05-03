# hw2

Конечная ER-модель может быть представлена в виде таблиц следующим образом:

Таблица: Users

| Имя атрибута | Тип атрибута | Ограничение | Описание атрибута |
| --- | --- | --- | --- |
| user_id | INTEGER | PRIMARY KEY | Уникальный идентификатор пользователя |
| username | VARCHAR(50) | NOT NULL | Имя пользователя |
| password | VARCHAR(50) | NOT NULL | Пароль пользователя |

Таблица: Employees

| Имя атрибута | Тип атрибута | Ограничение | Описание атрибута |
| --- | --- | --- | --- |
| employee_id | INTEGER | PRIMARY KEY | Уникальный идентификатор сотрудника |
| full_name | VARCHAR(100) | NOT NULL | Полное имя сотрудника |
| position | VARCHAR(50) | NOT NULL | Должность сотрудника |
| department_id | INTEGER | FOREIGN KEY | Идентификатор отдела, к которому принадлежит сотрудник |

Таблица: Departments

| Имя атрибута | Тип атрибута | Ограничение | Описание атрибута |
| --- | --- | --- | --- |
| department_id | INTEGER | PRIMARY KEY | Уникальный идентификатор отдела |
| name | VARCHAR(50) | NOT NULL | Название отдела |

Таблица: Applications

| Имя атрибута | Тип атрибута | Ограничение | Описание атрибута |
| --- | --- | --- | --- |
| application_id | INTEGER | PRIMARY KEY | Уникальный идентификатор заявки |
| employee_id | INTEGER | FOREIGN KEY | Идентификатор сотрудника, подавшего заявку |
| date | DATE | NOT NULL | Дата подачи заявки |

Таблица: Assessments

| Имя атрибута | Тип атрибута | Ограничение | Описание атрибута |
| --- | --- | --- | --- |
| assessment_id | INTEGER | PRIMARY KEY | Уникальный идентификатор аттестации |
| application_id | INTEGER | FOREIGN KEY | Идентификатор заявки, по которой была проведена аттестация |
| date | DATE | NOT NULL | Дата проведения аттестации |
| result | VARCHAR(50) | NOT NULL | Результаты аттестации |
| decision | VARCHAR(50) | NOT NULL | Решение о присвоении квалификации сотруднику |

### Скрипты для создания таблиц:

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  department_id INTEGER NOT NULL,
  qualification TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE departments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  employee_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id INTEGER NOT NULL,
  evaluator_id INTEGER NOT NULL,
  result TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (application_id) REFERENCES applications(id),
  FOREIGN KEY (evaluator_id) REFERENCES employees(id)
);
```

Дамп сохранен в файле dump.

### Возможные запросы к базе данных для формирования отчетов по аттестации медицинских работников:

- Отчет о количестве поданных заявок на аттестацию по отделам за последний месяц:

```sql
SELECT departments.name AS department, COUNT(applications.id) AS num_applications
FROM applications
JOIN employees ON employees.id = applications.employee_id
JOIN departments ON departments.id = employees.department_id
WHERE applications.created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
GROUP BY departments.id;
```

- Отчет о количестве проведенных аттестаций по отделам за последний месяц:

```sql
SELECT departments.name AS department, COUNT(assessments.id) AS num_assessments
FROM assessments
JOIN applications ON applications.id = assessments.application_id
JOIN employees ON employees.id = applications.employee_id
JOIN departments ON departments.id = employees.department_id
WHERE assessments.created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
GROUP BY departments.id;
```

- Отчет о средней оценке сотрудников в каждом отделе за последний месяц:

```sql
SELECT departments.name AS department, AVG(CAST(assessments.result AS INTEGER)) AS avg_rating
FROM assessments
JOIN applications ON applications.id = assessments.application_id
JOIN employees ON employees.id = applications.employee_id
JOIN departments ON departments.id = employees.department_id
WHERE assessments.created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
GROUP BY departments.id;
```

- Отчет о количестве проведенных аттестаций сотрудниками врачебной специальности за последний месяц:

```sql
SELECT COUNT(DISTINCT assessments.id) AS num_assessments
FROM assessments
JOIN applications ON applications.id = assessments.application_id
JOIN employees ON employees.id = applications.employee_id
WHERE employees.qualification = 'врач' AND assessments.created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime');
```

- Отчет о количестве сотрудников врачебной специальности, не прошедших аттестацию в последний месяц:

```sql
SELECT COUNT(DISTINCT employees.id) AS num_employees
FROM employees
LEFT JOIN applications ON applications.employee_id = employees.id AND applications.created_at BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime')
LEFT JOIN assessments ON assessments.application_id = applications.id
WHERE employees.qualification = 'врач' AND assessments.id IS NULL;
```

Результаты запросов представлены в файлах с соответствующими названиями.