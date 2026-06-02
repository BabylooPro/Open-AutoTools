# Open-AutoTools CLI Benchmark

- Run: run_20260527t2233z
- Started: 2026-05-27T22:33:47.522975+00:00
- Finished: 2026-05-27T22:38:23.512766+00:00
- Platform: Windows
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 1178.851 | 1281.379 | 1256.531 | 1451.216 | 1451.216 |
| Text | autocaps | special | OK | 5 | 1175.090 | 1202.571 | 1196.471 | 1245.617 | 1245.617 |
| Text | autocaps | mixed | OK | 5 | 1232.489 | 1301.568 | 1284.388 | 1370.622 | 1370.622 |
| Text | autocaps | unicode | OK | 5 | 1150.381 | 1213.139 | 1222.028 | 1284.613 | 1284.613 |
| Color | autocolor | hex-default | OK | 5 | 1236.349 | 1283.615 | 1289.610 | 1310.141 | 1310.141 |
| Color | autocolor | hex-rgb | OK | 5 | 1271.325 | 1525.960 | 1323.900 | 2144.503 | 2144.503 |
| Color | autocolor | rgb-hsl | OK | 5 | 1312.505 | 1334.102 | 1317.566 | 1405.644 | 1405.644 |
| Color | autocolor | hsl-rgba | OK | 5 | 1269.269 | 1314.821 | 1323.482 | 1339.616 | 1339.616 |
| Files | autoconvert | md-json | OK | 5 | 1328.010 | 1376.010 | 1376.053 | 1445.128 | 1445.128 |
| Network | autoip | basic | OK | 5 | 1319.519 | 1342.698 | 1337.355 | 1383.127 | 1383.127 |
| Network | autoip | connectivity | OK | 5 | 1502.444 | 1525.902 | 1523.211 | 1558.516 | 1558.516 |
| Network | autoip | dns | OK | 5 | 1286.438 | 1372.048 | 1336.364 | 1587.519 | 1587.519 |
| Network | autoip | ports | OK | 5 | 1261.172 | 1524.311 | 1370.127 | 2241.992 | 2241.992 |
| Text | autolower | basic | OK | 5 | 1254.279 | 1324.135 | 1349.613 | 1380.565 | 1380.565 |
| Text | autolower | special | OK | 5 | 1276.508 | 1318.890 | 1309.220 | 1367.317 | 1367.317 |
| Text | autolower | mixed | OK | 5 | 1304.671 | 1346.743 | 1353.158 | 1388.268 | 1388.268 |
| Text | autolower | unicode | OK | 5 | 1271.090 | 1342.895 | 1340.396 | 1403.055 | 1403.055 |
| Text | autonote | add-note | OK | 5 | 1283.940 | 1344.459 | 1329.678 | 1424.400 | 1424.400 |
| Text | autonote | list-notes | OK | 5 | 1232.284 | 1314.716 | 1308.966 | 1415.493 | 1415.493 |
| Security | autopassword | basic | OK | 5 | 1285.409 | 1356.924 | 1331.559 | 1503.783 | 1503.783 |
| Security | autopassword | length | OK | 5 | 1274.557 | 1623.714 | 1442.342 | 2243.575 | 2243.575 |
| Security | autopassword | no-special | OK | 5 | 1141.842 | 1322.174 | 1360.448 | 1418.887 | 1418.887 |
| Security | autopassword | no-numbers | OK | 5 | 1334.208 | 1361.575 | 1369.917 | 1386.796 | 1386.796 |
| Security | autopassword | no-uppercase | OK | 5 | 1217.811 | 1328.152 | 1335.960 | 1404.926 | 1404.926 |
| Security | autopassword | min-special | OK | 5 | 1249.423 | 1290.756 | 1273.777 | 1346.993 | 1346.993 |
| Security | autopassword | min-numbers | OK | 5 | 1256.672 | 1335.479 | 1345.235 | 1419.496 | 1419.496 |
| Security | autopassword | analysis | OK | 5 | 1424.658 | 1481.680 | 1489.676 | 1516.183 | 1516.183 |
| Security | autopassword | encryption | OK | 5 | 1179.165 | 1274.993 | 1274.036 | 1350.624 | 1350.624 |
| Task | autotodo | autotodo-list | OK | 5 | 1209.021 | 1487.476 | 1285.478 | 2275.728 | 2275.728 |
| Conversion | autounit | length-meters-feet | OK | 5 | 1204.700 | 1257.932 | 1224.824 | 1363.756 | 1363.756 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 1164.843 | 1291.132 | 1314.630 | 1440.735 | 1440.735 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 1274.964 | 1303.979 | 1303.467 | 1326.065 | 1326.065 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 1177.123 | 1246.348 | 1208.922 | 1398.051 | 1398.051 |
| Files | autozip | zip-readme | OK | 5 | 1211.336 | 1272.775 | 1235.849 | 1393.301 | 1393.301 |
