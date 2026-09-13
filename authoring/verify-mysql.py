from pathlib import Path
import subprocess,json,csv
R=Path(__file__).resolve().parents[1];container='uiabd-lab-qa-20260913'
def sql(text,db='uiabd_qa',ok=True):
 p=subprocess.run(['docker','exec','-i',container,'mysql','-uroot','--batch','--raw',db],input=text.encode('utf-8'),capture_output=True)
 if ok and p.returncode:raise RuntimeError(p.stderr.decode())
 return p.stdout.decode('utf-8'),p.returncode
checks=[]
out,code=sql((R/'private/qa-procedure.sql').read_text(encoding='utf-8'));checks.append('procedure_and_trigger_created')
for v in range(1,31):
 material=1+(v-1)%4;branch=1+(v-1)%3
 base=int(sql(f'SELECT quantity FROM material_balances WHERE material_id={material} AND branch_id={branch};')[0].splitlines()[1].split('.')[0])
 ref=f'QA-V{v:02}'
 sql(f"CALL post_stock_movement({material},{branch},10,'RECEIPT','{ref}');")
 for call in [f"CALL post_stock_movement({material},{branch},10,'RECEIPT','{ref}');",f"CALL post_stock_movement({material},{branch},0,'ISSUE','BAD-{v}');",f"CALL post_stock_movement({material},{branch},999999,'ISSUE','BAD-{v}');"]:
  _,err=sql(call,ok=False);assert err
 after=int(sql(f'SELECT quantity FROM material_balances WHERE material_id={material} AND branch_id={branch};')[0].splitlines()[1].split('.')[0]);assert after==base+10
checks.append('30_variants_stock_atomicity_duplicate_zero_insufficient')
sql("START TRANSACTION; UPDATE orders SET status=status WHERE order_id=1001; COMMIT;")
assert sql('SELECT COUNT(*) FROM order_status_audit;')[0].splitlines()[1]=='0'
sql("START TRANSACTION; UPDATE orders SET status='DONE' WHERE order_id=1001; ROLLBACK;")
assert sql('SELECT COUNT(*) FROM order_status_audit;')[0].splitlines()[1]=='0'
sql("START TRANSACTION; UPDATE orders SET status='DONE' WHERE order_id=1001; COMMIT;")
assert sql('SELECT COUNT(*) FROM order_status_audit;')[0].splitlines()[1]=='1'
sql("UPDATE orders SET status='NEW' WHERE order_id=1001;")
checks.append('trigger_same_value_change_rollback_commit')
keys=[]
variants=list(csv.DictReader((R/'inputs/variants/c4-s7-variants.csv').read_text(encoding='utf-8-sig').splitlines()))
for r in variants:
 v=int(r['variant']);order=int(r['order_id']);statuses=','.join("'"+s+"'" for s in r['statuses'].split('|'))
 query=f"SELECT order_id FROM orders WHERE order_id<100000 AND branch_id={r['branch_id']} AND order_date>='{r['date_from']}' AND order_date<DATE_ADD('{r['date_to']}',INTERVAL 1 DAY) AND status IN ({statuses}) ORDER BY order_id;"
 selected=sql(query)[0].splitlines()[1:]
 query=f"SELECT COALESCE((SELECT SUM(i.quantity*s.unit_price) FROM order_items i JOIN services s USING(service_id) WHERE i.order_id={order}),0) AS service_cost, COALESCE((SELECT SUM(i.quantity*n.quantity_per_service*m.unit_price) FROM order_items i JOIN material_norms n USING(service_id) JOIN materials m USING(material_id) WHERE i.order_id={order}),0) AS material_cost;"
 costs=sql(query)[0].splitlines()[1].split('\t')
 keys.append({'variant':v,'order_id':order,'filtered_ids':selected,'service_cost':costs[0],'material_cost':costs[1],'total':round(float(costs[0])+float(costs[1]),2)})
(R/'private/mysql-variant-keys.json').write_text(json.dumps(keys,ensure_ascii=False,indent=2),encoding='utf-8')
checks.append('30_variant_filter_and_cost_reference_results')
sql((R/'inputs/backup/service_ops_backup.sql').read_text(encoding='utf-8'))
restored=sql((R/'inputs/sql/recovery_checks.sql').read_text(encoding='utf-8'))[0]
assert '53235.75' in restored
checks.append('backup_recovery_counts_sum_check_table')
(R/'quality/mysql-check.json').write_text(json.dumps({'server':sql('SELECT VERSION();')[0].splitlines()[1],'checks':checks,'recovery':restored,'scope':'isolated Docker MySQL, not Windows service or novice trial'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Passed:',len(checks),'check groups')
