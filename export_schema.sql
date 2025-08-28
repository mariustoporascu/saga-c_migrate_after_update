SET LIST ON;
SET ECHO OFF;
SET HEADING OFF;
SET TERM ^ ;

SELECT
    rf.rdb$relation_name AS table_name,
    rf.rdb$field_name AS column_name,
    f.rdb$field_type AS field_type_code,
    rf.rdb$null_flag AS not_null,
    rf.rdb$default_source AS default_value
FROM rdb$relation_fields rf
JOIN rdb$fields f ON rf.rdb$field_source = f.rdb$field_name
WHERE rf.rdb$system_flag = 0
ORDER BY rf.rdb$relation_name, rf.rdb$field_position
^

QUIT
^
