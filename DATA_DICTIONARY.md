# Rating data dictionary

Both inputs are UTF-8 CSV files. Empty numeric cells represent missing ratings, not zero.

| Field | Meaning |
|---|---|
| `query_id` | Stable pseudonym Q001–Q050; shared across inputs; ordering has no scientific meaning. |
| `rater_id` | Stable pseudonym R01–R05; only present in evaluator-level input. |
| `retriever` | `bm25` or `dpr`. |
| `condition` | `keyword_none_naive`, `keyword_none_hyde`, `keyword_hyde`, or `keyword_mesh_hyde`. |
| `{metric}_human` | One expert's integer rating, 1–5, or missing. |
| `{metric}_human_mean` | Mean of available experts for this query–condition pair. |
| `{metric}_human_std` | Sample standard deviation of available expert ratings (ddof=1). |
| `{metric}_human_count` | Number of observed expert ratings for this pair and metric. |
| `{metric}_gpt` | Archived GPT-4o integer rating, 1–5. |

Metrics: `factuality`, `diversity`, `clarity`, `insightfulness`.

`human_ratings_anonymized.csv`: unique (`rater_id`, `query_id`, `retriever`, `condition`), 2000 rows. Missing scores by metric: 15, 15, 16, 15. Complete five-rater items: 387, 387, 386, 387.

`arxiv_human_gpt_anonymized.csv`: unique (`query_id`, `retriever`, `condition`), 400 rows. GPT scores are complete; all panel means have observations. Query–condition comparisons weight each pair equally; human condition means instead pool available individual scores, so weights can differ with missingness.

## Outputs

- `condition_means.csv`: source, retriever, condition, metric, mean, observed score count.
- `inter_rater_agreement.csv`: missingness, complete items, absolute-agreement single-rater/panel-mean ICC, interval Krippendorff alpha.
- `condition_rank_agreement.csv`: Spearman correlation of eight condition means.
- `query_cluster_bootstrap.csv`: pooled correlations and expert-minus-GPT offsets with percentile 95% intervals; 50 queries resampled as clusters, fixed panel.
- `sensitivity_results.csv`: 4 metrics × (1 pooled + 1 complete-case + 5 rater omissions + 8 within-condition comparisons) = 60 rows. `n` counts query–condition pairs. No confidence intervals or significance tests are implied.

The scripts use only the two rating inputs. No private query/rater mapping is needed or included. Pseudonyms do not make a guarantee of anonymity against every possible external linkage.
