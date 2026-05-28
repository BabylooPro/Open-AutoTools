# Open-AutoTools CLI Benchmark

- Run: run_20260528t0018z
- Started: 2026-05-28T00:18:41.995157+00:00
- Finished: 2026-05-28T00:19:39.560526+00:00
- Platform: Ubuntu
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 110.999 | 116.951 | 114.270 | 129.800 | 129.800 |
| Text | autocaps | special | OK | 5 | 98.840 | 131.659 | 121.570 | 168.820 | 168.820 |
| Text | autocaps | mixed | OK | 5 | 96.105 | 106.344 | 107.957 | 113.769 | 113.769 |
| Text | autocaps | unicode | OK | 5 | 107.448 | 110.924 | 112.319 | 113.463 | 113.463 |
| Color | autocolor | hex-default | OK | 5 | 111.043 | 143.227 | 142.187 | 173.334 | 173.334 |
| Color | autocolor | hex-rgb | OK | 5 | 115.439 | 136.148 | 142.769 | 154.120 | 154.120 |
| Color | autocolor | rgb-hsl | OK | 5 | 112.165 | 115.353 | 114.362 | 117.985 | 117.985 |
| Color | autocolor | hsl-rgba | OK | 5 | 107.404 | 113.941 | 111.609 | 122.398 | 122.398 |
| Files | autoconvert | md-json | OK | 5 | 126.412 | 142.212 | 143.225 | 161.661 | 161.661 |
| Network | autoip | basic | OK | 5 | 192.161 | 224.738 | 218.040 | 258.691 | 258.691 |
| Network | autoip | connectivity | OK | 5 | 382.402 | 396.543 | 401.812 | 408.557 | 408.557 |
| Network | autoip | dns | OK | 5 | 340.111 | 383.612 | 370.116 | 467.272 | 467.272 |
| Network | autoip | ports | OK | 5 | 331.150 | 350.314 | 354.636 | 367.297 | 367.297 |
| Text | autolower | basic | OK | 5 | 113.592 | 124.624 | 119.044 | 144.443 | 144.443 |
| Text | autolower | special | OK | 5 | 114.630 | 160.559 | 179.582 | 198.328 | 198.328 |
| Text | autolower | mixed | OK | 5 | 107.684 | 118.777 | 122.083 | 122.951 | 122.951 |
| Text | autolower | unicode | OK | 5 | 109.630 | 135.929 | 120.718 | 192.171 | 192.171 |
| Text | autonote | add-note | OK | 5 | 98.444 | 113.064 | 110.694 | 127.569 | 127.569 |
| Text | autonote | list-notes | OK | 5 | 103.953 | 119.067 | 111.285 | 158.272 | 158.272 |
| Security | autopassword | basic | OK | 5 | 113.179 | 251.576 | 266.341 | 370.039 | 370.039 |
| Security | autopassword | length | OK | 5 | 175.406 | 308.955 | 351.064 | 466.527 | 466.527 |
| Security | autopassword | no-special | OK | 5 | 127.729 | 339.939 | 397.572 | 435.442 | 435.442 |
| Security | autopassword | no-numbers | OK | 5 | 293.583 | 413.993 | 428.441 | 499.987 | 499.987 |
| Security | autopassword | no-uppercase | OK | 5 | 124.369 | 266.661 | 205.389 | 432.632 | 432.632 |
| Security | autopassword | min-special | OK | 5 | 224.646 | 395.355 | 402.810 | 562.233 | 562.233 |
| Security | autopassword | min-numbers | OK | 5 | 204.361 | 274.770 | 254.350 | 354.622 | 354.622 |
| Security | autopassword | analysis | OK | 5 | 307.040 | 397.147 | 372.803 | 483.254 | 483.254 |
| Security | autopassword | encryption | OK | 5 | 232.210 | 316.913 | 264.983 | 556.990 | 556.990 |
| Task | autotodo | autotodo-list | OK | 5 | 307.942 | 383.840 | 341.999 | 485.301 | 485.301 |
| Conversion | autounit | length-meters-feet | OK | 5 | 565.591 | 627.140 | 592.510 | 754.242 | 754.242 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 576.077 | 726.317 | 724.425 | 868.470 | 868.470 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 491.564 | 580.502 | 600.835 | 671.494 | 671.494 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 510.365 | 592.716 | 523.015 | 743.227 | 743.227 |
| Files | autozip | zip-readme | OK | 5 | 238.767 | 373.588 | 358.752 | 549.576 | 549.576 |
