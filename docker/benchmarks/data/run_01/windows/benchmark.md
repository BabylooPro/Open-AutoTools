# Open-AutoTools CLI Benchmark

- Run: run_01
- Started: 2026-05-27T22:26:47.263138+00:00
- Finished: 2026-05-27T22:31:19.664990+00:00
- Platform: Windows
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 1204.013 | 1293.367 | 1288.828 | 1356.690 | 1356.690 |
| Text | autocaps | special | OK | 5 | 1181.920 | 1247.190 | 1231.364 | 1296.542 | 1296.542 |
| Text | autocaps | mixed | OK | 5 | 1175.686 | 1469.709 | 1413.335 | 2089.559 | 2089.559 |
| Text | autocaps | unicode | OK | 5 | 1241.418 | 1257.932 | 1251.521 | 1288.210 | 1288.210 |
| Color | autocolor | hex-default | OK | 5 | 1153.192 | 1209.569 | 1209.400 | 1304.992 | 1304.992 |
| Color | autocolor | hex-rgb | OK | 5 | 1188.746 | 1250.819 | 1265.333 | 1298.083 | 1298.083 |
| Color | autocolor | rgb-hsl | OK | 5 | 1194.180 | 1223.884 | 1220.246 | 1248.291 | 1248.291 |
| Color | autocolor | hsl-rgba | OK | 5 | 1220.599 | 1272.198 | 1249.162 | 1342.310 | 1342.310 |
| Files | autoconvert | md-json | OK | 5 | 1134.344 | 1222.304 | 1217.767 | 1295.370 | 1295.370 |
| Network | autoip | basic | OK | 5 | 1180.501 | 1205.616 | 1196.430 | 1253.952 | 1253.952 |
| Network | autoip | connectivity | OK | 5 | 1428.175 | 1542.449 | 1496.552 | 1817.417 | 1817.417 |
| Network | autoip | dns | OK | 5 | 1304.975 | 1325.520 | 1329.712 | 1345.084 | 1345.084 |
| Network | autoip | ports | OK | 5 | 1204.068 | 1298.196 | 1289.309 | 1398.412 | 1398.412 |
| Text | autolower | basic | OK | 5 | 1255.525 | 1284.124 | 1276.182 | 1334.490 | 1334.490 |
| Text | autolower | special | OK | 5 | 1314.897 | 1359.498 | 1347.598 | 1424.751 | 1424.751 |
| Text | autolower | mixed | OK | 5 | 1273.337 | 1345.296 | 1338.378 | 1416.496 | 1416.496 |
| Text | autolower | unicode | OK | 5 | 1224.900 | 1326.735 | 1310.119 | 1459.424 | 1459.424 |
| Text | autonote | add-note | OK | 5 | 1272.295 | 1288.975 | 1288.217 | 1299.950 | 1299.950 |
| Text | autonote | list-notes | OK | 5 | 1255.262 | 1533.571 | 1405.199 | 2154.916 | 2154.916 |
| Security | autopassword | basic | OK | 5 | 1254.586 | 1289.103 | 1284.853 | 1323.023 | 1323.023 |
| Security | autopassword | length | OK | 5 | 1296.094 | 1321.707 | 1314.413 | 1369.626 | 1369.626 |
| Security | autopassword | no-special | OK | 5 | 1222.189 | 1333.714 | 1342.895 | 1417.349 | 1417.349 |
| Security | autopassword | no-numbers | OK | 5 | 1316.705 | 1339.042 | 1334.682 | 1360.165 | 1360.165 |
| Security | autopassword | no-uppercase | OK | 5 | 1284.865 | 1375.968 | 1355.531 | 1485.937 | 1485.937 |
| Security | autopassword | min-special | OK | 5 | 1285.191 | 1385.438 | 1372.215 | 1470.439 | 1470.439 |
| Security | autopassword | min-numbers | OK | 5 | 1221.162 | 1297.246 | 1255.343 | 1477.140 | 1477.140 |
| Security | autopassword | analysis | OK | 5 | 1494.834 | 1825.366 | 1694.118 | 2467.120 | 2467.120 |
| Security | autopassword | encryption | OK | 5 | 1268.115 | 1312.257 | 1318.819 | 1364.581 | 1364.581 |
| Task | autotodo | autotodo-list | OK | 5 | 1222.897 | 1250.415 | 1255.453 | 1291.085 | 1291.085 |
| Conversion | autounit | length-meters-feet | OK | 5 | 1224.755 | 1269.071 | 1245.845 | 1382.279 | 1382.279 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 1183.545 | 1250.094 | 1226.672 | 1362.565 | 1362.565 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 1271.668 | 1321.102 | 1324.389 | 1375.766 | 1375.766 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 1204.399 | 1318.302 | 1308.436 | 1406.258 | 1406.258 |
| Files | autozip | zip-readme | OK | 5 | 1208.628 | 1285.394 | 1264.645 | 1408.065 | 1408.065 |
