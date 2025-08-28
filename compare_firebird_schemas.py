import re

FIELD_TYPE_MAP = {
    7: "SMALLINT",
    8: "INTEGER",
    9: "QUAD",
    10: "FLOAT",
    11: "D_FLOAT",
    12: "DATE",
    13: "TIME",
    14: "CHAR",
    16: "BIGINT",
    27: "DOUBLE",
    35: "TIMESTAMP",
    37: "VARCHAR",
    261: "BLOB"
}

def parse_schema_multiline(file_path):
    """Parse ISQL multi-line schema dump."""
    schema = {}
    current = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if 'TABLE_NAME' in current and 'COLUMN_NAME' in current:
                    table = current['TABLE_NAME']
                    column = current['COLUMN_NAME']
                    dtype_code = int(current.get('FIELD_TYPE_CODE', 0))
                    not_null = current.get('NOT_NULL', '<null>')
                    default = current.get('DEFAULT_VALUE', None)
                    dtype = FIELD_TYPE_MAP.get(dtype_code, f"UNKNOWN({dtype_code})")
                    schema.setdefault(table, {})[column] = (dtype, not_null, default)
                current = {}
                continue
            match = re.match(r'(\w+)\s+(.*)', line)
            if match:
                key, value = match.groups()
                current[key.strip()] = value.strip()
    # Last column
    if 'TABLE_NAME' in current and 'COLUMN_NAME' in current:
        table = current['TABLE_NAME']
        column = current['COLUMN_NAME']
        dtype_code = int(current.get('FIELD_TYPE_CODE', 0))
        not_null = current.get('NOT_NULL', '<null>')
        default = current.get('DEFAULT_VALUE', None)
        dtype = FIELD_TYPE_MAP.get(dtype_code, f"UNKNOWN({dtype_code})")
        schema.setdefault(table, {})[column] = (dtype, not_null, default)
    return schema

def generate_create_table(table_name, columns):
    """Generate CREATE TABLE SQL for a table."""
    col_defs = []
    for col, (dtype, not_null, default) in columns.items():
        line = f"    {col} {dtype}"
        if not_null != '<null>':
            line += " NOT NULL"
        if default not in (None, '<null>'):
            line += f" {default}"
        col_defs.append(line)
    cols_sql = ",\n".join(col_defs)
    return f"CREATE TABLE {table_name} (\n{cols_sql}\n);"

def compare_schemas(old_schema, new_schema):
    scripts = []

    old_tables = set(old_schema.keys())
    new_tables = set(new_schema.keys())

    # 1. Missing tables in old → generate full CREATE TABLE
    missing_tables = new_tables - old_tables
    for table in missing_tables:
        create_sql = generate_create_table(table, new_schema[table])
        scripts.append(f"-- Missing table in old DB: {table}")
        scripts.append(create_sql)

    # 2. Deleted tables in new
    deleted_tables = old_tables - new_tables
    for table in deleted_tables:
        scripts.append(f"-- Deleted table in new DB: {table} (consider dropping or logging)")

    # 3 & 4. Columns for common tables
    common_tables = old_tables & new_tables
    for table in common_tables:
        old_cols = set(old_schema[table].keys())
        new_cols = set(new_schema[table].keys())

        # 3. Missing columns in old
        for col in new_cols - old_cols:
            dtype, not_null, default = new_schema[table][col]
            line = f"ALTER TABLE {table} ADD {col} {dtype}"
            if not_null != '<null>':
                line += " NOT NULL"
            if default not in (None, '<null>'):
                line += f" {default}"
            line += ";"
            scripts.append(line)

        # 4. Deleted columns in new
        for col in old_cols - new_cols:
            scripts.append(f"-- Column {col} in table {table} exists in old DB but not in new DB (consider dropping or logging)")

    return scripts

if __name__ == "__main__":
    old_schema = parse_schema_multiline('old_schema.txt')
    new_schema = parse_schema_multiline('new_schema.txt')

    scripts = compare_schemas(old_schema, new_schema)

    if scripts:
        with open('update_schema.sql', 'w', encoding='utf-8') as f:
            f.write('\n'.join(scripts))
        print("Update script generated: update_schema.sql")
    else:
        print("Schemas are identical")
