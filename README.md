# Biomedical expert and LLM-judge scoring in Alzheimer's literature RAG

**LLM Judge and Biomedical Expert Agreement in Alzheimer's Disease Literature RAG: An Exploratory Query-Reformulation Study**

[Read the manuscript](manuscript.pdf) · [Download arXiv source](arxiv_submission.zip)

This is a retrospective exploratory comparison of two scoring protocols on 50 queries and eight RAG configurations. Five biomedical researchers assessed query, response, and retrieved abstracts side by side; GPT-4o assessed individual query-response pairs without abstracts. Evaluator type is therefore confounded with evidence access and presentation. Correlations measure association, not factual correctness or interchangeability.

## Reproduce

Use Python 3.12 in a fresh virtual environment:

```sh
pip install -r requirements.txt
python reproduce_analysis.py
python 04_query_cluster_bootstrap.py
```

The first script validates the 2,000 rater records, 400 matched pairs, unique identifiers, and recomputed panel means before writing condition means, ICC, interval Krippendorff alpha, and condition-rank correlations. The second uses 2,000 query-cluster bootstrap replicates with seed 20260807. All eight conditions remain together when a query is sampled.

## Files

- `human_ratings_anonymized.csv`: 2,000 records, five raters, four metrics; 61 missing scalar scores.
- `arxiv_human_gpt_anonymized.csv`: 400 matched pairs with panel summaries and GPT scores.
- `condition_means.csv`, `inter_rater_agreement.csv`, `condition_rank_agreement.csv`, `query_cluster_bootstrap.csv`: reproduced results.
- `environment.json`, `requirements.txt`: tested analysis versions.
- `arxiv_submission.zip`: LaTeX source, bibliography, prompt figures, and ancillary data/scripts. Extract and compile `sn-article.tex` with XeLaTeX/BibTeX or Tectonic.

Query IDs and rater IDs are consistent across tables. Query texts, generated responses, retrieved abstracts, and evaluator names are excluded. One missing query-text cell was linked by its existing query ID after all eight response/context pairs were verified against the other files. Its observed scores are retained; scores were not imputed.

## Interpretation and provenance

Pooled Pearson correlations range from 0.28 to 0.54; Spearman correlations range from 0.27 to 0.52. Single-rater ICC ranges from 0.09 to 0.24. Method rankings are descriptive: document budgets vary, keywords also enter the generation prompt, and the archived BM25 no-keyword baseline has a second-step selection artifact. No retrieval relevance gold standard is available.

Legacy pipeline: [yeomsee/best_practices_bio_rag](https://github.com/yeomsee/best_practices_bio_rag), commit `25be531c6e8b5aff76b1a99a9011665e062299e2`. Corpus/index: [Hugging Face](https://huggingface.co/datasets/stv10121/pubmed_alzheimer_kb). These are provenance resources; exact original model snapshots and corpus preprocessing are incompletely documented. This release reproduces the statistical analysis, not the original model calls.

## Citation and reuse

See `CITATION.cff`. No arXiv identifier has been assigned to this release. No additional software or data license is granted by this repository; obtain permission for reuse beyond applicable legal rights.
