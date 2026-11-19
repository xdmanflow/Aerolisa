# Pipeline Builder: `silver/cmapss_cycles_pb` (low-code twin of `silver_cycles`)

Input: `bronze/cmapss_raw`.

| # | Board / transform | Settings |
|---|---|---|
| 1 | Extract (regex) | `subset` = regex `FD00\d` on `source_file` |
| 2 | Case | `split` = "train" if `source_file` starts with "train" else "test" |
| 3 | Case | `role` = "HIST" if split = train else "FLEET" |
| 4 | Pad / concat | `engine_id` = concat_ws("-", subset, role, lpad(unit, 3, "0")) |
| 5 | Concat | `cycle_id` = concat_ws("-", engine_id, lpad(cycle, 3, "0")) |
| 6 | Cast | unit, cycle → integer; op1–op3, sensor_1–21 → double |
| 7 | Select columns | same order as the code version |
| 8 | Output + expectations | primary key `cycle_id`; `split` in (train, test) |

**Compare:** row count 33,727 and 10 random `cycle_id`s identical to `silver/cmapss_cycles`.
**Write down:** what was faster in Pipeline Builder, and what you'd only do in code (tests, reuse in the ML repo).
