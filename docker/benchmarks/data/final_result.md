# Open-AutoTools Benchmark Diff

- Generated: 2026-06-02T00:19:38.591395+00:00
- Reports: 15 across 5 runs
- Runners: 3
- Case samples: 510
- Failed cases: 0


## Global Runner Diff

| Runner | Runs | Cases | Failed | Avg mean ms | Total mean ms | Avg P95 ms | Max ms | Diff ms | Diff % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Ubuntu Python 3.12 | 5 | 170 | 0 | 525.829 | 89390.860 | 603.544 | 2201.824 | +0.000 | +0.0% |
| macOS Python 3.12 | 5 | 170 | 0 | 764.662 | 129992.456 | 857.347 | 2541.458 | +238.833 | +45.4% |
| Windows Python 3.12 | 5 | 170 | 0 | 765.070 | 130061.935 | 853.422 | 2467.120 | +239.242 | +45.5% |

## Diff By Run

| Run | Fastest | Runner | Avg mean ms | Diff ms | Diff % | Failed |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| run_20260527t2226z | Ubuntu Python 3.12 | Ubuntu Python 3.12 | 976.831 | +0.000 | +0.0% | 0 |
| run_20260527t2226z | Ubuntu Python 3.12 | Windows Python 3.12 | 1327.387 | +350.557 | +35.9% | 0 |
| run_20260527t2226z | Ubuntu Python 3.12 | macOS Python 3.12 | 1329.460 | +352.629 | +36.1% | 0 |
| run_20260527t2233z | Ubuntu Python 3.12 | Ubuntu Python 3.12 | 975.130 | +0.000 | +0.0% | 0 |
| run_20260527t2233z | Ubuntu Python 3.12 | macOS Python 3.12 | 1339.306 | +364.176 | +37.3% | 0 |
| run_20260527t2233z | Ubuntu Python 3.12 | Windows Python 3.12 | 1347.796 | +372.665 | +38.2% | 0 |
| run_20260528t0015z | Ubuntu Python 3.12 | Ubuntu Python 3.12 | 195.795 | +0.000 | +0.0% | 0 |
| run_20260528t0015z | Ubuntu Python 3.12 | Windows Python 3.12 | 353.724 | +157.929 | +80.7% | 0 |
| run_20260528t0015z | Ubuntu Python 3.12 | macOS Python 3.12 | 355.975 | +160.180 | +81.8% | 0 |
| run_20260528t0018z | Ubuntu Python 3.12 | Ubuntu Python 3.12 | 279.218 | +0.000 | +0.0% | 0 |
| run_20260528t0018z | Ubuntu Python 3.12 | Windows Python 3.12 | 445.209 | +165.992 | +59.4% | 0 |
| run_20260528t0018z | Ubuntu Python 3.12 | macOS Python 3.12 | 447.946 | +168.728 | +60.4% | 0 |
| run_20260602t0018z | Ubuntu Python 3.12 | Ubuntu Python 3.12 | 202.169 | +0.000 | +0.0% | 0 |
| run_20260602t0018z | Ubuntu Python 3.12 | macOS Python 3.12 | 350.621 | +148.451 | +73.4% | 0 |
| run_20260602t0018z | Ubuntu Python 3.12 | Windows Python 3.12 | 351.235 | +149.066 | +73.7% | 0 |

## Biggest Case Gaps

| Run | Case | Fastest | Slowest | Gap ms | Gap % |
| --- | --- | --- | --- | ---: | ---: |
| run_20260602t0018z | autocaps / mixed | Ubuntu Python 3.12 (121.605) | Windows Python 3.12 (426.446) | 304.841 | +250.7% |
| run_20260528t0018z | autonote / add-note | Ubuntu Python 3.12 (113.064) | Windows Python 3.12 (378.538) | 265.474 | +234.8% |
| run_20260528t0018z | autolower / mixed | Ubuntu Python 3.12 (118.777) | Windows Python 3.12 (391.346) | 272.569 | +229.5% |
| run_20260528t0015z | autopassword / min-special | Ubuntu Python 3.12 (143.491) | Windows Python 3.12 (462.123) | 318.632 | +222.1% |
| run_20260528t0018z | autolower / basic | Ubuntu Python 3.12 (124.624) | Windows Python 3.12 (382.819) | 258.195 | +207.2% |
| run_20260528t0018z | autonote / list-notes | Ubuntu Python 3.12 (119.067) | Windows Python 3.12 (355.726) | 236.659 | +198.8% |
| run_20260602t0018z | autocaps / unicode | Ubuntu Python 3.12 (124.449) | macOS Python 3.12 (357.950) | 233.501 | +187.6% |
| run_20260528t0015z | autopassword / no-uppercase | Ubuntu Python 3.12 (131.676) | macOS Python 3.12 (357.645) | 225.969 | +171.6% |
| run_20260528t0018z | autolower / unicode | Ubuntu Python 3.12 (135.929) | macOS Python 3.12 (368.755) | 232.826 | +171.3% |
| run_20260528t0018z | autolower / special | Ubuntu Python 3.12 (160.559) | Windows Python 3.12 (431.953) | 271.394 | +169.0% |
