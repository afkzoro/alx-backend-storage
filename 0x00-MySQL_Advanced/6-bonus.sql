-- Write a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.

-- Requirements:

-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects - if no projects.name found in the table, you should create it
-- score, the score value for the correction
CREATE PROCEDURE AddBonus(
    IN student_id INT,
    IN bonus_points INT,
    IN correction_date DATE,
    IN correction_text TEXT
)
BEGIN
    INSERT INTO corrections (student_id, points, correction_date, correction_text)
    VALUES (student_id, bonus_points, correction_date, correction_text);
END;
