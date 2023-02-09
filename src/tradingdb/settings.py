CURRENCIES=['GBP','USD','EUR']

EXCHANGES={
    'NASDAQ':{'cur':'USD'},
    'NYSE':{'cur':'USD'},
    'FTSE':{'cur':'GBP'},
    'FTSE-AIM':{'cur':'GBP'},
    'INDEXES':{},
}

INDEXES={
    'FTSE100':              { 'yf':'^FTSE','url':'%5EFTSE','cur':'GBP','wiki':'https://en.wikipedia.org/wiki/FTSE_100_Index'},
    'FTSEAIM_all_share':    {'yf': '^FTAI', 'url':'%5EFTAI','cur':'GBP'},
    'NASDAQ':               {'yf':'^IXIC','url':'%5EIXIC','cur':'USD'},
    'DowJones':             {'yf':'^GSPC','url':'%5EGSPC','cur':'USD'},
    'S&P500':               {'yf':'^DJI','url':'%5EDJI','cur':'USD','wiki':'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'},
}


VALID_INTERVALS={   '1m':60,
                        '2m':2*60,
                        '5m':5*60,
                        '15m':15*60,
                        '30m':30*60,
                        '60m':60*60,
                        '90m':90*60,
                        '1h':60*60,
                        '1d':24*60*60,
                        '5d':5*24*60*60,
                        '1wk':7*24*60*60,
                        '1mo':30*24*60*60,
                        '3mo':90*24*60*60,
                        }