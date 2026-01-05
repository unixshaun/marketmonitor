# Market Monitor Widget

> A sleek, customizable Windows desktop widget for real-time cryptocurrency and stock market monitoring

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Overview

Market Monitor Widget is a lightweight desktop application that provides real-time tracking of cryptocurrency prices and key stock market indicators in a single, always-accessible window. Built with Python and Tkinter, it's designed for traders, investors, and crypto enthusiasts who want instant access to market data.

## ✨ Features

### Cryptocurrency Tracking
- 🪙 **Customizable crypto portfolio** - Track any cryptocurrencies via simple config file
- 💰 **Real-time prices** from CoinMarketCap API
- 📈 **24-hour change percentages** with color-coded indicators
- 😱 **Fear & Greed Index** for each crypto showing market sentiment
- 🎨 **Smart price formatting** (more decimals for smaller coins)

### Stock Market Indicators
- 📊 **Market Status** - Real-time US stock market open/closed indicator
- 📉 **VIX (Fear Index)** - CBOE Volatility Index with daily change
- 🎯 **Put/Call Ratio** - Options market sentiment (Bullish/Bearish)
- 📈 **S&P 500 Breadth** - Overall market direction indicator

### User Experience
- ⚙️ **Fully configurable** via JSON config file
- 🎨 **Modern dark theme** optimized for Windows 11
- 📏 **Auto-sizing window** - Adjusts height based on number of cryptos
- 🖱️ **Draggable** - Position anywhere on your screen
- 🔄 **Configurable refresh rate** (default: 30 seconds)
- 📌 **Optional always-on-top** mode
- 💨 **Lightweight** - Minimal CPU and memory usage

## 📸 Screenshot

![Market Monitor Widget](screenshot.png)
*Example showing BTC, ETH, XRP with market indicators*

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** - [Download here](https://www.python.org/downloads/)
- **CoinMarketCap API Key** - [Get free API key](https://coinmarketcap.com/api/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/market-monitor-widget.git
   cd market-monitor-widget
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   - Open `crypto_widget.py` in a text editor
   - Find line 14: `self.CMC_API_KEY = "YOUR_API_KEY_HERE"`
   - Replace with your actual CoinMarketCap API key
   - Save the file

4. **Set up your config**
   ```bash
   copy config.example.json config.json
   ```
   Edit `config.json` to customize which cryptos to track

5. **Run the widget**
   ```bash
   python crypto_widget.py
   ```

## ⚙️ Configuration

Edit `config.json` to customize your experience:

```json
{
  "cryptos": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "cmc_symbol": "BTC"
    },
    {
      "name": "Ethereum",
      "symbol": "ETH",
      "cmc_symbol": "ETH"
    }
  ],
  "update_interval_seconds": 30,
  "window_always_on_top": false
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `cryptos` | Array | BTC, XRP, ETH | List of cryptocurrencies to track |
| `update_interval_seconds` | Number | 30 | How often to refresh data (seconds) |
| `window_always_on_top` | Boolean | false | Keep widget above other windows |

### Adding Cryptocurrencies

Popular cryptocurrencies you can add:

```json
{"name": "Bitcoin", "symbol": "BTC", "cmc_symbol": "BTC"}
{"name": "Ethereum", "symbol": "ETH", "cmc_symbol": "ETH"}
{"name": "Ripple", "symbol": "XRP", "cmc_symbol": "XRP"}
{"name": "Cardano", "symbol": "ADA", "cmc_symbol": "ADA"}
{"name": "Solana", "symbol": "SOL", "cmc_symbol": "SOL"}
{"name": "Polkadot", "symbol": "DOT", "cmc_symbol": "DOT"}
{"name": "Dogecoin", "symbol": "DOGE", "cmc_symbol": "DOGE"}
{"name": "Avalanche", "symbol": "AVAX", "cmc_symbol": "AVAX"}
{"name": "Polygon", "symbol": "MATIC", "cmc_symbol": "MATIC"}
{"name": "Chainlink", "symbol": "LINK", "cmc_symbol": "LINK"}
```

See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for the complete list and detailed configuration options.

## 🎯 Usage

### Running the Widget

**Standard mode:**
```bash
python crypto_widget.py
```

**Silent mode (no console window):**
```bash
pythonw crypto_widget.py
```

### Creating a Desktop Shortcut

**Windows:**
1. Double-click `create_desktop_shortcut.vbs`
2. A shortcut will appear on your desktop

Or manually:
1. Right-click `run_crypto_widget.bat`
2. Select "Send to" → "Desktop (create shortcut)"

### Auto-start on Windows Login

1. Press `Win + R`, type `shell:startup`, press Enter
2. Copy the desktop shortcut into the Startup folder
3. Widget will now launch automatically when you log in

## 📊 Market Indicators Explained

### Fear & Greed Index (0-100)
- **0-25**: Extreme Fear (Red) 🔴
- **26-45**: Fear (Orange) 🟠
- **46-55**: Neutral (Yellow) 🟡
- **56-75**: Greed (Light Green) 🟢
- **76-100**: Extreme Greed (Green) 🟢

### VIX (Volatility Index)
- **Below 15**: Low volatility, calm markets
- **15-20**: Normal volatility
- **20-30**: Elevated volatility
- **Above 30**: High volatility, market fear

### Put/Call Ratio
- **Above 1.0**: Bearish sentiment (more puts than calls)
- **Below 1.0**: Bullish sentiment (more calls than puts)

### Market Status
- **OPEN** 🟢: Market is trading (9:30 AM - 4:00 PM ET, Mon-Fri)
- **PRE-MARKET** 🟡: Before market opens
- **CLOSED** 🔴: Market closed for the day
- **CLOSED (Weekend)** 🔴: Saturday or Sunday

## 🔧 Troubleshooting

### Widget won't start
- Ensure Python 3.7+ is installed: `python --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that `config.json` exists and is valid JSON

### No crypto prices showing
- Verify your CoinMarketCap API key is correct
- Check your internet connection
- Ensure you haven't exceeded API rate limits (10,000 calls/month on free tier)

### Market indicators not visible
- The window auto-sizes based on crypto count
- Try restarting the widget
- Check console output for errors

### API Rate Limits
With the free CoinMarketCap tier (10,000 calls/month):
- **30-second updates**: ~86,400 calls/month (24/7) - exceeds limit
- **60-second updates**: ~43,200 calls/month (24/7) - exceeds limit
- **Recommended**: 60-second updates, run 8-10 hours/day = ~14,400-18,000 calls/month

To stay within limits, either:
- Increase `update_interval_seconds` to 60 or 120
- Run the widget only when actively trading/monitoring

## 🛠️ Tech Stack

- **Python 3.7+** - Core language
- **Tkinter** - GUI framework (built-in with Python)
- **Requests** - HTTP library for API calls
- **yfinance** - Yahoo Finance data for stock indicators
- **pytz** - Timezone handling for market hours

## 📡 API Sources

- **Crypto Prices & Fear/Greed**: [CoinMarketCap API](https://coinmarketcap.com/api/) (Free tier: 10,000 calls/month)
- **Stock Market Data**: [Yahoo Finance](https://finance.yahoo.com/) via yfinance (Free, unlimited)

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs by opening an issue
- 💡 Suggest new features or improvements
- 🔧 Submit pull requests with bug fixes or new features
- 📖 Improve documentation
- ⭐ Star the project if you find it useful!

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-new-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -am 'Add some feature'`
6. Push: `git push origin feature/my-new-feature`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CoinMarketCap](https://coinmarketcap.com/) for cryptocurrency data and Fear & Greed Index
- [Yahoo Finance](https://finance.yahoo.com/) for stock market data
- [Alternative.me](https://alternative.me/) for the original Fear & Greed Index methodology

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/market-monitor-widget/issues)
- **Documentation**: See [CONFIG_GUIDE.md](CONFIG_GUIDE.md) for detailed configuration
- **API Setup**: See [CMC_API_SETUP.md](CMC_API_SETUP.md) for CoinMarketCap API key instructions

## 🗺️ Roadmap

Planned features for future releases:

- [ ] Multiple theme support (light/dark/custom)
- [ ] Price alerts and notifications
- [ ] Historical price charts
- [ ] Portfolio tracking with holdings
- [ ] Customizable market indicators
- [ ] Support for additional crypto exchanges
- [ ] macOS and Linux support

## ⚠️ Disclaimer

This tool is for informational purposes only. It is not financial advice. Always do your own research before making investment decisions. The creators of this tool are not responsible for any financial losses.

---

**Made with ❤️ by crypto and stock market enthusiasts**

*If you find this tool useful, please consider giving it a ⭐ on GitHub!*
