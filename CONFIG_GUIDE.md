# Configuration Guide

The Market Monitor widget can be customized using the `config.json` file.

## Configuration File Location

The `config.json` file should be in the same directory as `crypto_widget.py`.

## Configuration Options

### Example config.json

```json
{
  "cryptos": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "cmc_symbol": "BTC"
    },
    {
      "name": "Ripple",
      "symbol": "XRP",
      "cmc_symbol": "XRP"
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

## Settings Explained

### `cryptos` (Array of Objects)
List of cryptocurrencies to track. Each crypto has three properties:

- **`name`** (string): Display name (e.g., "Bitcoin", "Ethereum")
- **`symbol`** (string): Short symbol for display (e.g., "BTC", "ETH")
- **`cmc_symbol`** (string): CoinMarketCap API symbol (usually same as symbol)

**Example - Adding Cardano:**
```json
{
  "name": "Cardano",
  "symbol": "ADA",
  "cmc_symbol": "ADA"
}
```

### `update_interval_seconds` (Number)
How often to refresh data in seconds.

- **Default**: 30 seconds
- **Recommended**: 30-60 seconds
- **Minimum**: 15 seconds (to avoid API rate limits)

**Example:**
```json
"update_interval_seconds": 60
```

### `window_always_on_top` (Boolean)
Whether the widget stays on top of other windows.

- **`true`**: Widget always visible above other windows
- **`false`**: Widget behaves like a normal window (can be covered by other apps)

**Example:**
```json
"window_always_on_top": true
```

## Popular Cryptocurrencies

Here are some popular cryptos you can add:

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
{"name": "Litecoin", "symbol": "LTC", "cmc_symbol": "LTC"}
{"name": "Uniswap", "symbol": "UNI", "cmc_symbol": "UNI"}
{"name": "Stellar", "symbol": "XLM", "cmc_symbol": "XLM"}
{"name": "Cosmos", "symbol": "ATOM", "cmc_symbol": "ATOM"}
```

## Complete Example with 5 Cryptos

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
    },
    {
      "name": "Ripple",
      "symbol": "XRP",
      "cmc_symbol": "XRP"
    },
    {
      "name": "Cardano",
      "symbol": "ADA",
      "cmc_symbol": "ADA"
    },
    {
      "name": "Solana",
      "symbol": "SOL",
      "cmc_symbol": "SOL"
    }
  ],
  "update_interval_seconds": 60,
  "window_always_on_top": false
}
```

## Tips

1. **Window Size**: The widget automatically adjusts height based on the number of cryptos
2. **API Limits**: More cryptos = more API calls. Keep it under 10 for optimal performance
3. **Update Frequency**: Longer intervals (60s) help you stay within API limits
4. **Always on Top**: Set to `false` if you want the widget to behave like a normal window

## Troubleshooting

**Widget won't start:**
- Check that your JSON syntax is correct (commas, brackets, quotes)
- Use a JSON validator like jsonlint.com
- If config.json has errors, the widget will fall back to default cryptos (BTC & XRP)

**Crypto not showing:**
- Verify the `cmc_symbol` is correct
- Check CoinMarketCap's website for the exact symbol
- Some cryptos may have different symbols on CMC

**Changes not appearing:**
- Make sure you saved config.json
- Restart the widget completely
- Check the console output for error messages

## Applying Changes

After editing `config.json`:
1. Save the file
2. Close the widget completely
3. Run `python crypto_widget.py` again

The new configuration will be loaded on startup!
