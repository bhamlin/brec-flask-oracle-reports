
title = 'Disconnect list'
desc = 'Disconnects scheduled over the past week and not completed'
template = 'disconnect_list.html'
query = '''

SELECT
 so_master.SONO as service_order_id, loc.mapno as location_id,
 so_master.ACCOUNTNO as account_number, mtr.meterno as meter_number,
 f0002 as ResourceName, wtype.work_type as ORDER_TYPE, so_master.ORDER_STATUS,
 ATSCBS.DISCOVERER_FUNCTIONS.GET_MEMBER_NAME(acc_master.MEMBERNO) as MemberName,
 ATSCBS.DISCOVERER_FUNCTIONS.GET_SERVICE_ADDRESS(so_master.ACCOUNTNO) as Address,
 so_master.ACCOUNTNO as AccountNumber, so_master.COMPLETION_DATE as CompletionDate,
 so_master.CREATION_DATE as CreationDate, acc_master.MEMBERNO as MemberNumber,
 so_master.ORDER_STATUS as CurrentStatus
FROM
 ( SELECT ACCOUNTNO, BRANCH_ID AS i151258, MEMBERNO
   FROM ATSCBS.ACCOUNT_MASTER ) acc_master,
 ( SELECT COMPLETION_DATE, CREATION_DATE, ACCOUNTNO, ORDER_STATUS,
    REQUESTED_BY AS i153527, location_id, SONO, WORK_TYPE
   FROM CISDATA.SO_MASTER ) so_master,
 ( SELECT SO_MASTER.SONO AS f0001, RESOURCE_MASTER.RES_NAME AS f0002
   FROM ATSCBS.RESOURCE_MASTER RESOURCE_MASTER, CISDATA.SO_MASTER SO_MASTER
   WHERE ( RESOURCE_MASTER.ID = SO_MASTER.RESOURCE_ID ) ) oRes,
 ( select LOCATION_ID, METERNO from CISDATA.SERVICE_METERS ) mtr,
 ( SELECT LOCATION_ID, NAME as MAPNO from fmdata.location ) loc,
 CISDATA.TYPE_PROFILES wtype
WHERE ((so_master.ACCOUNTNO = acc_master.ACCOUNTNO))
   and (so_master.WORK_TYPE = wtype.work_type_id(+))
   and (f0001 = so_master.SONO)
   AND (( SYSDATE-so_master.CREATION_DATE(+) ) <= 6 )
   and (so_master.location_id = mtr.location_id )
   and (so_master.location_id = loc.location_id )
   and (so_master.ORDER_STATUS = 'Opened')
   and (wtype.work_type = 'Cutoff')
 --  and (wtype.work_type != 'Cutoff')
 --  and (f0002 = 'Andrew Harris')
ORDER BY so_master.CREATION_DATE DESC

'''.strip()

import csv
import io

def to_csv(data):
    output = io.StringIO()
    if data:
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow( ('so_number', 'location_id', 'account_number', 'meter_number',
                          'ResourceName', 'ORDER_TYPE', 'ORDER_STATUS', 'MemberName',
                          'Address', 'AccountNumber', 'CompletionDate', 'CreationDate',
                          'MemberNumber', 'CurrentStatus') )
        for row in data:
            writer.writerow(row)
    result = output.getvalue()
    output.close()
    return result
