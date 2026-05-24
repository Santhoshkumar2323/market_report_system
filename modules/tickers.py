# modules/tickers.py

ASSET_STRUCTURE = {

    "Global Indices": {
        "United States": [
            {"name": "S&P 500", "symbol": "^GSPC"},
            {"name": "NASDAQ", "symbol": "^IXIC"},
            {"name": "Dow Jones", "symbol": "^DJI"},
        ],
        "Europe": [
            {"name": "DAX", "symbol": "^GDAXI"},
            {"name": "CAC 40", "symbol": "^FCHI"},
            {"name": "Euro Stoxx 50", "symbol": "^STOXX50E"},
            {"name": "FTSE 100", "symbol": "^FTSE"},
        ],
        "Japan": [
            {"name": "Nikkei 225", "symbol": "^N225"},
        ],
        "China": [
            {"name": "SSE Composite", "symbol": "000001.SS"},
            {"name": "SZSE Component", "symbol": "399001.SZ"},
        ],
        "India": [
            {"name": "Nifty 50", "symbol": "^NSEI"},
            {"name": "Sensex", "symbol": "^BSESN"},
        ],
    },

    "US Sectors": [
        {"name": "Technology", "symbol": "XLK"},
        {"name": "Financials", "symbol": "XLF"},
        {"name": "Healthcare", "symbol": "XLV"},
        {"name": "Energy", "symbol": "XLE"},
        {"name": "Industrials", "symbol": "XLI"},
    ],

"India Sectors": [
    {"name": "Nifty Bank", "symbol": "^NSEBANK"},
    {"name": "Nifty IT", "symbol": "^CNXIT"},
    {"name": "Nifty Energy", "symbol": "^CNXENERGY"},
    {"name": "Nifty FMCG", "symbol": "^CNXFMCG"},
    {"name": "Nifty Auto", "symbol": "^CNXAUTO"},
    {"name": "Nifty Pharma", "symbol": "^CNXPHARMA"},
    {"name": "Nifty Metal", "symbol": "^CNXMETAL"}
],


    "Commodities": [
        {"name": "Gold Futures", "symbol": "GC=F"},
        {"name": "Silver Futures", "symbol": "SI=F"},
        {"name": "WTI Crude", "symbol": "CL=F"},
        {"name": "Brent Crude", "symbol": "BZ=F"},
        {"name": "Copper", "symbol": "HG=F"},
    ],

    "Crypto": [
        {"name": "Bitcoin", "symbol": "BTC-USD"},
        {"name": "Ethereum", "symbol": "ETH-USD"},
        {"name": "Solana", "symbol": "SOL-USD"},
    ],

    "Macro Market Signals": [
        {"name": "US Dollar Index", "symbol": "DX-Y.NYB"},
        {"name": "VIX Volatility", "symbol": "^VIX"},
        {"name": "USDJPY", "symbol": "JPY=X"},
    ],
}