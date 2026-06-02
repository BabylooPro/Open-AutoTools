# Open-AutoTools CLI Benchmark

- Run: run_05
- Started: 2026-06-02T00:18:25.246439+00:00
- Finished: 2026-06-02T00:19:38.560613+00:00
- Platform: macOS
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 215.161 | 231.919 | 230.824 | 248.807 | 248.807 |
| Text | autocaps | special | OK | 5 | 215.917 | 236.692 | 235.202 | 259.504 | 259.504 |
| Text | autocaps | mixed | OK | 5 | 333.415 | 426.007 | 450.907 | 456.441 | 456.441 |
| Text | autocaps | unicode | OK | 5 | 247.400 | 357.950 | 364.899 | 506.968 | 506.968 |
| Color | autocolor | hex-default | OK | 5 | 217.884 | 269.160 | 269.104 | 338.017 | 338.017 |
| Color | autocolor | hex-rgb | OK | 5 | 216.781 | 239.865 | 219.469 | 321.696 | 321.696 |
| Color | autocolor | rgb-hsl | OK | 5 | 222.183 | 233.754 | 230.296 | 252.998 | 252.998 |
| Color | autocolor | hsl-rgba | OK | 5 | 220.613 | 228.527 | 228.229 | 239.724 | 239.724 |
| Files | autoconvert | md-json | OK | 5 | 213.205 | 225.440 | 219.041 | 262.227 | 262.227 |
| Network | autoip | basic | OK | 5 | 447.146 | 466.013 | 468.300 | 482.046 | 482.046 |
| Network | autoip | connectivity | OK | 5 | 682.903 | 730.813 | 720.719 | 808.173 | 808.173 |
| Network | autoip | dns | OK | 5 | 599.255 | 613.156 | 612.864 | 622.157 | 622.157 |
| Network | autoip | ports | OK | 5 | 616.766 | 640.237 | 628.102 | 678.281 | 678.281 |
| Text | autolower | basic | OK | 5 | 216.832 | 249.824 | 221.319 | 352.016 | 352.016 |
| Text | autolower | special | OK | 5 | 274.095 | 308.719 | 319.705 | 333.406 | 333.406 |
| Text | autolower | mixed | OK | 5 | 248.768 | 281.702 | 281.839 | 305.734 | 305.734 |
| Text | autolower | unicode | OK | 5 | 242.226 | 277.614 | 286.914 | 318.173 | 318.173 |
| Text | autonote | add-note | OK | 5 | 195.779 | 230.839 | 242.154 | 267.211 | 267.211 |
| Text | autonote | list-notes | OK | 5 | 194.347 | 259.205 | 272.896 | 331.865 | 331.865 |
| Security | autopassword | basic | OK | 5 | 228.895 | 268.347 | 249.976 | 325.552 | 325.552 |
| Security | autopassword | length | OK | 5 | 223.344 | 244.733 | 240.198 | 271.703 | 271.703 |
| Security | autopassword | no-special | OK | 5 | 215.528 | 227.776 | 221.658 | 249.271 | 249.271 |
| Security | autopassword | no-numbers | OK | 5 | 214.011 | 222.150 | 217.200 | 237.279 | 237.279 |
| Security | autopassword | no-uppercase | OK | 5 | 202.783 | 212.479 | 208.744 | 228.961 | 228.961 |
| Security | autopassword | min-special | OK | 5 | 203.826 | 209.201 | 209.060 | 215.044 | 215.044 |
| Security | autopassword | min-numbers | OK | 5 | 210.221 | 224.057 | 218.062 | 249.749 | 249.749 |
| Security | autopassword | analysis | OK | 5 | 209.962 | 212.931 | 211.294 | 217.779 | 217.779 |
| Security | autopassword | encryption | OK | 5 | 205.545 | 246.693 | 223.046 | 352.380 | 352.380 |
| Task | autotodo | autotodo-list | OK | 5 | 194.284 | 205.171 | 202.228 | 222.937 | 222.937 |
| Conversion | autounit | length-meters-feet | OK | 5 | 630.829 | 650.045 | 653.173 | 678.551 | 678.551 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 640.105 | 666.689 | 650.300 | 729.048 | 729.048 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 641.033 | 653.457 | 656.824 | 665.014 | 665.014 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 639.290 | 829.038 | 691.592 | 1152.476 | 1152.476 |
| Files | autozip | zip-readme | OK | 5 | 221.070 | 340.897 | 234.646 | 560.149 | 560.149 |
