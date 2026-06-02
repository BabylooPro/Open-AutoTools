# Open-AutoTools CLI Benchmark

- Run: run_04
- Started: 2026-05-28T00:18:42.158779+00:00
- Finished: 2026-05-28T00:20:15.004596+00:00
- Platform: macOS
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 228.832 | 268.385 | 239.918 | 371.553 | 371.553 |
| Text | autocaps | special | OK | 5 | 234.654 | 252.665 | 238.543 | 291.960 | 291.960 |
| Text | autocaps | mixed | OK | 5 | 246.404 | 266.489 | 258.352 | 294.124 | 294.124 |
| Text | autocaps | unicode | OK | 5 | 234.008 | 243.267 | 239.728 | 252.905 | 252.905 |
| Color | autocolor | hex-default | OK | 5 | 233.544 | 245.384 | 244.518 | 254.934 | 254.934 |
| Color | autocolor | hex-rgb | OK | 5 | 215.986 | 230.016 | 221.793 | 253.065 | 253.065 |
| Color | autocolor | rgb-hsl | OK | 5 | 215.073 | 225.223 | 224.645 | 234.427 | 234.427 |
| Color | autocolor | hsl-rgba | OK | 5 | 229.057 | 257.640 | 235.249 | 337.543 | 337.543 |
| Files | autoconvert | md-json | OK | 5 | 218.191 | 236.229 | 235.541 | 254.116 | 254.116 |
| Network | autoip | basic | OK | 5 | 459.042 | 502.424 | 476.808 | 622.611 | 622.611 |
| Network | autoip | connectivity | OK | 5 | 654.264 | 756.759 | 671.381 | 964.788 | 964.788 |
| Network | autoip | dns | OK | 5 | 851.439 | 908.747 | 891.861 | 1024.102 | 1024.102 |
| Network | autoip | ports | OK | 5 | 673.593 | 837.191 | 829.985 | 941.630 | 941.630 |
| Text | autolower | basic | OK | 5 | 343.822 | 379.139 | 362.713 | 438.553 | 438.553 |
| Text | autolower | special | OK | 5 | 346.920 | 431.933 | 444.475 | 486.268 | 486.268 |
| Text | autolower | mixed | OK | 5 | 325.531 | 390.920 | 350.976 | 531.620 | 531.620 |
| Text | autolower | unicode | OK | 5 | 316.097 | 368.755 | 342.120 | 489.373 | 489.373 |
| Text | autonote | add-note | OK | 5 | 329.144 | 378.095 | 371.074 | 418.076 | 418.076 |
| Text | autonote | list-notes | OK | 5 | 269.768 | 355.545 | 349.628 | 418.765 | 418.765 |
| Security | autopassword | basic | OK | 5 | 304.676 | 406.372 | 423.714 | 490.627 | 490.627 |
| Security | autopassword | length | OK | 5 | 386.399 | 464.366 | 463.153 | 527.750 | 527.750 |
| Security | autopassword | no-special | OK | 5 | 274.459 | 316.244 | 308.123 | 394.924 | 394.924 |
| Security | autopassword | no-numbers | OK | 5 | 327.006 | 396.663 | 390.000 | 481.170 | 481.170 |
| Security | autopassword | no-uppercase | OK | 5 | 292.043 | 390.488 | 399.615 | 538.271 | 538.271 |
| Security | autopassword | min-special | OK | 5 | 289.636 | 410.349 | 435.670 | 552.559 | 552.559 |
| Security | autopassword | min-numbers | OK | 5 | 316.656 | 405.786 | 383.172 | 555.228 | 555.228 |
| Security | autopassword | analysis | OK | 5 | 387.369 | 508.112 | 483.413 | 599.356 | 599.356 |
| Security | autopassword | encryption | OK | 5 | 287.603 | 429.645 | 410.536 | 591.984 | 591.984 |
| Task | autotodo | autotodo-list | OK | 5 | 265.894 | 300.549 | 299.834 | 345.174 | 345.174 |
| Conversion | autounit | length-meters-feet | OK | 5 | 813.863 | 981.639 | 998.256 | 1070.682 | 1070.682 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 920.867 | 973.782 | 931.058 | 1088.426 | 1088.426 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 659.248 | 746.670 | 676.719 | 1008.413 | 1008.413 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 633.875 | 672.400 | 673.541 | 727.882 | 727.882 |
| Files | autozip | zip-readme | OK | 5 | 238.077 | 292.290 | 293.728 | 339.274 | 339.274 |
