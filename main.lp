Maximize
 obj: sum {i in 1..n} (sum {j in 1..m} (Lij * xij)) - sum {i in 1..n} (fi * yi)
Subject To
 c1{j in 1..m}: sum {i in 1..n} xij <= 1
 c2{i in 1..n}: sum {j in 1..m} (dj * xij) <= Capi * yi
Bounds
 0 <= xij <= 1 forall i in 1..n, j in 1..m
Binary
 yi forall i in 1..n
End
