# Open-AutoTools CLI Benchmark

- Run: run_20260528t0015z
- Started: 2026-05-28T00:15:18.931707+00:00
- Finished: 2026-05-28T00:16:33.313013+00:00
- Platform: macOS
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 230.376 | 263.221 | 261.299 | 294.404 | 294.404 |
| Text | autocaps | special | OK | 5 | 231.391 | 237.229 | 231.933 | 247.125 | 247.125 |
| Text | autocaps | mixed | OK | 5 | 220.114 | 235.683 | 233.621 | 260.047 | 260.047 |
| Text | autocaps | unicode | OK | 5 | 227.202 | 250.051 | 232.689 | 283.308 | 283.308 |
| Color | autocolor | hex-default | OK | 5 | 227.293 | 237.644 | 240.685 | 244.693 | 244.693 |
| Color | autocolor | hex-rgb | OK | 5 | 226.936 | 238.816 | 240.713 | 250.226 | 250.226 |
| Color | autocolor | rgb-hsl | OK | 5 | 222.663 | 243.964 | 250.317 | 257.280 | 257.280 |
| Color | autocolor | hsl-rgba | OK | 5 | 225.620 | 248.899 | 250.062 | 264.765 | 264.765 |
| Files | autoconvert | md-json | OK | 5 | 244.094 | 251.574 | 249.678 | 259.692 | 259.692 |
| Network | autoip | basic | OK | 5 | 452.165 | 469.697 | 466.845 | 491.442 | 491.442 |
| Network | autoip | connectivity | OK | 5 | 656.685 | 674.756 | 668.155 | 696.041 | 696.041 |
| Network | autoip | dns | OK | 5 | 609.567 | 626.122 | 621.427 | 645.949 | 645.949 |
| Network | autoip | ports | OK | 5 | 579.038 | 623.983 | 626.696 | 652.684 | 652.684 |
| Text | autolower | basic | OK | 5 | 219.962 | 243.518 | 238.401 | 268.630 | 268.630 |
| Text | autolower | special | OK | 5 | 248.357 | 292.127 | 300.268 | 344.848 | 344.848 |
| Text | autolower | mixed | OK | 5 | 245.554 | 282.106 | 296.410 | 315.478 | 315.478 |
| Text | autolower | unicode | OK | 5 | 230.674 | 287.083 | 301.616 | 328.819 | 328.819 |
| Text | autonote | add-note | OK | 5 | 197.533 | 228.733 | 239.231 | 251.675 | 251.675 |
| Text | autonote | list-notes | OK | 5 | 205.677 | 257.910 | 255.849 | 298.876 | 298.876 |
| Security | autopassword | basic | OK | 5 | 251.605 | 280.817 | 283.413 | 297.429 | 297.429 |
| Security | autopassword | length | OK | 5 | 208.801 | 244.552 | 246.091 | 284.990 | 284.990 |
| Security | autopassword | no-special | OK | 5 | 225.856 | 267.004 | 245.464 | 348.279 | 348.279 |
| Security | autopassword | no-numbers | OK | 5 | 228.555 | 235.261 | 232.243 | 247.507 | 247.507 |
| Security | autopassword | no-uppercase | OK | 5 | 226.320 | 357.645 | 234.644 | 781.965 | 781.965 |
| Security | autopassword | min-special | OK | 5 | 225.861 | 378.046 | 292.836 | 628.501 | 628.501 |
| Security | autopassword | min-numbers | OK | 5 | 226.251 | 237.922 | 239.391 | 250.590 | 250.590 |
| Security | autopassword | analysis | OK | 5 | 227.071 | 241.308 | 241.662 | 248.920 | 248.920 |
| Security | autopassword | encryption | OK | 5 | 229.868 | 272.787 | 236.074 | 396.056 | 396.056 |
| Task | autotodo | autotodo-list | OK | 5 | 188.984 | 222.634 | 204.741 | 271.162 | 271.162 |
| Conversion | autounit | length-meters-feet | OK | 5 | 696.641 | 714.805 | 723.404 | 726.333 | 726.333 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 696.608 | 722.710 | 724.606 | 739.573 | 739.573 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 682.922 | 715.552 | 692.739 | 803.246 | 803.246 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 679.435 | 714.405 | 706.808 | 779.940 | 779.940 |
| Files | autozip | zip-readme | OK | 5 | 282.628 | 304.594 | 300.906 | 334.708 | 334.708 |
