show pdbs;
ALTER SYSTEM SET PROCESSES=500 SCOPE=SPFILE;
alter session set container= freepdb1;
create user bosskit identified by bosskit DEFAULT TABLESPACE users quota unlimited on users;
grant DB_DEVELOPER_ROLE to bosskit;

BEGIN
CTX_DDL.CREATE_PREFERENCE('bosskit.world_lexer','WORLD_LEXER');
END;
/
