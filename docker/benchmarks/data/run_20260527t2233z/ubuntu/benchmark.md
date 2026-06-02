# Open-AutoTools CLI Benchmark

- Run: run_20260527t2233z
- Started: 2026-05-27T22:33:47.387629+00:00
- Finished: 2026-05-27T22:37:07.504872+00:00
- Platform: Ubuntu
- Python: 3.12
- Iterations: 5
- Warmup: 1
- Timeout: 30s

| Category | Tool | Case | Status | Count | Min ms | Mean ms | Median ms | P95 ms | Max ms |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Text | autocaps | basic | OK | 5 | 875.188 | 1007.132 | 978.425 | 1146.166 | 1146.166 |
| Text | autocaps | special | OK | 5 | 918.997 | 950.018 | 957.221 | 974.565 | 974.565 |
| Text | autocaps | mixed | OK | 5 | 882.589 | 919.660 | 929.534 | 957.793 | 957.793 |
| Text | autocaps | unicode | OK | 5 | 836.135 | 928.994 | 914.891 | 1075.499 | 1075.499 |
| Color | autocolor | hex-default | OK | 5 | 856.805 | 887.635 | 871.514 | 957.348 | 957.348 |
| Color | autocolor | hex-rgb | OK | 5 | 879.793 | 921.422 | 887.109 | 979.563 | 979.563 |
| Color | autocolor | rgb-hsl | OK | 5 | 877.253 | 953.017 | 918.931 | 1100.500 | 1100.500 |
| Color | autocolor | hsl-rgba | OK | 5 | 897.610 | 1290.323 | 935.744 | 1920.278 | 1920.278 |
| Files | autoconvert | md-json | OK | 5 | 854.147 | 933.819 | 884.644 | 1101.684 | 1101.684 |
| Network | autoip | basic | OK | 5 | 867.965 | 923.465 | 906.692 | 982.655 | 982.655 |
| Network | autoip | connectivity | OK | 5 | 1076.346 | 1145.879 | 1136.968 | 1263.132 | 1263.132 |
| Network | autoip | dns | OK | 5 | 844.507 | 946.154 | 937.937 | 1031.216 | 1031.216 |
| Network | autoip | ports | OK | 5 | 866.465 | 914.646 | 893.617 | 1026.814 | 1026.814 |
| Text | autolower | basic | OK | 5 | 889.620 | 976.241 | 947.319 | 1150.942 | 1150.942 |
| Text | autolower | special | OK | 5 | 867.590 | 908.713 | 915.978 | 944.968 | 944.968 |
| Text | autolower | mixed | OK | 5 | 883.264 | 939.144 | 922.959 | 999.727 | 999.727 |
| Text | autolower | unicode | OK | 5 | 888.316 | 931.539 | 940.621 | 955.868 | 955.868 |
| Text | autonote | add-note | OK | 5 | 939.939 | 1138.460 | 965.498 | 1849.749 | 1849.749 |
| Text | autonote | list-notes | OK | 5 | 864.220 | 926.161 | 913.699 | 1030.420 | 1030.420 |
| Security | autopassword | basic | OK | 5 | 858.158 | 917.600 | 928.718 | 948.127 | 948.127 |
| Security | autopassword | length | OK | 5 | 896.858 | 958.479 | 965.018 | 1019.622 | 1019.622 |
| Security | autopassword | no-special | OK | 5 | 884.633 | 916.506 | 914.638 | 949.028 | 949.028 |
| Security | autopassword | no-numbers | OK | 5 | 913.373 | 988.906 | 975.354 | 1051.117 | 1051.117 |
| Security | autopassword | no-uppercase | OK | 5 | 865.461 | 931.085 | 908.103 | 1034.040 | 1034.040 |
| Security | autopassword | min-special | OK | 5 | 893.677 | 928.082 | 938.781 | 953.041 | 953.041 |
| Security | autopassword | min-numbers | OK | 5 | 833.866 | 951.348 | 959.125 | 1024.768 | 1024.768 |
| Security | autopassword | analysis | OK | 5 | 1045.530 | 1144.508 | 1134.351 | 1243.100 | 1243.100 |
| Security | autopassword | encryption | OK | 5 | 924.571 | 992.621 | 958.979 | 1084.303 | 1084.303 |
| Task | autotodo | autotodo-list | OK | 5 | 875.856 | 1209.585 | 965.569 | 2201.824 | 2201.824 |
| Conversion | autounit | length-meters-feet | OK | 5 | 810.114 | 901.181 | 897.755 | 989.827 | 989.827 |
| Conversion | autounit | volume-liters-gallons | OK | 5 | 858.506 | 947.425 | 949.207 | 1027.574 | 1027.574 |
| Conversion | autounit | weight-kg-lb | OK | 5 | 887.850 | 942.407 | 899.681 | 1039.730 | 1039.730 |
| Conversion | autounit | temperature-celsius-fahrenheit | OK | 5 | 904.179 | 967.068 | 965.232 | 1061.243 | 1061.243 |
| Files | autozip | zip-readme | OK | 5 | 875.445 | 915.211 | 917.122 | 938.023 | 938.023 |
