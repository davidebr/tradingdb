# webpage https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX&page=1
import requests
from requests.adapters import HTTPAdapter, Retry

from bs4 import BeautifulSoup

import pandas as pd

import yfinance as yf

from datetime import datetime, timedelta
import logging
import json
import numpy as np
import os
import urllib

from tradingdb.ORM import stock


log = logging.getLogger(__name__)
handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
log.addHandler(handler)


def make_request(url, mode="GET", payload=None, backoff=5.0):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=backoff)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    if mode == "GET":
        response = session.get(url)
    elif mode == "POST":
        response = requests.post(url, json=payload)
    return response


def download_ftse_symbols(index_symbol):

    index_dictionary = {
        "FTSE-100": "ftse-100",
        "FTSE-250": "ftse-250",
        "FTSE-350": "ftse-350",
        "FTSE-AllShare": "ftse-all-share",
        "AIM50": "ftse-aim-uk-50-index",
        "AIM100": "ftse-aim-100-index",
        "AIM-AllShare": "ftse-aim-all-share",
    }

    index = index_dictionary[index_symbol]

    URL = f"https://api.londonstockexchange.com/api/v1/pages?path=ftse-constituents&parameters=indexname%3D{index}%26tab%3Dtable"
    # print(urllib.parse.unquote(URL))
    log.debug("Calling the page frame...")

    x = make_request(URL)
    soup = BeautifulSoup(x.content, "html.parser")
    myjson = json.loads(soup.text)

    tabId_for_post = myjson["components"][1]["content"][0]["value"]["toggles"][0][
        "tabId"
    ]
    componentId_for_post = myjson["components"][1]["content"][0]["value"]["toggles"][0][
        "modules"
    ][0]["moduleId"]
    componentId_for_post = urllib.parse.quote(componentId_for_post)

    URL = "https://api.londonstockexchange.com/api/v1/components/refresh"
    df = pd.DataFrame()
    i = 0
    while True:
        payload = {
            "path": "ftse-constituents",
            "parameters": f"indexname%3D{index}%26tab%3Dtable%26tabId%3D{tabId_for_post}",
            "components": [
                {"componentId": componentId_for_post, "parameters": f"page={i}"}
            ],
        }
        x = requests.post(URL, json=payload)
        # print(x.content)
        soup = BeautifulSoup(x.content, "html.parser")
        myjson = json.loads(soup.text)
        results = myjson[0]["content"][0]["value"]["content"]

        if len(results) == 0:
            break

        df = pd.concat([df, pd.DataFrame.from_records(results)])
        # df=pd.DataFrame.from_records(results)
        log.debug("pagenumber " + str(i) + " number of entries so far: " + str(len(df)))
        i += 1

    return df


def download_data_from_yfsymbols(
    symbols, timestart, timeend, interval="1d", mypath=None
):
    # d1=timestart.date()
    # mystart=f"{d1:%Y-%m-%d}"
    # d2=timeend.date()
    # myend=f"{d2:%Y-%m-%d}"
    # print("Start ",d1," End ",d2)
    import copy

    results_df = {}

    # yfinance automatically detect if this is a list or a simple string
    df = yf.download(tickers=symbols, interval=interval, start=timestart, end=timeend)

    if isinstance(symbols, str):
        results_df[symbols] = copy.deepcopy(df)
    elif isinstance(symbols, list):
        if len(symbols) > 1:
            for symbol in df.columns.levels[1]:
                ddf = df.iloc[:, df.columns.get_level_values(1) == symbol]
                ddf.columns = ddf.columns.droplevel(1)
                # save in csv
                if len(ddf) > 0:
                    if mypath is not None:
                        filename = f"{symbol}.csv"
                        filename = os.path.join(mypath, filename)
                        ddf.to_csv(filename, index=True)
                    ddf=ddf.dropna()
                    results_df[symbol] = copy.deepcopy(ddf)
        else:
            df=df.dropna()
            results_df[symbols] = copy.deepcopy(df)

    return results_df
