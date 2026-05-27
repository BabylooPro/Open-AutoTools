# Open-AutoTools CLI Benchmark

- Run: run_20260527t2233z
- Started: 2026-05-27T22:33:47.592234+00:00
- Finished: 2026-05-27T22:38:22.575542+00:00
- Platform: macOS
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 1178.823 | 1270.493 | 1254.968 | 1423.994 | 1423.994 |
| Text | autocaps | special | OK | 5 | 1166.870 | 1201.813 | 1214.311 | 1227.565 | 1227.565 |
| Text | autocaps | mixed | OK | 5 | 1221.141 | 1295.272 | 1290.620 | 1399.989 | 1399.989 |
| Text | autocaps | unicode | OK | 5 | 1154.505 | 1204.501 | 1212.606 | 1254.130 | 1254.130 |
| Color | autocolor | hex-default | OK | 5 | 1219.961 | 1261.897 | 1265.700 | 1304.735 | 1304.735 |
| Color | autocolor | hex-rgb | OK | 5 | 1242.419 | 1552.116 | 1291.343 | 2048.168 | 2048.168 |
| Color | autocolor | rgb-hsl | OK | 5 | 1244.568 | 1318.328 | 1280.553 | 1501.081 | 1501.081 |
| Color | autocolor | hsl-rgba | OK | 5 | 1222.600 | 1318.604 | 1337.864 | 1405.934 | 1405.934 |
| Files | autoconvert | md-json | OK | 5 | 1224.429 | 1297.563 | 1296.862 | 1383.232 | 1383.232 |
| Network | autoip | basic | OK | 5 | 1324.376 | 1354.883 | 1337.410 | 1426.488 | 1426.488 |
| Network | autoip | connectivity | OK | 5 | 1446.052 | 1476.356 | 1468.259 | 1540.848 | 1540.848 |
| Network | autoip | dns | OK | 5 | 1260.961 | 1343.415 | 1294.729 | 1541.911 | 1541.911 |
| Network | autoip | ports | OK | 5 | 1310.765 | 1397.523 | 1372.721 | 1535.254 | 1535.254 |
| Text | autolower | basic | OK | 5 | 1289.185 | 1368.942 | 1350.070 | 1506.271 | 1506.271 |
| Text | autolower | special | OK | 5 | 1265.962 | 1316.288 | 1321.438 | 1392.509 | 1392.509 |
| Text | autolower | mixed | OK | 5 | 1320.831 | 1345.224 | 1348.236 | 1364.206 | 1364.206 |
| Text | autolower | unicode | OK | 5 | 1330.419 | 1374.249 | 1365.935 | 1447.608 | 1447.608 |
| Text | autonote | add-note | OK | 5 | 1290.625 | 1331.214 | 1324.866 | 1368.034 | 1368.034 |
| Text | autonote | list-notes | OK | 5 | 1174.815 | 1334.921 | 1329.577 | 1474.987 | 1474.987 |
| Security | autopassword | basic | OK | 5 | 1268.320 | 1366.744 | 1380.358 | 1428.091 | 1428.091 |
| Security | autopassword | length | OK | 5 | 1312.907 | 1565.842 | 1388.591 | 2401.654 | 2401.654 |
| Security | autopassword | no-special | OK | 5 | 1246.543 | 1298.321 | 1297.137 | 1380.402 | 1380.402 |
| Security | autopassword | no-numbers | OK | 5 | 1342.479 | 1406.467 | 1407.076 | 1460.510 | 1460.510 |
| Security | autopassword | no-uppercase | OK | 5 | 1274.293 | 1345.862 | 1312.964 | 1506.033 | 1506.033 |
| Security | autopassword | min-special | OK | 5 | 1181.486 | 1294.609 | 1294.402 | 1384.764 | 1384.764 |
| Security | autopassword | min-numbers | OK | 5 | 1220.467 | 1276.516 | 1244.926 | 1360.700 | 1360.700 |
| Security | autopassword | analysis | OK | 5 | 1427.323 | 1509.920 | 1499.040 | 1631.729 | 1631.729 |
| Security | autopassword | encryption | OK | 5 | 1204.157 | 1267.821 | 1263.097 | 1318.911 | 1318.911 |
| Task | autotodo | autotodo-list | OK | 5 | 1255.272 | 1499.130 | 1279.062 | 2151.211 | 2151.211 |
| Conversion | autounit | length-meters-feet | OK | 5 | 1222.587 | 1295.362 | 1263.495 | 1432.244 | 1432.244 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 1229.618 | 1262.288 | 1258.329 | 1308.212 | 1308.212 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 1266.329 | 1287.947 | 1268.401 | 1346.282 | 1346.282 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 1192.349 | 1247.259 | 1210.300 | 1381.992 | 1381.992 |
| Files | autozip | zip-readme | OK | 5 | 1224.259 | 1248.712 | 1234.604 | 1300.037 | 1300.037 |
