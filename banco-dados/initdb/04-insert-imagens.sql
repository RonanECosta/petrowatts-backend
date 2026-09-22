USE petrowatts_db;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/byd-dolphin-mini.png')
WHERE id = 1;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/byd-dolphin-mini-5l.png')
WHERE id = 2;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/byd-dolphin-gs.png')
WHERE id = 3;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/byd-dolphin-plus.png')
WHERE id = 4;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/gwm-ora-03.png')
WHERE id = 5;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/gwm-ora-03-gt.png')
WHERE id = 6;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/renault-kwid-e-tech.png')
WHERE id = 7;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/renault-megane-e-tech.png')
WHERE id = 8;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/jac-e-js1.png')
WHERE id = 9;

UPDATE carros_eletricos 
SET thumbnail = LOAD_FILE('/var/lib/mysql-files/caoa-cherry-icar.png')
WHERE id = 10;