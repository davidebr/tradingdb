CURRENCIES=['GBP','USD','EUR']

EXCHANGES={
    'NASDAQ':{'cur':'USD'},
    'NYSE':{'cur':'USD'},
    'FTSE':{'cur':'GBP'},
    'FTSE-AIM':{'cur':'GBP'}
}

INDEXES={
    'FTSE100':              { 'yf':'^FTSE','url':'%5EFTSE'},
    'FTSEAIM_all_share':    {'yf': '^FTAI', 'url':'%5EFTAI'},
    'NASDAQ':               {'yf':'^IXIC','url':'%5EIXIC'},
    'DowJones':             {'yf':'^GSPC','url':'%5EGSPC'},
    'S&P500':               {'yf':'^DJI','url':'%5EDJI'},
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