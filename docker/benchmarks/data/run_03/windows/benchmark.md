# Open-AutoTools CLI Benchmark

- Run: run_03
- Started: 2026-05-28T00:15:18.890278+00:00
- Finished: 2026-05-28T00:16:32.927420+00:00
- Platform: Windows
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 231.481 | 263.291 | 260.583 | 293.640 | 293.640 |
| Text | autocaps | special | OK | 5 | 231.513 | 237.112 | 232.045 | 247.127 | 247.127 |
| Text | autocaps | mixed | OK | 5 | 220.155 | 235.565 | 232.798 | 260.413 | 260.413 |
| Text | autocaps | unicode | OK | 5 | 227.418 | 250.245 | 233.204 | 282.980 | 282.980 |
| Color | autocolor | hex-default | OK | 5 | 227.848 | 237.766 | 240.691 | 245.367 | 245.367 |
| Color | autocolor | hex-rgb | OK | 5 | 227.073 | 238.782 | 240.576 | 250.024 | 250.024 |
| Color | autocolor | rgb-hsl | OK | 5 | 222.207 | 243.793 | 249.906 | 257.214 | 257.214 |
| Color | autocolor | hsl-rgba | OK | 5 | 224.988 | 248.674 | 249.947 | 264.764 | 264.764 |
| Files | autoconvert | md-json | OK | 5 | 244.235 | 251.350 | 249.128 | 259.485 | 259.485 |
| Network | autoip | basic | OK | 5 | 451.903 | 469.686 | 466.831 | 490.236 | 490.236 |
| Network | autoip | connectivity | OK | 5 | 655.024 | 675.791 | 668.060 | 701.874 | 701.874 |
| Network | autoip | dns | OK | 5 | 616.863 | 629.697 | 632.568 | 638.361 | 638.361 |
| Network | autoip | ports | OK | 5 | 577.883 | 620.102 | 625.804 | 641.012 | 641.012 |
| Text | autolower | basic | OK | 5 | 219.979 | 243.491 | 237.749 | 268.733 | 268.733 |
| Text | autolower | special | OK | 5 | 248.045 | 294.225 | 302.687 | 350.987 | 350.987 |
| Text | autolower | mixed | OK | 5 | 248.481 | 281.623 | 296.280 | 315.848 | 315.848 |
| Text | autolower | unicode | OK | 5 | 230.535 | 286.677 | 293.905 | 318.783 | 318.783 |
| Text | autonote | add-note | OK | 5 | 193.637 | 229.854 | 240.069 | 255.962 | 255.962 |
| Text | autonote | list-notes | OK | 5 | 223.644 | 259.616 | 261.532 | 289.474 | 289.474 |
| Security | autopassword | basic | OK | 5 | 248.255 | 279.881 | 287.101 | 305.153 | 305.153 |
| Security | autopassword | length | OK | 5 | 212.335 | 238.635 | 231.314 | 280.819 | 280.819 |
| Security | autopassword | no-special | OK | 5 | 226.547 | 266.030 | 254.186 | 332.312 | 332.312 |
| Security | autopassword | no-numbers | OK | 5 | 225.394 | 231.751 | 228.553 | 240.368 | 240.368 |
| Security | autopassword | no-uppercase | OK | 5 | 226.985 | 241.129 | 234.304 | 262.087 | 262.087 |
| Security | autopassword | min-special | OK | 5 | 219.474 | 462.123 | 516.068 | 732.447 | 732.447 |
| Security | autopassword | min-numbers | OK | 5 | 220.832 | 235.421 | 239.873 | 246.534 | 246.534 |
| Security | autopassword | analysis | OK | 5 | 225.173 | 237.743 | 237.974 | 257.658 | 257.658 |
| Security | autopassword | encryption | OK | 5 | 229.163 | 272.774 | 266.252 | 362.203 | 362.203 |
| Task | autotodo | autotodo-list | OK | 5 | 188.359 | 209.268 | 204.607 | 253.965 | 253.965 |
| Conversion | autounit | length-meters-feet | OK | 5 | 658.243 | 693.215 | 698.980 | 710.667 | 710.667 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 700.505 | 725.867 | 708.711 | 764.143 | 764.143 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 692.148 | 712.706 | 694.056 | 769.742 | 769.742 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 673.564 | 719.491 | 737.183 | 750.350 | 750.350 |
| Files | autozip | zip-readme | OK | 5 | 274.856 | 303.239 | 303.096 | 328.327 | 328.327 |
