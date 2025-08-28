SET LIST ON;
SET ECHO OFF;
SET HEADING OFF;
SET TERM ^ ;

-- Output all tables and their columns
SELECT rdb$relation_name AS table_name,
       rdb$field_name AS column_name,
       rdb$field_type AS field_type,
       rdb$null_flag AS not_null,
       rdb$default_source AS default_value
FROM rdb$relation_fields
WHERE rdb$system_flag = 0
ORDER BY rdb$relation_name, rdb$field_position
^

QUIT
^
