"""Reproduce all descriptive and reliability tables from text-free ratings.
Run: python reproduce_analysis.py; python 04_query_cluster_bootstrap.py
"""
from pathlib import Path
import importlib.metadata as md
import json
import numpy as np
import pandas as pd
import pingouin as pg
import krippendorff
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parent
METRICS=['factuality','diversity','clarity','insightfulness']
h=pd.read_csv(ROOT/'human_ratings_anonymized.csv')
m=pd.read_csv(ROOT/'arxiv_human_gpt_anonymized.csv')
keys=['query_id','retriever','condition']
assert len(h)==2000 and not h.duplicated(keys+['rater_id']).any()
assert len(m)==400 and not m.duplicated(keys).any()
assert h.groupby(keys).size().eq(5).all()
assert m.groupby('query_id').size().eq(8).all()
reliability=[]; descriptive=[]; ranks=[]
for metric in METRICS:
 col=metric+'_human'; pivot=h.pivot(index=keys,columns='rater_id',values=col)
 assert h[col].dropna().between(1,5).all()
 joined=m.set_index(keys).join(pivot.mean(axis=1).rename('recomputed'))
 assert np.allclose(joined.recomputed,joined[metric+'_human_mean'])
 complete=pivot.dropna(); n,k=complete.shape
 long=complete.reset_index(drop=True).rename_axis('item').reset_index().melt('item',var_name='rater',value_name='score')
 iccs=pg.intraclass_corr(data=long,targets='item',raters='rater',ratings='score').set_index('Type')
 def icc(new,old):
  return float(iccs.loc[new if new in iccs.index else old,'ICC'])
 reliability.append(dict(metric=metric,missing_scores=int(h[col].isna().sum()),complete_items=n,icc_a1=icc('ICC(A,1)','ICC2'),icc_ak=icc('ICC(A,k)','ICC2k'),krippendorff_alpha=float(krippendorff.alpha(reliability_data=complete.to_numpy().T,level_of_measurement='interval'))))
 hm=h.groupby(['retriever','condition'])[col].mean(); gm=m.groupby(['retriever','condition'])[metric+'_gpt'].mean()
 ranks.append(dict(metric=metric,spearman_rho=float(spearmanr(hm,gm).statistic)))
 for (ret,cond),val in hm.items():
  descriptive.append(dict(source='human',retriever=ret,condition=cond,metric=metric,mean=val,n=int(h[(h.retriever==ret)&(h.condition==cond)][col].count())))
 for (ret,cond),val in gm.items():
  descriptive.append(dict(source='gpt',retriever=ret,condition=cond,metric=metric,mean=val,n=50))
pd.DataFrame(reliability).to_csv(ROOT/'inter_rater_agreement.csv',index=False)
pd.DataFrame(descriptive).to_csv(ROOT/'condition_means.csv',index=False)
pd.DataFrame(ranks).to_csv(ROOT/'condition_rank_agreement.csv',index=False)
(ROOT/'environment.json').write_text(json.dumps({p:md.version(p) for p in ['numpy','pandas','scipy','pingouin','krippendorff','matplotlib']},indent=2)+'\n')
print(pd.DataFrame(reliability).to_string(index=False)); print(pd.DataFrame(ranks).to_string(index=False));print('PASS: dimensions, unique keys, scale bounds, and recomputed panel means')
