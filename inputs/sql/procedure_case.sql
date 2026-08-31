-- Набор вызовов; процедура создаётся студентом.
CALL post_stock_movement(1,1,10,'RECEIPT','CALL-OK-01');
CALL post_stock_movement(1,1,3,'ISSUE','CALL-OK-02');
CALL post_stock_movement(999,1,1,'RECEIPT','CALL-BAD-MATERIAL');
CALL post_stock_movement(1,1,0,'RECEIPT','CALL-BAD-ZERO');
CALL post_stock_movement(1,1,999999,'ISSUE','CALL-BAD-BALANCE');
CALL post_stock_movement(1,1,10,'RECEIPT','CALL-OK-01');
