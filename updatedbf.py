import datetime
import json

import dbf

from readsagavers import read_version_info


def transfer_rows(old_file:str, new_file: str):
    # Open the old and new DBF files
    with dbf.Table(old_file) as old_table, dbf.Table(new_file) as new_table:
        # Find common fields between the two tables
        common_fields = set(old_table.field_names).intersection(new_table.field_names)

        # Transfer rows from old to new, filling extra fields with default values
        for old_record in old_table:
            # if new_table contains the same record, skip it
            has_record = False
            for new_record in new_table:
                if new_record[0] == old_record[0]:
                    # write the record in a commonrecords.txt
                    # date and time, new_file, record
                    # date and time, old_file, record
                    with open("pylogs/commonrecords.csv", "a") as file:
                        file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')},{new_file},{json.dumps(new_record.__str__())}\n")
                        file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')},{old_file},{json.dumps(old_record.__str__())}\n")
                    has_record = True
                    break
            if has_record:
                continue
            # Create a dictionary for the new record
            new_record_data = {}

            if(new_file.lower().endswith('societ.dbf')):
                # empty the table
                with dbf.Table(new_file) as new_table:
                    with new_table.__getitem__(0) as new_record_data:
                        new_version = read_version_info()
                        # Fill in common field values from the old record
                        for field in common_fields:
                            new_record_data[field] = old_record[field]

                        # Fill in default values for extra fields in the new table
                        for field in new_table.field_names:
                            if field not in common_fields:
                                field_type = new_table.field_info(field).field_type
                                new_record_data[field] = field_type.__init__()
                        new_record_data['VE'] = new_version
            
            # Add the new record to the new table
            if not (new_file.lower().endswith('societ.dbf')):
                # Fill in common field values from the old record
                for field in common_fields:
                    new_record_data[field] = old_record[field]

                # Fill in default values for extra fields in the new table
                for field in new_table.field_names:
                    if field not in common_fields:
                        field_type = new_table.field_info(field).field_type
                        new_record_data[field] = field_type.__init__()
                # write the record in a newrecords.txt
                # date and time, new_file, record
                with open("pylogs/newrecords.csv", "a") as file:
                    file.write(f"{datetime.datetime.now().strftime('%H:%M:%S')},{new_file},{new_record_data}\n")
                new_table.append(new_record_data)

# test
#transfer_rows('_0001_/societ.dbf', '0001/societ.dbf')