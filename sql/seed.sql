INSERT INTO games (game_id, title, developer, publisher, release_date, price) VALUES
    (1,  'Hollow Knight',                    'Team Cherry',            'Team Cherry',                     '2017-02-24', 14.99),
    (2,  'Stardew Valley',                   'ConcernedApe',           'ConcernedApe',                    '2016-02-26', 14.99),
    (3,  'Hades',                            'Supergiant Games',       'Supergiant Games',                '2020-09-17', 24.99),
    (4,  'Lethal Company',                   'Zeekerss',               'Zeekerss',                        '2023-10-23', 9.99),
    (5,  'Among Us',                         'Innersloth',             'Innersloth',                      '2018-11-16', 4.99),
    (6,  'Elden Ring',                       'FromSoftware',           'Bandai Namco',                    '2022-02-25', 59.99),
    (7,  'Dark Souls III',                   'FromSoftware',           'Bandai Namco',                    '2016-04-12', 59.99),
    (8,  'Tekken 8',                         'Bandai Namco Studios',   'Bandai Namco',                    '2024-01-26', 69.99),
    (9,  'Baldur''s Gate 3',                 'Larian Studios',         'Larian Studios',                  '2023-08-03', 59.99),
    (10, 'Portal 2',                         'Valve',                  'Valve',                           '2011-04-18', 9.99),
    (11, 'Counter-Strike 2',                 'Valve',                  'Valve',                           '2023-09-27', 0.00),
    (12, 'Half-Life 2',                      'Valve',                  'Valve',                           '2004-11-16', 9.99),
    (13, 'Left 4 Dead 2',                    'Valve',                  'Valve',                           '2009-11-17', 9.99),
    (14, 'Phasmophobia',                     'Kinetic Games',          'Kinetic Games',                   '2020-09-18', 19.99),
    (15, 'Content Warning',                  'Skog',                   'Landfall',                        '2024-04-01', 7.99),
    (16, 'Totally Accurate Battle Simulator','Landfall',               'Landfall',                        '2021-04-01', 19.99),
    (17, 'PEAK',                             'Aggro Crab',             'Landfall',                        '2025-06-16', 7.99),
    (18, 'Celeste',                          'Maddy Makes Games',      'Maddy Makes Games',               '2018-01-25', 19.99),
    (19, 'Terraria',                         'Re-Logic',               'Re-Logic',                        '2011-05-16', 9.99),
    (20, 'Cyberpunk 2077',                   'CD Projekt Red',         'CD Projekt',                      '2020-12-10', 59.99),
    (21, 'The Witcher 3: Wild Hunt',         'CD Projekt Red',         'CD Projekt',                      '2015-05-18', 9.99),
    (22, 'Hades II',                         'Supergiant Games',       'Supergiant Games',                '2025-09-25', 29.99),
    (23, 'Helldivers 2',                     'Arrowhead Game Studios', 'Sony Interactive Entertainment',  '2024-02-08', 39.99),
    (24, 'Vampire Survivors',                'poncle',                 'poncle',                          '2022-10-20', 4.99),
    (25, 'R.E.P.O.',                         'semiwork',               'semiwork',                        '2025-02-26', 9.99);

UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/367520/3c3489495136b26b34f8a9543c7f5645b99d388c/header.jpg?t=1776125684', steam_app_id = 367520 WHERE game_id = 1;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/413150/header.jpg?t=1786554168', steam_app_id = 413150 WHERE game_id = 2;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1145360/header.jpg?t=1758127023', steam_app_id = 1145360 WHERE game_id = 3;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1966720/header.jpg?t=1775380053', steam_app_id = 1966720 WHERE game_id = 4;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/945360/d611f3f87743b5121532023b1d3ee2dd0e96e772/header.jpg?t=1793821899', steam_app_id = 945360 WHERE game_id = 5;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg?t=1790290043', steam_app_id = 1245620 WHERE game_id = 6;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/374320/header.jpg?t=1748630784', steam_app_id = 374320 WHERE game_id = 7;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1778820/bb40124a525d6146a7c1ee4848bf3a14aa716224/header.jpg?t=1794438159', steam_app_id = 1778820 WHERE game_id = 8;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1086940/48a2fcbda8565bb45025e98fd8ebde8a7203f6a0/header.jpg?t=1777363040', steam_app_id = 1086940 WHERE game_id = 9;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/620/faffc0f560786e2f05104a8d2fac837c6969bf13/header.jpg?t=1790187113', steam_app_id = 620 WHERE game_id = 10;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/730/162664aa5da85f418105350c5d67ca565f6c3713/header.jpg?t=1793054556', steam_app_id = 730 WHERE game_id = 11;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/220/header.jpg?t=1745368545', steam_app_id = 220 WHERE game_id = 12;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/550/header.jpg?t=1772742214', steam_app_id = 550 WHERE game_id = 13;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/739630/8fc6642a091321343695b2273f8f7137c5d26483/header_alt_assets_14.jpg?t=1795522435', steam_app_id = 739630 WHERE game_id = 14;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2881650/header.jpg?t=1785137321', steam_app_id = 2881650 WHERE game_id = 15;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/508440/header.jpg?t=1730715415', steam_app_id = 508440 WHERE game_id = 16;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3527290/31bac6b2eccf09b368f5e95ce510bae2baf3cfcd/header.jpg?t=1792684718', steam_app_id = 3527290 WHERE game_id = 17;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/504230/header.jpg?t=1714089525', steam_app_id = 504230 WHERE game_id = 18;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/105600/header.jpg?t=1792530636', steam_app_id = 105600 WHERE game_id = 19;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1091500/48a93d6445a67520ea49833c93dae8f2e68fc540/header_alt_assets_9.jpg?t=1794474878', steam_app_id = 1091500 WHERE game_id = 20;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/292030/4b5b1ba5061b8a992cc69ac58b4245434edb4296/header.jpg?t=1793900434', steam_app_id = 292030 WHERE game_id = 21;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1145350/91ac334a2c137d08968ccc0bc474a02579602100/header.jpg?t=1779901265', steam_app_id = 1145350 WHERE game_id = 22;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/553850/850e2f9e5bb15c5706bb9a1edc832f4f782e8be5/header.jpg?t=1793395133', steam_app_id = 553850 WHERE game_id = 23;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1794680/2ca07b690dde645771125ed9d9206c4c5fde4dd4/header.jpg?t=1794307910', steam_app_id = 1794680 WHERE game_id = 24;
UPDATE games SET image_url = 'https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3241660/62177765c05399116f0453fe1177b00ceed698c4/header_alt_assets_3.jpg?t=1793278962', steam_app_id = 3241660 WHERE game_id = 25;

INSERT INTO tags (tag_id, name) VALUES
    (1,  'Action'),
    (2,  'Multiplayer'),
    (3,  'Indie'),
    (4,  'Friend Slop'),
    (5,  'Co-op'),
    (6,  'Singleplayer'),
    (7,  'RPG'),
    (8,  'Horror'),
    (9,  'Roguelike'),
    (10, 'Open World'),
    (11, 'FPS'),
    (12, 'Platformer'),
    (13, 'Puzzle'),
    (14, 'Simulation'),
    (15, 'Story Rich'),
    (16, 'Strategy'),
    (17, 'Fighting'),
    (18, 'Sandbox'),
    (19, 'Discount');

INSERT INTO game_tags (game_id, tag_id) VALUES
    (1, 1), (1, 3), (1, 6), (1, 12),
    (2, 2), (2, 3), (2, 5), (2, 14),
    (3, 1), (3, 3), (3, 6), (3, 9),
    (4, 2), (4, 3), (4, 4), (4, 5), (4, 8),
    (5, 2), (5, 3), (5, 4),
    (6, 1), (6, 2), (6, 7), (6, 10),
    (7, 1), (7, 6), (7, 7),
    (8, 1), (8, 2), (8, 17),
    (9, 2), (9, 5), (9, 7), (9, 15),
    (10, 5), (10, 6), (10, 13),
    (11, 1), (11, 2), (11, 11),
    (12, 1), (12, 6), (12, 11), (12, 15),
    (13, 1), (13, 2), (13, 5), (13, 8), (13, 11),
    (14, 2), (14, 3), (14, 4), (14, 5), (14, 8),
    (15, 2), (15, 3), (15, 4), (15, 5), (15, 8),
    (16, 3), (16, 14), (16, 16),
    (17, 2), (17, 3), (17, 4), (17, 5),
    (18, 3), (18, 6), (18, 12),
    (19, 1), (19, 2), (19, 3), (19, 5), (19, 18),
    (20, 1), (20, 7), (20, 10), (20, 11), (20, 15),
    (21, 6), (21, 7), (21, 10), (21, 15), (21, 19),
    (22, 1), (22, 3), (22, 6), (22, 9),
    (23, 1), (23, 2), (23, 5), (23, 11),
    (24, 1), (24, 3), (24, 9),
    (25, 2), (25, 3), (25, 4), (25, 5), (25, 8);

INSERT INTO platforms (platform_id, name) VALUES
    (1, 'Steam'),
    (2, 'Epic Games Store'),
    (3, 'PlayStation Store'),
    (4, 'Xbox Store'),
    (5, 'Nintendo eShop');

INSERT INTO game_platforms (game_id, platform_id) VALUES
    (1, 1), (1, 3), (1, 4), (1, 5),
    (2, 1), (2, 3), (2, 4), (2, 5),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (4, 1),
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (6, 1), (6, 3), (6, 4),
    (7, 1), (7, 3), (7, 4),
    (8, 1), (8, 3), (8, 4),
    (9, 1), (9, 3), (9, 4),
    (10, 1), (10, 5),
    (11, 1),
    (12, 1),
    (13, 1),
    (14, 1), (14, 3), (14, 4),
    (15, 1),
    (16, 1), (16, 2), (16, 3), (16, 4),
    (17, 1),
    (18, 1), (18, 2), (18, 3), (18, 4), (18, 5),
    (19, 1), (19, 3), (19, 4), (19, 5),
    (20, 1), (20, 2), (20, 3), (20, 4), (20, 5),
    (21, 1), (21, 2), (21, 3), (21, 4), (21, 5),
    (22, 1), (22, 2), (22, 5),
    (23, 1), (23, 3), (23, 4),
    (24, 1), (24, 3), (24, 4), (24, 5),
    (25, 1);

INSERT INTO users (user_id, username, email, created_at) VALUES
    (1,  'lestat',      'lestat@example.com',      '2025-01-14 18:22:05'),
    (2,  'duy',         'duy@example.com',         '2025-01-14 18:40:51'),
    (3,  'nightowl',    'nightowl@example.com',    '2025-02-03 02:15:33'),
    (4,  'pixelpusher', 'pixelpusher@example.com', '2025-03-21 14:08:12'),
    (5,  'frag_queen',  'fragqueen@example.com',   '2025-04-09 20:47:39'),
    (6,  'cozygamer',   'cozygamer@example.com',   '2025-05-30 11:30:00'),
    (7,  'speedrunsam', 'sam@example.com',         '2025-07-12 16:55:21'),
    (8,  'lootgoblin',  'lootgoblin@example.com',  '2025-08-25 22:03:47'),
    (9,  'retro_rick',  'rick@example.com',        '2025-10-02 09:19:10'),
    (10, 'newbie42',    'newbie42@example.com',    '2026-10-30 13:45:00');

INSERT INTO library (user_id, game_id, created_at) VALUES
    (1, 4,  '2025-01-15 20:10:00'),
    (1, 5,  '2025-01-15 20:12:00'),
    (1, 14, '2025-02-01 21:30:00'),
    (1, 25, '2025-03-01 19:00:00'),
    (1, 13, '2025-04-11 22:45:00'),
    (2, 1,  '2025-01-15 10:05:00'),
    (2, 3,  '2025-01-20 17:40:00'),
    (2, 6,  '2025-02-14 23:10:00'),
    (2, 7,  '2025-03-02 18:25:00'),
    (2, 4,  '2025-03-15 21:00:00'),
    (2, 11, '2025-04-05 16:30:00'),
    (3, 8,  '2025-02-04 03:00:00'),
    (3, 11, '2025-02-04 03:20:00'),
    (3, 23, '2025-02-10 01:45:00'),
    (3, 6,  '2025-03-08 02:30:00'),
    (4, 18, '2025-03-22 15:00:00'),
    (4, 1,  '2025-03-25 19:20:00'),
    (4, 24, '2025-04-02 12:10:00'),
    (5, 11, '2025-04-10 21:00:00'),
    (5, 13, '2025-04-12 22:30:00'),
    (5, 23, '2025-05-01 20:15:00'),
    (5, 12, '2025-05-20 18:00:00'),
    (6, 2,  '2025-05-30 12:00:00'),
    (6, 16, '2025-06-10 14:30:00'),
    (6, 9,  '2025-08-04 10:00:00'),
    (7, 18, '2025-07-12 17:30:00'),
    (7, 1,  '2025-07-13 09:00:00'),
    (7, 10, '2025-08-01 20:40:00'),
    (8, 20, '2025-08-26 19:00:00'),
    (8, 21, '2025-08-26 19:05:00'),
    (8, 9,  '2025-09-12 21:30:00'),
    (8, 19, '2025-10-01 18:15:00'),
    (9, 12, '2025-10-02 10:00:00'),
    (9, 10, '2025-10-03 11:30:00'),
    (9, 19, '2025-10-20 15:45:00');
