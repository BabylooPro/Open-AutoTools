# Open-AutoTools CLI Benchmark

- Run: run_20260527t2226z
- Started: 2026-05-27T22:26:47.135802+00:00
- Finished: 2026-05-27T22:30:08.752022+00:00
- Platform: Ubuntu
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 939.704 | 1024.065 | 1008.203 | 1107.720 | 1107.720 |
| Text | autocaps | special | OK | 5 | 857.410 | 1017.929 | 1043.492 | 1171.430 | 1171.430 |
| Text | autocaps | mixed | OK | 5 | 860.242 | 943.632 | 893.978 | 1063.348 | 1063.348 |
| Text | autocaps | unicode | OK | 5 | 909.927 | 1249.927 | 1051.523 | 1688.027 | 1688.027 |
| Color | autocolor | hex-default | OK | 5 | 888.519 | 980.275 | 976.383 | 1066.330 | 1066.330 |
| Color | autocolor | hex-rgb | OK | 5 | 875.609 | 939.201 | 931.703 | 1045.664 | 1045.664 |
| Color | autocolor | rgb-hsl | OK | 5 | 850.496 | 910.278 | 937.018 | 960.893 | 960.893 |
| Color | autocolor | hsl-rgba | OK | 5 | 873.452 | 905.192 | 884.765 | 950.322 | 950.322 |
| Files | autoconvert | md-json | OK | 5 | 844.864 | 904.995 | 896.371 | 964.929 | 964.929 |
| Network | autoip | basic | OK | 5 | 848.431 | 937.887 | 947.763 | 1027.782 | 1027.782 |
| Network | autoip | connectivity | OK | 5 | 1044.293 | 1221.840 | 1233.823 | 1396.110 | 1396.110 |
| Network | autoip | dns | OK | 5 | 868.523 | 964.334 | 980.428 | 1012.074 | 1012.074 |
| Network | autoip | ports | OK | 5 | 858.557 | 960.417 | 941.564 | 1120.659 | 1120.659 |
| Text | autolower | basic | OK | 5 | 922.291 | 956.914 | 936.330 | 1010.435 | 1010.435 |
| Text | autolower | special | OK | 5 | 892.601 | 1036.875 | 919.379 | 1447.042 | 1447.042 |
| Text | autolower | mixed | OK | 5 | 854.389 | 926.777 | 936.327 | 989.943 | 989.943 |
| Text | autolower | unicode | OK | 5 | 874.614 | 922.552 | 897.772 | 1022.213 | 1022.213 |
| Text | autonote | add-note | OK | 5 | 847.350 | 906.033 | 907.765 | 952.883 | 952.883 |
| Text | autonote | list-notes | OK | 5 | 887.476 | 959.008 | 947.017 | 1018.392 | 1018.392 |
| Security | autopassword | basic | OK | 5 | 895.173 | 925.762 | 924.823 | 955.036 | 955.036 |
| Security | autopassword | length | OK | 5 | 838.519 | 911.983 | 909.548 | 1011.928 | 1011.928 |
| Security | autopassword | no-special | OK | 5 | 886.690 | 930.319 | 927.652 | 978.882 | 978.882 |
| Security | autopassword | no-numbers | OK | 5 | 879.777 | 986.498 | 975.909 | 1129.862 | 1129.862 |
| Security | autopassword | no-uppercase | OK | 5 | 847.852 | 936.132 | 924.951 | 1002.771 | 1002.771 |
| Security | autopassword | min-special | OK | 5 | 898.140 | 1021.473 | 988.123 | 1280.285 | 1280.285 |
| Security | autopassword | min-numbers | OK | 5 | 863.663 | 959.107 | 946.291 | 1085.632 | 1085.632 |
| Security | autopassword | analysis | OK | 5 | 1120.011 | 1165.496 | 1160.927 | 1219.828 | 1219.828 |
| Security | autopassword | encryption | OK | 5 | 920.213 | 936.093 | 934.873 | 952.889 | 952.889 |
| Task | autotodo | autotodo-list | OK | 5 | 865.940 | 898.673 | 877.928 | 958.416 | 958.416 |
| Conversion | autounit | length-meters-feet | OK | 5 | 900.166 | 956.624 | 967.032 | 1021.887 | 1021.887 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 878.544 | 956.461 | 944.622 | 1024.001 | 1024.001 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 890.533 | 949.831 | 938.117 | 1051.588 | 1051.588 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 923.260 | 999.360 | 955.080 | 1098.088 | 1098.088 |
| Files | autozip | zip-readme | OK | 5 | 903.202 | 1010.301 | 1003.252 | 1172.146 | 1172.146 |
