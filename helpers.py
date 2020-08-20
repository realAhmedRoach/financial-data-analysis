#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Holds information about a specific asset recommendation
class Recommendation:
    BUY = 'BUY'
    SELL = 'SELL'
    SPREAD = 'SPREAD'
    
    def __init__(self, r_type, asset, analysis=''):
        self.r_type = r_type
        self.asset = asset
        self.analysis = analysis


# In[ ]:


import pandas as pd

# shortcuts for Quandl data codes
class Data:
    CPI = 'FRED/CPIAUCSL'
    ANFCI = 'FRED/ANFCI'
    LEVERAGE = 'FRED/NFCINONFINLEVERAGE'
    FF = 'FRED/FF'
    LI = 'FRED/USSLIND'
    RGPDI = 'FRED/GPDIC1'
    BUSINV = 'FRED/BUSINV'
    YLDCRV = 'FRED/T10Y2Y'
    MONSPLY = 'FRED/M1'
    RETAIL = 'FRED/RSXFS'
    LOANS = 'FRED/BUSLOANS'
    PCE = 'FRED/PCE'
    RGDP = 'FRED/GDPC1'
    NGDP = 'FRED/GDP'
    PGDP = 'FRED/NGDPPOT'
    ED = 'CME/ED'
    ED1 = 'CHRIS/CME_ED1'
    EY = 'MULTPL/SP500_EARNINGS_YIELD_MONTH'
    TBILL = 'FRED/DGS3MO'
    TED = 'FRED/TEDRATE'
    DXY = 'CHRIS/ICE_DX1'
    VIX = 'CHRIS/CBOE_VX1'
    SENT = 'AAII/AAII_SENTIMENT'
    
    OILINV = 'FRED/A33DTI'
    OILCAP = 'EIA/PET_MOPUEUS2_M'

# CFTC COT Report shortcuts
class COT:
    GE = ['132741', 'GE', 'Eurodollar']
    ZN = ['043602', 'ZN', 'Ten-year T-Note']
    ZF = ['044601', 'ZF', 'Five-year T-Note']
    ZT = ['042601', 'ZT', 'Two-year T-Note']
    ZB = ['020601', 'ZB', 'T-Bond']
    UB = ['020604', 'UB', 'Ultra T-Bond']
    _6S = ['092741', '6S', 'Swiss Franc']
    _6M = ['095741', '6M', 'Mexican Peso']
    _6E = ['099741', '6E', 'Euro FX']
    _6B = ['096742', '6B', 'British Pound']
    _6N = ['112741', '6N', 'New Zealand Dollar']
    _6C = ['090741', '6C', 'Canadian Dollar']
    _6A = ['232741', '6A', 'Australian Dollar']
    _6J = ['097741', '6J', 'Japanese Yen']
    NIY = ['240743', 'NIY', 'Nikkei Yen']
    ES = ['13874C', 'ES', 'E-mini S&P']
    YM = ['124603', 'YM', 'E-mini Dow']
    NQ = ['209742', 'NQ', 'E-mini NASDAQ']
    DX = ['098662', 'DX', 'Dollar Index']
    VX = ['1170E1', 'VX', 'VIX']
    
    CL = ['067651', 'CL', 'Crude Oil']
    OJ = ['040701', 'OJ', 'Orange Juice']
    ZC = ['002602', 'ZC', 'Corn']
    ZS = ['005602', 'ZS', 'Soybeans']
    GC = ['088691', 'GC', 'Gold']
    RR = ['039601', 'RR', 'Rough Rice']
    ZW = ['001602', 'ZW', 'Wheat']
    HO = ['022651', 'HO', 'Heating Oil']
    RB = ['111659', 'RB', 'RBOB Gasoline']
    CT = ['033661', 'CT', 'Cotton']
    LBS = ['058643', 'LBS', 'Random-Length Lumber']
    ZM = ['SN', 'ZM', 'Soybean Meal']
    HG = ['085692', 'HG', 'Copper']
    NG = ['023651', 'NG', 'Natural Gas']
    LE = ['057642', 'LE', 'Live Cattle']
    CC = ['073732', 'CC', 'Cocoa']
    ZO = ['004603', 'ZO', 'Oats']
    GF = ['061641', 'GF', 'Feeder Cattle']
    SB = ['080732', 'SB', 'Sugar']
    ZL = ['007601', 'ZL', 'Soybean Oil']
    SI = ['084691', 'SI', 'Silver']
    PA = ['075651', 'PA', 'Palladium']
    HE = ['054642', 'HE', 'Lean Hog']
    PL = ['076651', 'PL', 'Platinum']
    KC = ['083731', 'KC', 'Coffee']
    
    FIN = [GE, ZN, ZF, ZT, ZB, UB, _6S, _6M, _6E, _6B, _6N, _6C, _6A, _6J, NIY, ES, YM, NQ, DX, VX]
    COM = [CL, OJ, ZC, ZS, GC, RR, ZW, HO, RB, CT, LBS, ZM, HG, NG, LE, CC, ZO, GF, SB, ZL, SI, PA, HE, PL, KC]
    
    
    @staticmethod
    def data(asset):
        return 'CFTC/' + (asset, asset[0])[isinstance(asset, list)] + '_FO_ALL'
    
    fin_cols = {'columns': ['Open Interest', 'Asset Manager Longs', 'Asset Manager Shorts', 'Leveraged Funds Longs', 'Leveraged Funds Shorts', 'Other Reportable Longs', 'Other Reportable Shorts', 'Non Reportable Longs', 'Non Reportable Shorts']}
    
    def format_fin(data_old, last_only=False):
        data = data_old
        del data['Dealer Spreads']
        del data['Leveraged Funds Spreads']
        del data['Asset Manager Spreads']
        del data['Other Reportable Spreads']
        del data['Total Reportable Longs']
        del data['Total Reportable Shorts']
        data['Net'] = 0
        data['Net'] += data['Asset Manager Longs'] - data['Asset Manager Shorts']
        data['Net'] += data['Leveraged Funds Longs'] - data['Leveraged Funds Shorts']
        data['Net'] += data['Other Reportable Longs'] - data['Other Reportable Shorts']
        data['Net'] += data['Non Reportable Longs'] - data['Non Reportable Shorts']
        data['Percent'] = data['Net'] / data['Open Interest']
        lowest = data['Percent'].min()
        difference = data['Percent'].max() - lowest
        data['Percent'] = (data['Percent'] - lowest) / difference
        return data if not last_only else last(data, 'Percent')
    
    def format_com(data_old, last_only=False):
        data = data_old
        del data['Swap Dealer Longs']
        del data['Swap Dealer Shorts']
        del data['Swap Dealer Spreads']
        del data['Money Manager Spreads']
        del data['Other Reportable Spreads']
        del data['Total Reportable Longs']
        del data['Total Reportable Shorts']
        data['Net'] = 0
        data['Net'] += data['Money Manager Longs'] - data['Money Manager Shorts']
        data['Net'] += data['Other Reportable Longs'] - data['Other Reportable Shorts']
        data['Net'] += data['Non Reportable Longs'] - data['Non Reportable Shorts']
        data['Percent'] = data['Net'] / data['Open Interest']
        lowest = data['Percent'].min()
        difference = data['Percent'].max() - lowest
        data['Percent'] = (data['Percent'] - lowest) / difference
        return data if not last_only else last(data, 'Percent')
    


# In[ ]:


# date helper methods
from datetime import timedelta, date
year = timedelta(days=365)
data_date = date.today()

def date_fmt(date):
    return str(date.year) + '-' + str(date.month) + '-' + str(date.day)

def years_ago(num):
    return data_date - (year * num)


# In[ ]:


# statistics methods
def mean(df):
    return df.values.mean()

def last(df, col='Value'):
    return df[col].iloc[-1] if len(df[col]) > 0 else 0

def std(df):
    return df.values.std(ddof=1)

