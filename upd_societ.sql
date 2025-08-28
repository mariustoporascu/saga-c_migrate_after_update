UPDATE SOCIET SET VE = 3593;
COMMIT;


isql -user SYSDBA -password masterkey "C:\SAGA C.3.0\0001 - Copy\cont_baza.fdb" -i export_schema.sql -o "C:\SAGA C.3.0\0001 - Copy\old_schema.txt"