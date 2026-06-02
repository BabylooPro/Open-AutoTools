# Open-AutoTools CLI Benchmark

- Run: run_20260602t0018z
- Started: 2026-06-02T00:18:25.204473+00:00
- Finished: 2026-06-02T00:19:38.559953+00:00
- Platform: Windows
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 215.041 | 231.959 | 230.381 | 253.276 | 253.276 |
| Text | autocaps | special | OK | 5 | 216.378 | 236.877 | 235.379 | 259.689 | 259.689 |
| Text | autocaps | mixed | OK | 5 | 326.148 | 426.446 | 453.250 | 460.061 | 460.061 |
| Text | autocaps | unicode | OK | 5 | 262.779 | 355.433 | 369.627 | 466.454 | 466.454 |
| Color | autocolor | hex-default | OK | 5 | 217.621 | 271.245 | 269.707 | 343.101 | 343.101 |
| Color | autocolor | hex-rgb | OK | 5 | 217.671 | 239.697 | 219.667 | 320.633 | 320.633 |
| Color | autocolor | rgb-hsl | OK | 5 | 222.604 | 233.749 | 230.287 | 246.523 | 246.523 |
| Color | autocolor | hsl-rgba | OK | 5 | 223.480 | 228.566 | 227.986 | 235.723 | 235.723 |
| Files | autoconvert | md-json | OK | 5 | 212.012 | 225.058 | 219.071 | 261.628 | 261.628 |
| Network | autoip | basic | OK | 5 | 446.696 | 460.637 | 464.404 | 475.035 | 475.035 |
| Network | autoip | connectivity | OK | 5 | 688.006 | 734.512 | 711.032 | 818.107 | 818.107 |
| Network | autoip | dns | OK | 5 | 604.789 | 613.208 | 612.051 | 621.033 | 621.033 |
| Network | autoip | ports | OK | 5 | 613.568 | 636.881 | 614.879 | 689.425 | 689.425 |
| Text | autolower | basic | OK | 5 | 217.007 | 251.774 | 222.034 | 349.892 | 349.892 |
| Text | autolower | special | OK | 5 | 266.575 | 309.640 | 325.031 | 332.645 | 332.645 |
| Text | autolower | mixed | OK | 5 | 246.837 | 281.954 | 273.180 | 319.016 | 319.016 |
| Text | autolower | unicode | OK | 5 | 233.090 | 277.669 | 295.492 | 330.423 | 330.423 |
| Text | autonote | add-note | OK | 5 | 195.652 | 231.021 | 243.055 | 267.267 | 267.267 |
| Text | autonote | list-notes | OK | 5 | 201.055 | 250.609 | 261.410 | 312.500 | 312.500 |
| Security | autopassword | basic | OK | 5 | 254.014 | 286.949 | 300.298 | 319.903 | 319.903 |
| Security | autopassword | length | OK | 5 | 225.071 | 248.098 | 236.475 | 284.112 | 284.112 |
| Security | autopassword | no-special | OK | 5 | 215.999 | 229.903 | 221.141 | 259.727 | 259.727 |
| Security | autopassword | no-numbers | OK | 5 | 214.007 | 223.733 | 225.117 | 237.320 | 237.320 |
| Security | autopassword | no-uppercase | OK | 5 | 202.123 | 212.334 | 208.836 | 226.719 | 226.719 |
| Security | autopassword | min-special | OK | 5 | 203.559 | 209.146 | 208.840 | 215.371 | 215.371 |
| Security | autopassword | min-numbers | OK | 5 | 210.915 | 224.098 | 217.952 | 253.401 | 253.401 |
| Security | autopassword | analysis | OK | 5 | 209.631 | 212.923 | 211.305 | 217.776 | 217.776 |
| Security | autopassword | encryption | OK | 5 | 204.382 | 246.404 | 224.015 | 352.375 | 352.375 |
| Task | autotodo | autotodo-list | OK | 5 | 194.298 | 203.293 | 202.429 | 214.567 | 214.567 |
| Conversion | autounit | length-meters-feet | OK | 5 | 628.416 | 648.512 | 653.214 | 667.490 | 667.490 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 634.605 | 666.437 | 648.975 | 736.896 | 736.896 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 639.434 | 654.232 | 654.330 | 666.356 | 666.356 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 650.347 | 837.091 | 691.265 | 1157.442 | 1157.442 |
| Files | autozip | zip-readme | OK | 5 | 220.372 | 341.901 | 235.438 | 567.850 | 567.850 |
