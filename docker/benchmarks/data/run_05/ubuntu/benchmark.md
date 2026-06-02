# Open-AutoTools CLI Benchmark

- Run: run_05
- Started: 2026-06-02T00:18:25.156537+00:00
- Finished: 2026-06-02T00:19:07.619014+00:00
- Platform: Ubuntu
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 104.169 | 136.938 | 120.771 | 206.091 | 206.091 |
| Text | autocaps | special | OK | 5 | 107.624 | 117.023 | 116.483 | 130.655 | 130.655 |
| Text | autocaps | mixed | OK | 5 | 109.717 | 121.605 | 117.119 | 153.181 | 153.181 |
| Text | autocaps | unicode | OK | 5 | 109.532 | 124.449 | 119.637 | 144.278 | 144.278 |
| Color | autocolor | hex-default | OK | 5 | 238.134 | 407.920 | 433.193 | 489.153 | 489.153 |
| Color | autocolor | hex-rgb | OK | 5 | 236.329 | 315.774 | 303.701 | 452.065 | 452.065 |
| Color | autocolor | rgb-hsl | OK | 5 | 102.572 | 125.588 | 121.776 | 155.367 | 155.367 |
| Color | autocolor | hsl-rgba | OK | 5 | 114.826 | 164.251 | 135.303 | 288.409 | 288.409 |
| Files | autoconvert | md-json | OK | 5 | 130.105 | 138.505 | 138.311 | 147.799 | 147.799 |
| Network | autoip | basic | OK | 5 | 193.219 | 229.030 | 202.488 | 328.510 | 328.510 |
| Network | autoip | connectivity | OK | 5 | 424.638 | 441.167 | 430.807 | 477.766 | 477.766 |
| Network | autoip | dns | OK | 5 | 365.160 | 373.253 | 368.416 | 391.266 | 391.266 |
| Network | autoip | ports | OK | 5 | 364.333 | 373.766 | 371.524 | 386.433 | 386.433 |
| Text | autolower | basic | OK | 5 | 111.910 | 151.753 | 126.862 | 225.222 | 225.222 |
| Text | autolower | special | OK | 5 | 108.609 | 117.438 | 112.525 | 134.756 | 134.756 |
| Text | autolower | mixed | OK | 5 | 106.322 | 145.476 | 127.517 | 243.741 | 243.741 |
| Text | autolower | unicode | OK | 5 | 105.255 | 128.469 | 122.189 | 160.356 | 160.356 |
| Text | autonote | add-note | OK | 5 | 101.619 | 118.456 | 115.479 | 146.494 | 146.494 |
| Text | autonote | list-notes | OK | 5 | 100.016 | 116.037 | 114.575 | 132.857 | 132.857 |
| Security | autopassword | basic | OK | 5 | 115.902 | 126.857 | 127.874 | 142.685 | 142.685 |
| Security | autopassword | length | OK | 5 | 113.638 | 129.091 | 118.958 | 159.934 | 159.934 |
| Security | autopassword | no-special | OK | 5 | 111.529 | 117.854 | 113.193 | 134.912 | 134.912 |
| Security | autopassword | no-numbers | OK | 5 | 109.570 | 117.109 | 113.109 | 136.972 | 136.972 |
| Security | autopassword | no-uppercase | OK | 5 | 117.278 | 125.214 | 123.020 | 139.141 | 139.141 |
| Security | autopassword | min-special | OK | 5 | 105.102 | 119.122 | 120.600 | 129.764 | 129.764 |
| Security | autopassword | min-numbers | OK | 5 | 110.854 | 118.806 | 115.859 | 127.516 | 127.516 |
| Security | autopassword | analysis | OK | 5 | 118.131 | 144.323 | 130.570 | 181.497 | 181.497 |
| Security | autopassword | encryption | OK | 5 | 113.891 | 123.039 | 115.612 | 149.211 | 149.211 |
| Task | autotodo | autotodo-list | OK | 5 | 102.555 | 109.893 | 110.716 | 114.902 | 114.902 |
| Conversion | autounit | length-meters-feet | OK | 5 | 438.394 | 458.693 | 455.080 | 480.635 | 480.635 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 390.493 | 404.067 | 405.246 | 418.525 | 418.525 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 377.803 | 388.501 | 387.749 | 396.808 | 396.808 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 364.768 | 401.188 | 403.496 | 447.130 | 447.130 |
| Files | autozip | zip-readme | OK | 5 | 105.624 | 143.103 | 123.110 | 253.699 | 253.699 |
