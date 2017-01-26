
title = 'Engineer list'
desc = 'List of engineers configured in ATS'
template = 'engineer_list.html'
query = '''

select engineer_no, engineer_name
from fisdata.engineers
where engineer_name not like 'x%'
order by engineer_name

'''.strip()

import csv
import io

def to_csv(data):
    output = io.StringIO()
    if data:
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow( ('engineer_no', 'engineer_name') )
        for row in data:
            writer.writerow(row)
    result = output.getvalue()
    output.close()
    return result
