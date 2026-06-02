# Open-AutoTools CLI Benchmark

- Run: run_04
- Started: 2026-05-28T00:18:42.086389+00:00
- Finished: 2026-05-28T00:20:14.259235+00:00
- Platform: Windows
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 233.107 | 251.298 | 237.723 | 294.777 | 294.777 |
| Text | autocaps | special | OK | 5 | 229.816 | 239.641 | 238.908 | 253.536 | 253.536 |
| Text | autocaps | mixed | OK | 5 | 239.183 | 261.290 | 261.043 | 273.926 | 273.926 |
| Text | autocaps | unicode | OK | 5 | 229.384 | 237.200 | 231.839 | 248.146 | 248.146 |
| Color | autocolor | hex-default | OK | 5 | 229.240 | 236.873 | 233.945 | 247.189 | 247.189 |
| Color | autocolor | hex-rgb | OK | 5 | 216.038 | 228.763 | 221.828 | 246.734 | 246.734 |
| Color | autocolor | rgb-hsl | OK | 5 | 215.065 | 227.846 | 224.919 | 243.866 | 243.866 |
| Color | autocolor | hsl-rgba | OK | 5 | 225.072 | 255.670 | 234.842 | 337.684 | 337.684 |
| Files | autoconvert | md-json | OK | 5 | 217.412 | 232.120 | 224.860 | 256.282 | 256.282 |
| Network | autoip | basic | OK | 5 | 463.367 | 482.632 | 471.245 | 527.000 | 527.000 |
| Network | autoip | connectivity | OK | 5 | 655.867 | 697.444 | 696.057 | 767.506 | 767.506 |
| Network | autoip | dns | OK | 5 | 823.331 | 943.825 | 977.273 | 1003.610 | 1003.610 |
| Network | autoip | ports | OK | 5 | 702.253 | 920.253 | 922.856 | 1095.581 | 1095.581 |
| Text | autolower | basic | OK | 5 | 358.084 | 382.819 | 360.453 | 437.102 | 437.102 |
| Text | autolower | special | OK | 5 | 341.163 | 431.953 | 445.959 | 486.468 | 486.468 |
| Text | autolower | mixed | OK | 5 | 333.006 | 391.346 | 350.086 | 525.974 | 525.974 |
| Text | autolower | unicode | OK | 5 | 307.532 | 368.560 | 346.552 | 488.263 | 488.263 |
| Text | autonote | add-note | OK | 5 | 324.927 | 378.538 | 369.728 | 460.592 | 460.592 |
| Text | autonote | list-notes | OK | 5 | 269.577 | 355.726 | 363.177 | 421.999 | 421.999 |
| Security | autopassword | basic | OK | 5 | 303.317 | 398.711 | 430.965 | 460.928 | 460.928 |
| Security | autopassword | length | OK | 5 | 359.027 | 399.159 | 386.722 | 470.006 | 470.006 |
| Security | autopassword | no-special | OK | 5 | 286.447 | 324.541 | 316.710 | 407.508 | 407.508 |
| Security | autopassword | no-numbers | OK | 5 | 313.689 | 394.616 | 383.729 | 485.752 | 485.752 |
| Security | autopassword | no-uppercase | OK | 5 | 292.727 | 382.449 | 398.856 | 490.503 | 490.503 |
| Security | autopassword | min-special | OK | 5 | 255.995 | 404.404 | 443.562 | 559.279 | 559.279 |
| Security | autopassword | min-numbers | OK | 5 | 342.700 | 411.001 | 383.102 | 555.444 | 555.444 |
| Security | autopassword | analysis | OK | 5 | 386.477 | 488.182 | 479.203 | 596.054 | 596.054 |
| Security | autopassword | encryption | OK | 5 | 283.848 | 460.760 | 488.819 | 589.528 | 589.528 |
| Task | autotodo | autotodo-list | OK | 5 | 265.405 | 320.675 | 314.737 | 379.016 | 379.016 |
| Conversion | autounit | length-meters-feet | OK | 5 | 837.564 | 930.297 | 879.646 | 1125.780 | 1125.780 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 926.539 | 950.928 | 942.415 | 998.241 | 998.241 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 660.840 | 795.792 | 738.029 | 1001.798 | 1001.798 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 634.205 | 676.762 | 678.582 | 740.662 | 740.662 |
| Files | autozip | zip-readme | OK | 5 | 240.121 | 275.037 | 273.026 | 313.549 | 313.549 |
