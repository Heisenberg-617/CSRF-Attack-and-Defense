-- Password is 'Admin123!' hashed with werkzeug's generate_password_hash function using scrypt
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@corpo.com', 'scrypt:32768:8:1$fnXRsw345iNzaCsJ$5542690ece89a3d0ba754c419b3c4466253cba64b0db0401cae8ca2e456eb5a1e1d9832fcf79c9a89eb51aee5015a1ae80b7911014a618e43b81905694d97d33', 'admin');

-- 3. Create standard users (to test that they CAN'T access admin routes)
INSERT INTO users (username, email, password_hash, role) VALUES 
('resp_equipe', 'resp1@corpo.com', 'scrypt:32768:8:1$mQ3GpoTVubNILdlk$f4b419edcd03276d02635d3b8f398633607e7db3e3a738c741843ac31f1ba77663b1532966a130cefe53d3893e2c0d0cbe9ddd5bdabc6aa21129473a51bdaedd', 'responsable_equipe'),
('resp_projet', 'resp2@corpo.com', 'scrypt:32768:8:1$8jqdsPz4EgGd5aOv$faccadf71f2702b8ca9d47031b4525f268309ad8e0cf806c4b9b52675c49769b11b6ad0d69d4990f44a363c07ca9b97381a2b4c974cecfbc55cf37559e4660a4', 'responsable_projet'),
('guest1', 'guest@corpo.com', 'scrypt:32768:8:1$WvyOEv8mekmOS91s$3c8fb14d6d9a5a19dd8eb7cb4f2184513a35e4aff39c6d82a92e6c6100509c9a595181c0235b39112e1e4f28deef4fd3332646f4313739f3049ce6165f933724', 'guest'),
('guest2', 'guest2@corpo.com', 'scrypt:32768:8:1$uO4dp6jddMgvY2m4$a79ed106bdd3608eaa3afb040a1d2628c4586b0fe0b3ac23e7463eb33d49505aad7502ef8774e0f1073b77316017c2f4879c1f39e350a7b319effd31ca97ad10', 'guest');

INSERT INTO teams (name, description) VALUES 
('Team Alpha', 'This is the first team.'),
('Team Beta', 'This is the second team.');

INSERT INTO tasks (title, description, deadline, status, user_id, team_id) VALUES 
('Task 1', 'Description for Task 1', '2026-12-31 23:59:59', 'todo', 1, 1),
('Task 2', 'Description for Task 2', '2026-11-20 23:59:59', 'todo', 1, 1),
('Task 3', 'Description for Task 3', '2026-10-20 23:59:59', 'todo', 1, 1),
('Task 4', 'Description for Task 4', '2026-09-20 23:59:59', 'todo', 1, 2),
('Task 5', 'Description for Task 5', '2026-08-20 23:59:59', 'todo', 1, 2);

-- Passwords:
--    "admin": "Admin123!",
--    "resp_equipe": "RespEq123!",
--    "resp_projet": "RespPr123!",
--    "guest1": "Guest1!",
--    "guest2": "Guest2!"
