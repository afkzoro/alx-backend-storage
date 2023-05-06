-- Write a SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student. Note: An average score can be a decimal

-- Requirements:

-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
  DECLARE total_score INT;
  DECLARE num_assignments INT;
  DECLARE average_score DECIMAL(5,2);

  -- Computes total score and number of assignments for the student
  SELECT SUM(score), COUNT(*) FROM scores WHERE student_id = user_id INTO total_score, num_assignments;

  -- Computes the average score
  IF num_assignments > 0 THEN
    SET average_score = total_score / num_assignments;
  ELSE
    SET average_score = 0;
  END IF;

  -- Stores the average score for the student
  UPDATE students SET average_score = average_score WHERE id = user_id;
END;
