# Open-AutoTools CLI Benchmark

- Run: run_20260527t2226z
- Started: 2026-05-27T22:26:47.312114+00:00
- Finished: 2026-05-27T22:31:20.267536+00:00
- Platform: macOS
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 1232.769 | 1293.546 | 1272.936 | 1371.101 | 1371.101 |
| Text | autocaps | special | OK | 5 | 1181.914 | 1245.725 | 1236.942 | 1307.883 | 1307.883 |
| Text | autocaps | mixed | OK | 5 | 1170.154 | 1465.561 | 1405.039 | 1937.753 | 1937.753 |
| Text | autocaps | unicode | OK | 5 | 1237.267 | 1259.684 | 1246.536 | 1326.422 | 1326.422 |
| Color | autocolor | hex-default | OK | 5 | 1125.210 | 1212.020 | 1166.353 | 1308.366 | 1308.366 |
| Color | autocolor | hex-rgb | OK | 5 | 1187.097 | 1253.598 | 1265.713 | 1298.682 | 1298.682 |
| Color | autocolor | rgb-hsl | OK | 5 | 1195.105 | 1226.531 | 1221.666 | 1271.951 | 1271.951 |
| Color | autocolor | hsl-rgba | OK | 5 | 1191.393 | 1270.904 | 1260.896 | 1338.256 | 1338.256 |
| Files | autoconvert | md-json | OK | 5 | 1165.307 | 1233.498 | 1244.280 | 1291.379 | 1291.379 |
| Network | autoip | basic | OK | 5 | 1174.501 | 1209.409 | 1194.677 | 1267.682 | 1267.682 |
| Network | autoip | connectivity | OK | 5 | 1427.294 | 1560.483 | 1496.193 | 1901.947 | 1901.947 |
| Network | autoip | dns | OK | 5 | 1299.827 | 1346.239 | 1339.083 | 1429.323 | 1429.323 |
| Network | autoip | ports | OK | 5 | 1239.902 | 1350.126 | 1319.629 | 1557.465 | 1557.465 |
| Text | autolower | basic | OK | 5 | 1265.445 | 1313.324 | 1314.630 | 1343.752 | 1343.752 |
| Text | autolower | special | OK | 5 | 1313.939 | 1371.458 | 1360.647 | 1418.792 | 1418.792 |
| Text | autolower | mixed | OK | 5 | 1267.443 | 1307.825 | 1292.910 | 1386.085 | 1386.085 |
| Text | autolower | unicode | OK | 5 | 1259.981 | 1340.216 | 1324.521 | 1419.829 | 1419.829 |
| Text | autonote | add-note | OK | 5 | 1269.255 | 1303.876 | 1297.578 | 1379.023 | 1379.023 |
| Text | autonote | list-notes | OK | 5 | 1320.912 | 1568.413 | 1387.842 | 2318.949 | 2318.949 |
| Security | autopassword | basic | OK | 5 | 1186.398 | 1312.684 | 1376.581 | 1394.155 | 1394.155 |
| Security | autopassword | length | OK | 5 | 1218.026 | 1303.312 | 1286.564 | 1381.313 | 1381.313 |
| Security | autopassword | no-special | OK | 5 | 1272.012 | 1311.138 | 1299.603 | 1362.227 | 1362.227 |
| Security | autopassword | no-numbers | OK | 5 | 1282.942 | 1340.708 | 1354.599 | 1374.901 | 1374.901 |
| Security | autopassword | no-uppercase | OK | 5 | 1268.336 | 1317.879 | 1292.688 | 1383.904 | 1383.904 |
| Security | autopassword | min-special | OK | 5 | 1238.807 | 1356.109 | 1371.483 | 1466.071 | 1466.071 |
| Security | autopassword | min-numbers | OK | 5 | 1225.167 | 1302.450 | 1250.426 | 1408.395 | 1408.395 |
| Security | autopassword | analysis | OK | 5 | 1492.174 | 1817.561 | 1695.497 | 2541.458 | 2541.458 |
| Security | autopassword | encryption | OK | 5 | 1233.120 | 1302.395 | 1294.084 | 1404.770 | 1404.770 |
| Task | autotodo | autotodo-list | OK | 5 | 1232.480 | 1256.830 | 1261.099 | 1270.232 | 1270.232 |
| Conversion | autounit | length-meters-feet | OK | 5 | 1225.554 | 1258.240 | 1263.839 | 1293.890 | 1293.890 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 1198.239 | 1260.587 | 1257.057 | 1348.685 | 1348.685 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 1276.164 | 1295.568 | 1296.973 | 1329.218 | 1329.218 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 1252.257 | 1312.283 | 1331.736 | 1371.145 | 1371.145 |
| Files | autozip | zip-readme | OK | 5 | 1225.332 | 1321.455 | 1273.561 | 1475.651 | 1475.651 |
