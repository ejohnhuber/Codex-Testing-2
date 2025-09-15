diff --git a//dev/null b/tests/test_arbitrage_checker.py
index 0000000000000000000000000000000000000000..834b582dc1c1027c863c347d69bee668d8a0be25 100644
--- a//dev/null
+++ b/tests/test_arbitrage_checker.py
@@ -0,0 +1,28 @@
+import os
+import sys
+
+sys.path.append(os.path.dirname(os.path.dirname(__file__)))
+
+from arbitrage_checker import check_arbitrage
+
+
+def test_detects_arbitrage_buy_b_sell_a():
+    result = check_arbitrage("Brent", 85.0, "WTI", 80.0)
+    assert result.arbitrage is True
+    assert result.buy_market == "WTI"
+    assert result.sell_market == "Brent"
+    assert result.profit == 5.0
+
+
+def test_detects_arbitrage_buy_a_sell_b():
+    result = check_arbitrage("LME", 75.0, "CME", 78.0)
+    assert result.arbitrage is True
+    assert result.buy_market == "LME"
+    assert result.sell_market == "CME"
+    assert result.profit == 3.0
+
+
+def test_no_arbitrage_when_difference_below_cost():
+    result = check_arbitrage("Market A", 100.0, "Market B", 99.5, transaction_cost=1.0)
+    assert result.arbitrage is False
+    assert result.profit == 0.0
