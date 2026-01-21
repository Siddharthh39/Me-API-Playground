INSERT INTO profiles (name, email, education)
VALUES ('Siddharth Singh', 'hellosiddharthh@email.com', 'B.Tech CSE');

INSERT INTO skills (name)
VALUES ('Python'), ('FastAPI'), ('PostgreSQL'), ('AWS');

INSERT INTO profile_skills
SELECT 1, id FROM skills;

INSERT INTO projects (profile_id, title, description)
VALUES (
  1,
  'Portfolio Backend',
  'FastAPI backend hosted with AWS RDS'
);

INSERT INTO links (profile_id, github, linkedin, portfolio)
VALUES (
  1,
  'https://github.com/siddharthh39',
  'https://www.linkedin.com/in/siddharth-singh-python-developer/',
  'https://siddharthh39.github.io/resume/'
);
