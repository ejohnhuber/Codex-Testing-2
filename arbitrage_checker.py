 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a//dev/null b/arbitrage_checker.py
index 0000000000000000000000000000000000000000..21f868b084db4cdeaa4f5527fe3c68e3f829e156 100644
--- a//dev/null
+++ b/arbitrage_checker.py
@@ -0,0 +1,95 @@
+"""Simple Trade Arbitrage Checker.
+
+This module provides a helper function to compare the prices of the same
+product across two markets and determine whether a simple arbitrage
+opportunity exists.
+
+Example
+-------
+>>> check_arbitrage("Brent", 85.0, "WTI", 80.0)
+{'arbitrage': True, 'buy_market': 'WTI', 'sell_market': 'Brent', 'profit': 5.0}
+
+"""
+
+from __future__ import annotations
+
+from dataclasses import dataclass
+
+
+@dataclass
+class ArbitrageResult:
+    """Result returned by :func:`check_arbitrage`.
+
+    Attributes
+    ----------
+    arbitrage: bool
+        Whether an arbitrage opportunity exists.
+    buy_market: str | None
+        Market where the product should be bought. ``None`` if no opportunity
+        exists.
+    sell_market: str | None
+        Market where the product should be sold. ``None`` if no opportunity
+        exists.
+    profit: float
+        Expected profit per unit after accounting for ``transaction_cost``.
+    """
+
+    arbitrage: bool
+    buy_market: str | None
+    sell_market: str | None
+    profit: float
+
+
+def check_arbitrage(
+    market_a: str,
+    price_a: float,
+    market_b: str,
+    price_b: float,
+    transaction_cost: float = 0.0,
+) -> ArbitrageResult:
+    """Compare two markets and report any arbitrage gap.
+
+    Parameters
+    ----------
+    market_a, market_b:
+        Names of the markets being compared.
+    price_a, price_b:
+        Prices for the product in each market.
+    transaction_cost:
+        Estimated total cost (fees, transport, etc.) of executing the trade.
+
+    Returns
+    -------
+    ArbitrageResult
+        Details of the arbitrage opportunity if one exists, otherwise
+        ``arbitrage`` is ``False``.
+    """
+
+    price_diff = price_a - price_b
+    # Positive price_diff means market A is more expensive than market B.
+    if price_diff > transaction_cost:
+        profit = price_diff - transaction_cost
+        return ArbitrageResult(True, market_b, market_a, profit)
+    elif -price_diff > transaction_cost:
+        profit = -price_diff - transaction_cost
+        return ArbitrageResult(True, market_a, market_b, profit)
+    return ArbitrageResult(False, None, None, 0.0)
+
+
+def _format_result(result: ArbitrageResult) -> str:
+    if result.arbitrage:
+        return (
+            f"Arbitrage opportunity: buy in {result.buy_market} and sell in"
+            f" {result.sell_market} for profit {result.profit:.2f}"
+        )
+    return "No arbitrage opportunity"
+
+
+if __name__ == "__main__":
+    market_a = input("Market A name: ").strip() or "Market A"
+    price_a = float(input(f"Price in {market_a}: "))
+    market_b = input("Market B name: ").strip() or "Market B"
+    price_b = float(input(f"Price in {market_b}: "))
+    transaction_cost = float(input("Transaction cost (default 0):") or 0)
+    result = check_arbitrage(market_a, price_a, market_b, price_b, transaction_cost)
+    print(_format_result(result))
 
EOF
)
