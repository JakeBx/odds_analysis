# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.2
#   kernelspec:
#     display_name: scrape36
#     language: python
#     name: scrape36
# ---

import re
import pandas as pd

silk = re.compile('\([\d]+\)')


def neds(driver):
    html_neds = driver.page_source
    df_list = pd.read_html(html_neds)
    if df_list[0].shape[1] == 11:
        neds_df = df_list[0].iloc[:,:4].dropna().reset_index(drop=True)
        neds_df.columns = ['runner', 'mi', 'flucs', 'odds']
    elif df_list[0].shape[1] == 14:
        neds_df = df_list[0].iloc[:,:4].dropna().reset_index(drop=True)
        neds_df.columns = ['runner', 'best_time', 'flucs', 'odds']
    else:
        neds_df = df_list[0].iloc[:,:3].dropna().reset_index(drop=True)
        neds_df.columns = ['runner', 'flucs', 'odds']    

    neds_df['back'] = neds_df.odds.apply(lambda x: x.split(' ')[0])
    neds_df['place'] = neds_df.odds.apply(lambda x: x.split(' ')[1])
    neds_df.drop('odds', axis=1, inplace=True)

    neds_df['num'] = neds_df.runner.apply(lambda x: silk.findall(x)[0])
    
    return neds_df


def betfair(driver):
    html_betfair = driver.page_source
    df_list = pd.read_html(html_betfair)

    df_bf = df_list[2].drop([1,2,5,6], axis=1)
    df_bf.columns = ['runner_bf', 'back_bf', 'lay']
    df_bf.dropna(inplace=True)
    df_bf['back_vol'] = df_bf.back_bf.apply(lambda x: x.split(' ')[1])
    df_bf['lay_vol'] = df_bf.lay.apply(lambda x: x.split(' ')[1])
    df_bf['back_bf'] = df_bf.back_bf.apply(lambda x: x.split(' ')[0])
    df_bf['lay'] = df_bf.lay.apply(lambda x: x.split(' ')[0])
    # df_bf['num'] = df_bf.runner_bf.apply(lambda x: silk.findall(x)[0])
    
    return df_bf


def palmer(driver):
    html_neds = driver.page_source
    df_list = pd.read_html(html_neds)
    if df_list[2].shape[1] == 10:
        pb_df = df_list[2].iloc[:-1,[0,2,3,5]]

    pb_df.columns = ['number', 'runner', 'back', 'place']
    pb_df.dropna(inplace=True)
    pb_df['num'] = pb_df.runner.apply(lambda x: silk.findall(x)[0])

    return pb_df


