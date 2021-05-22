#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from IPython.display import display, HTML
import math
from scipy.stats import ttest_ind_from_stats, mannwhitneyu
import numpy as np

# https://arxiv.org/pdf/1910.03878.pdf
# https://netflixtechblog.com/reimagining-experimentation-analysis-at-netflix-71356393af21
# https://gfycat.com/ethicalphysicalcarp


delay = {'metric': [.1, .2, .3,.4,.3,.2,.1], 'test cell': [11,22,11,22,11,11,22], 'dimension':['play_delay','play_delay','play_delay','play_delay','play_delay','play_delay','play_delay']}
sales = {'metric': [0, 1, 0,1,1,1,1], 'test cell': [11,22,11,22,11,11,22], 'dimension':['sales','sales','sales','sales','sales','sales','sales']}

data = pd.DataFrame(data=delay)
data=data.append(pd.DataFrame(data=sales))
data.groupby('dimension').count()

 
# Create the models
## Classes


class Metric():
    def __init__(self,key,label,description,win_direction,statistics):
        self.key=key
        self.label=label
        self.description=description
        self.win_direction=win_direction
        self.statistics=statistics
        
#         y=metric that needs to be measured (key)
#         W=other features useful for measuing the variable
#         x=a binary variable indicating whether a user recieved treatment
#         t=a variable for indexing time
#         theta=hyperparameters for the model
    


### Analysis Class




class Analysis():
    def __init__(self, data, control_experience,metrics,metadata):
        self.data=data
        self.control_experience=control_experience
        self.metrics=metrics
        self.metadata=metadata
    def stat_prep(self, *args):
        metrics=self.metrics
        key=metrics[0].key
        for i in metrics:
            for j in i.statistics:
                 print(j(data,key,control_group=self.control_experience['test cell']))
    def visualize(self,*args):
        css='https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'
        metrics=self.metrics
        key=metrics[0].key
        div_body=f'<html> <head><link rel="stylesheet" href="{css}"></head><body><div class="container">'
        for i in metrics:
            for j in i.statistics:
                div_body+=f"<div class='row'><div class='col-sm-2'>{j.name(self)}</div>"
                div_body+=f"<div class='col-sm-10'>{j(data=data,key=key,control_group=self.control_experience).get_stats().to_html(classes='table table-striped')}</div></div>"
        div_body+='</div></body></html>'

        return display(HTML(div_body))
#     this will loop through the statistics list and create a row for each statistic function
#     once we have functions that work, we will place them in the div labeled "table"

###### Causal Models ######


### Quant

class QuantileBoostrappingC():
    def __init__(self,key,data=[],**kwargs):
        self.data=data
        for key, value in kwargs.items():
            setattr(self, key, value)
    def name(self):
        return 'Quantile Bootstrapping'
    def get_stats(self):
        return data

### Mann Whitney

class MannWhitneyC():
    def __init__(self,data=[],**kwargs):
      self.data=data
      for key, value in kwargs.items():
            setattr(self, key, value)
    def name(self):
        return 'Mann-Whitney Wilco.'
    def test(self):
        control_filter=11
        variant_filter=22
        control_df=data[(data['test cell']==control_filter) & (data['dimension']=='play_delay')]
        variant_df=data[(data['test cell']==variant_filter) & (data['dimension']=='play_delay')]
        
        metric1=control_df[control_df['dimension']=='play_delay'].metric
        metric2=variant_df[variant_df['dimension']=='play_delay'].metric
        
        return mannwhitneyu(metric1, metric2)

    def get_stats(self):
        return pd.DataFrame({'Control':['-'],'Variant':[self.test().pvalue]})


### T Test

class TTestStatsclass():
    def __init__(self,key,data=[],**kwargs):
        self.data=data
        self.key=key
        for key, value in kwargs.items():
            setattr(self, key, value)
    def name(self):
        return 'T-Test'
    def test(self):
        key=self.key
        df=self.data
        control_filter=11
        variant_filter = 22
        
        control_df=df[(df['test cell']==control_filter) & (df['dimension']==key)]
        variant_df=df[(df['test cell']==variant_filter) & (df['dimension']==key)]
        
        metric1=control_df[control_df['dimension']==key].metric
        metric2=variant_df[variant_df['dimension']==key].metric
        
        n1=len(metric1)
        n2=len(metric2)
        mean1=metric1.mean()
        mean2=metric2.mean()
        

        std1 = np.std(metric1)
        std2 = np.std(metric2)
        return ttest_ind_from_stats(mean1, std1, mean2, std2,n1, n2)
    def get_stats(self):
        return pd.DataFrame({'Control':['-'],'Variant':[self.test().pvalue]})
    def whats_init(self):
        return self.key



class DescriptiveStatistics():
    def __init__(self, x='',Y='',W='',data=[],**kwargs):
        self.Y=Y
        self.x=x
        self.W=W
        self.data=data
    def name(self):
        return 'Descriptive Statistics'
    def get_stats(self):
        df= data.groupby('test cell').agg({
            'metric':['count','mean','median']
        })
        df.columns=['count','mean','median']
        dfs= df.T
        return dfs
    def loop(self):    
        dfs=self.get_stats().to_dict()
        for i in dfs:
            print(f'{i} \n # of accounts {dfs[i]["count"] :,.0f} \n  delta mean {dfs[i]["mean"] :,.2f} \n delta median {dfs[i]["median"] :,.2f} \n \
')
    
