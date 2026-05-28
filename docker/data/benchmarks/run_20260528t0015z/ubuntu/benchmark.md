# Open-AutoTools CLI Benchmark

- Run: run_20260528t0015z
- Started: 2026-05-28T00:15:18.850948+00:00
- Finished: 2026-05-28T00:16:00.449040+00:00
- Platform: Ubuntu
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 149.971 | 174.785 | 170.566 | 199.837 | 199.837 |
| Text | autocaps | special | OK | 5 | 120.204 | 160.108 | 165.129 | 184.637 | 184.637 |
| Text | autocaps | mixed | OK | 5 | 124.371 | 131.650 | 125.321 | 152.269 | 152.269 |
| Text | autocaps | unicode | OK | 5 | 109.403 | 142.508 | 151.718 | 158.889 | 158.889 |
| Color | autocolor | hex-default | OK | 5 | 116.480 | 138.226 | 130.985 | 164.825 | 164.825 |
| Color | autocolor | hex-rgb | OK | 5 | 122.531 | 141.765 | 125.424 | 203.605 | 203.605 |
| Color | autocolor | rgb-hsl | OK | 5 | 116.233 | 125.102 | 125.745 | 130.476 | 130.476 |
| Color | autocolor | hsl-rgba | OK | 5 | 115.472 | 138.423 | 138.849 | 177.185 | 177.185 |
| Files | autoconvert | md-json | OK | 5 | 130.995 | 147.819 | 146.900 | 166.534 | 166.534 |
| Network | autoip | basic | OK | 5 | 218.620 | 246.517 | 249.140 | 278.509 | 278.509 |
| Network | autoip | connectivity | OK | 5 | 386.543 | 426.816 | 433.160 | 466.961 | 466.961 |
| Network | autoip | dns | OK | 5 | 372.177 | 387.147 | 384.284 | 402.861 | 402.861 |
| Network | autoip | ports | OK | 5 | 355.592 | 365.165 | 367.324 | 368.389 | 368.389 |
| Text | autolower | basic | OK | 5 | 110.088 | 117.653 | 113.956 | 132.923 | 132.923 |
| Text | autolower | special | OK | 5 | 120.722 | 132.977 | 135.215 | 140.880 | 140.880 |
| Text | autolower | mixed | OK | 5 | 126.210 | 135.893 | 132.819 | 154.864 | 154.864 |
| Text | autolower | unicode | OK | 5 | 124.035 | 140.148 | 130.367 | 171.363 | 171.363 |
| Text | autonote | add-note | OK | 5 | 110.198 | 126.099 | 123.770 | 144.850 | 144.850 |
| Text | autonote | list-notes | OK | 5 | 116.471 | 133.824 | 126.563 | 158.193 | 158.193 |
| Security | autopassword | basic | OK | 5 | 120.061 | 140.164 | 129.826 | 183.368 | 183.368 |
| Security | autopassword | length | OK | 5 | 123.479 | 140.239 | 133.874 | 161.394 | 161.394 |
| Security | autopassword | no-special | OK | 5 | 118.002 | 130.453 | 127.277 | 151.310 | 151.310 |
| Security | autopassword | no-numbers | OK | 5 | 117.494 | 137.610 | 126.500 | 176.289 | 176.289 |
| Security | autopassword | no-uppercase | OK | 5 | 121.146 | 131.676 | 133.737 | 136.557 | 136.557 |
| Security | autopassword | min-special | OK | 5 | 127.765 | 143.491 | 136.479 | 169.431 | 169.431 |
| Security | autopassword | min-numbers | OK | 5 | 115.442 | 126.241 | 121.468 | 150.200 | 150.200 |
| Security | autopassword | analysis | OK | 5 | 123.700 | 166.496 | 163.615 | 193.987 | 193.987 |
| Security | autopassword | encryption | OK | 5 | 128.770 | 152.070 | 161.060 | 169.063 | 169.063 |
| Task | autotodo | autotodo-list | OK | 5 | 107.689 | 118.222 | 114.964 | 132.239 | 132.239 |
| Conversion | autounit | length-meters-feet | OK | 5 | 395.593 | 427.239 | 422.690 | 461.860 | 461.860 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 404.307 | 424.451 | 420.918 | 450.215 | 450.215 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 367.586 | 381.522 | 380.767 | 394.501 | 394.501 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 373.118 | 409.088 | 407.371 | 463.640 | 463.640 |
| Files | autozip | zip-readme | OK | 5 | 99.975 | 115.439 | 114.590 | 134.041 | 134.041 |
