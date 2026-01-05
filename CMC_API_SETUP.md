# CoinMarketCap API Key Setup Guide

The widget now uses CoinMarketCap's Fear & Greed Index, which requires a **free API key**.

## Step-by-Step: Get Your Free API Key

### 1. Go to CoinMarketCap API Website
Visit: **https://coinmarketcap.com/api/**

### 2. Click "Get Your Free API Key Now"
Look for the prominent button on the page

### 3. Sign Up (Free Account)
- Fill in your email, password, and basic info
- Choose the **Basic** plan (FREE - 10,000 API calls/month)
- Verify your email address

### 4. Get Your API Key
- Once logged in, go to your API dashboard
- Copy your API key (it looks like: `a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8`)

### 5. Add API Key to the Widget

Open `crypto_widget.py` in a text editor and find this line (near the top):

```python
self.CMC_API_KEY = "YOUR_API_KEY_HERE"  # <-- PUT YOUR CMC API KEY HERE
```

Replace `YOUR_API_KEY_HERE` with your actual API key:

```python
self.CMC_API_KEY = "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"  # Your real key
```

### 6. Save and Run
- Save the file
- Run: `python crypto_widget.py`
- The Fear & Greed indicator should now work!

## Free Tier Limits

The free Basic plan includes:
- **10,000 API calls per month**
- Perfect for this widget (updates every 30 seconds = ~86,400 calls/month for both cryptos)
- If you run the widget 8 hours/day, you'll use about 960 calls/day = ~28,800/month

**Tip:** The widget makes 2 API calls every 30 seconds (one for crypto prices, one for F&G). With the free tier's 10,000 calls/month, you can run it continuously for about 10 days, or 8 hours/day for the full month.

## Troubleshooting

**"Invalid CMC API key" error:**
- Double-check you copied the full API key correctly
- Make sure there are no extra spaces
- Verify your API key is active in your CMC dashboard

**"Please set your CoinMarketCap API key" error:**
- You forgot to replace "YOUR_API_KEY_HERE"
- Make sure you saved the file after editing

**Rate limit errors:**
- You've exceeded 10,000 calls for the month
- Wait until next month or upgrade to a paid plan
- Consider increasing the update interval to 60 seconds

## Why CoinMarketCap?

CoinMarketCap's Fear & Greed Index is:
- ✅ More comprehensive data sources
- ✅ Better market coverage
- ✅ More accurate sentiment analysis
- ✅ Industry standard for crypto metrics

## Need Help?

If you have issues:
1. Check the console output when running the widget
2. Verify your API key at: https://pro.coinmarketcap.com/account
3. Check your usage limits in the CMC dashboard
