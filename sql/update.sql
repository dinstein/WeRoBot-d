use mrobot;
drop table talk;
CREATE TABLE talk LIKE talk_e;
INSERT INTO talk SELECT * FROM talk_e;

