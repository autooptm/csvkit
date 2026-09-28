<div align="center">
  <a href="https://autooptm.com"><img src=".autooptm/logo.png" width="96" alt="AutoOptm"></a>

  <h1>csvkit · optimized by <a href="https://autooptm.com">AutoOptm</a></h1>

  <p><b>23.41x faster end to end</b> on the command below, output verified against the stock program.</p>

  <p>
    <a href="https://autooptm.com"><img alt="speedup" src="https://img.shields.io/badge/end--to--end-23.41x-2ea44f"></a>
    <a href="https://github.com/wireservice/csvkit/commit/ba8033dcbb2c72089e88f38a1a50ddfc8e5ac3df"><img alt="base" src="https://img.shields.io/badge/upstream-ba8033dcbb2c-blue"></a>
    <img alt="card" src="https://img.shields.io/badge/measured%20on-RTX%204090%20host%2C%20CPU-bound%20program-lightgrey">
  </p>
</div>

> This is a fork of [wireservice/csvkit](https://github.com/wireservice/csvkit) at commit
> [`ba8033dcbb2c`](https://github.com/wireservice/csvkit/commit/ba8033dcbb2c72089e88f38a1a50ddfc8e5ac3df) with the AutoOptm patch applied on top.
> The optimisation was found, measured and verified automatically by [AutoOptm](https://autooptm.com);
> the patch is also kept verbatim at [`.autooptm/autooptm.patch`](.autooptm/autooptm.patch).

## The result

| | |
|---|---|
| **Command** | `python csvkit/utilities/csvstat.py big.csv` |
| **Entry point** | `csvkit/utilities/csvstat.py` |
| **Unit measured** | one `csvstat` run over a 550k-row CSV (end to end) |
| **Before (stock)** | 161.3 s per unit |
| **After (this tree, all switches default ON)** | 6.89 s per unit |
| **Speedup** | **23.41x** end to end, noise floor of the host 0.3% (median of 5 repeats) |
| **Output** | bit-identical: every reported statistic equals stock csvkit on the pinned set and on the holdout (max_abs_diff = 0.0) |

### What changed

| File | Where | Gain (alone) |
|---|---|---|
| `csvkit/fastcast.py` | new module | 1.92x |
| `csvkit/fastcast.py` | new module | 1.008x |
| `csvkit/cli.py` | CSVKitUtility.get_column_types | 1.92x |
| `csvkit/utilities/csvstat.py` | CSVStat.read_table | 2.63x |
| `csvkit/utilities/csvstat.py` | CSVStat.calculate_stats | 1.04x |



## Reproduce

```bash
git clone https://github.com/autooptm/csvkit-ao.git
cd csvkit-ao
# set up exactly as upstream documents, then:
python csvkit/utilities/csvstat.py big.csv
```

The diff against upstream is one commit: `git log -1 -p` shows it, and
`git diff ba8033dcbb2c` is the same patch as `.autooptm/autooptm.patch`.

---

<div align="center"><sub>Optimized by <a href="https://autooptm.com">AutoOptm</a> — point it at a repository, get back a verified speedup and the patch.</sub></div>

---

The upstream README is [`README.rst`](README.rst), unchanged.

