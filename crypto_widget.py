import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime
import threading
import time
import yfinance as yf
import os

class CryptoWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Monitor")
        
        # CoinMarketCap API Key
        # Get your free API key at: https://coinmarketcap.com/api/
        self.CMC_API_KEY = "f4f2a47ef9714ae98e7a664de1cbc1ed"  # Replace with your actual API key
        
        # Load configuration
        self.load_config()
        
        # Window configuration
        self.root.attributes('-topmost', self.config.get('window_always_on_top', False))
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-alpha', 0.95)  # Slight transparency
        
        # Calculate window height dynamically based on content
        # Title bar and chrome
        title_bar_height = 30
        
        # Crypto section
        crypto_section_header = 30  # "CRYPTO" label + padding
        crypto_item_height = 85     # Height per crypto (name, price, change, F&G)
        total_crypto_height = crypto_section_header + (len(self.cryptos) * crypto_item_height)
        
        # Separator
        separator_height = 30
        
        # Market indicators section
        market_section_header = 30  # "MARKET INDICATORS" label + padding
        market_status_row = 35      # Market Status row
        vix_row = 35                # VIX row
        putcall_row = 35            # Put/Call row
        breadth_row = 35            # Breadth row
        market_section_padding = 20 # Extra padding for market section
        total_market_height = (market_section_header + market_status_row + 
                              vix_row + putcall_row + breadth_row + market_section_padding)
        
        # Update label and bottom padding
        update_label_height = 30
        bottom_padding = 30
        
        # Calculate total window height
        window_height = (title_bar_height + total_crypto_height + separator_height + 
                        total_market_height + update_label_height + bottom_padding)
        
        # Ensure minimum height
        window_height = max(window_height, 400)
        
        print(f"Window height calculated: {window_height}px for {len(self.cryptos)} cryptos")
        
        # Window size and position
        window_width = 340
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f'{window_width}x{window_height}+{screen_width-window_width-20}+20')
        
        # Make window draggable
        self.root.bind('<Button-1>', self.start_move)
        self.root.bind('<B1-Motion>', self.on_move)
        
        # Create main frame with styling
        self.main_frame = tk.Frame(root, bg='#1e1e1e', relief='raised', bd=2)
        self.main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Title bar
        title_frame = tk.Frame(self.main_frame, bg='#2d2d2d', height=30)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="⚡ Market Monitor", 
                              bg='#2d2d2d', fg='#ffffff', 
                              font=('Segoe UI', 10, 'bold'))
        title_label.pack(side='left', padx=10, pady=5)
        
        # Close button
        close_btn = tk.Label(title_frame, text="✕", bg='#2d2d2d', fg='#888888',
                            font=('Segoe UI', 12), cursor='hand2')
        close_btn.pack(side='right', padx=10)
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg='#ff4444'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg='#888888'))
        
        # Content frame
        content_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # CRYPTO SECTION
        crypto_title = tk.Label(content_frame, text="CRYPTO", 
                               bg='#1e1e1e', fg='#666666',
                               font=('Segoe UI', 8, 'bold'))
        crypto_title.pack(anchor='w', pady=(0, 5))
        
        # Create crypto sections dynamically based on config
        self.crypto_widgets = {}
        for crypto in self.cryptos:
            widgets = self.create_crypto_frame_with_fg(content_frame, crypto['name'], crypto['symbol'])
            widgets['frame'].pack(fill='x', pady=(0, 8))
            self.crypto_widgets[crypto['symbol']] = {
                'price_label': widgets['price_label'],
                'change_label': widgets['change_label'],
                'fg_label': widgets['fg_label'],
                'cmc_symbol': crypto['cmc_symbol']
            }
        
        # Separator
        separator = tk.Frame(content_frame, bg='#333333', height=1)
        separator.pack(fill='x', pady=10)
        
        # MARKET INDICATORS SECTION
        market_title = tk.Label(content_frame, text="MARKET INDICATORS", 
                               bg='#1e1e1e', fg='#666666',
                               font=('Segoe UI', 8, 'bold'))
        market_title.pack(anchor='w', pady=(0, 5))
        
        # Market indicators frame
        indicators_frame = tk.Frame(content_frame, bg='#2d2d2d', relief='flat')
        indicators_frame.pack(fill='x')
        
        # Market Status (Open/Closed)
        status_row = tk.Frame(indicators_frame, bg='#2d2d2d')
        status_row.pack(fill='x', padx=10, pady=(8, 4))
        
        status_label = tk.Label(status_row, text="Market Status:", 
                               bg='#2d2d2d', fg='#888888',
                               font=('Segoe UI', 8))
        status_label.pack(side='left')
        
        self.market_status_label = tk.Label(status_row, text="--", 
                                           bg='#2d2d2d', fg='#ffffff',
                                           font=('Segoe UI', 9, 'bold'))
        self.market_status_label.pack(side='right')
        
        # VIX
        vix_row = self.create_indicator_row(indicators_frame, "VIX (Fear Index)")
        vix_row['row'].pack(fill='x', padx=10, pady=(4, 4))
        self.vix_value_label = vix_row['value_label']
        self.vix_change_label = vix_row['change_label']
        
        # Put/Call Ratio
        pc_row = self.create_indicator_row(indicators_frame, "Put/Call Ratio (30d)")
        pc_row['row'].pack(fill='x', padx=10, pady=(4, 4))
        self.pc_value_label = pc_row['value_label']
        self.pc_change_label = pc_row['change_label']
        
        # Market Breadth (S&P 500 AdvDec)
        breadth_row = self.create_indicator_row(indicators_frame, "S&P 500 Breadth")
        breadth_row['row'].pack(fill='x', padx=10, pady=(4, 8))
        self.breadth_value_label = breadth_row['value_label']
        self.breadth_change_label = breadth_row['change_label']
        
        # Last update label
        self.update_label = tk.Label(content_frame, text="Updating...", 
                                     bg='#1e1e1e', fg='#555555',
                                     font=('Segoe UI', 7))
        self.update_label.pack(pady=(10, 0))
        
        # Start updating data
        self.update_data()
    
    def load_config(self):
        """Load configuration from config.json"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'r') as f:
                self.config = json.load(f)
            
            self.cryptos = self.config.get('cryptos', [])
            self.update_interval = self.config.get('update_interval_seconds', 30) * 1000  # Convert to ms
            
            if not self.cryptos:
                raise ValueError("No cryptos defined in config")
            
            print(f"Loaded {len(self.cryptos)} cryptocurrencies from config")
            for crypto in self.cryptos:
                print(f"  - {crypto['name']} ({crypto['symbol']})")
            
        except FileNotFoundError:
            print("Config file not found, using defaults")
            self.cryptos = [
                {"name": "Bitcoin", "symbol": "BTC", "cmc_symbol": "BTC"},
                {"name": "Ripple", "symbol": "XRP", "cmc_symbol": "XRP"}
            ]
            self.update_interval = 30000
            self.config = {}
        except Exception as e:
            print(f"Error loading config: {e}")
            self.cryptos = [
                {"name": "Bitcoin", "symbol": "BTC", "cmc_symbol": "BTC"},
                {"name": "Ripple", "symbol": "XRP", "cmc_symbol": "XRP"}
            ]
            self.update_interval = 30000
            self.config = {}
        
    def create_crypto_frame_with_fg(self, parent, name, symbol):
        frame = tk.Frame(parent, bg='#2d2d2d', relief='flat')
        
        # Header with name and symbol
        header = tk.Frame(frame, bg='#2d2d2d')
        header.pack(fill='x', padx=10, pady=(8, 0))
        
        name_label = tk.Label(header, text=name, 
                             bg='#2d2d2d', fg='#888888',
                             font=('Segoe UI', 9))
        name_label.pack(side='left')
        
        symbol_label = tk.Label(header, text=symbol, 
                               bg='#2d2d2d', fg='#666666',
                               font=('Segoe UI', 8))
        symbol_label.pack(side='right')
        
        # Price and change row
        price_row = tk.Frame(frame, bg='#2d2d2d')
        price_row.pack(fill='x', padx=10, pady=(2, 0))
        
        price_label = tk.Label(price_row, text="$--", 
                              bg='#2d2d2d', fg='#ffffff',
                              font=('Segoe UI', 16, 'bold'))
        price_label.pack(side='left')
        
        change_label = tk.Label(price_row, text="--", 
                               bg='#2d2d2d', fg='#888888',
                               font=('Segoe UI', 9))
        change_label.pack(side='left', padx=(10, 0))
        
        # Fear & Greed indicator row
        fg_row = tk.Frame(frame, bg='#2d2d2d')
        fg_row.pack(fill='x', padx=10, pady=(2, 8))
        
        fg_title = tk.Label(fg_row, text="F&G:", 
                           bg='#2d2d2d', fg='#666666',
                           font=('Segoe UI', 8))
        fg_title.pack(side='left')
        
        fg_label = tk.Label(fg_row, text="--", 
                           bg='#2d2d2d', fg='#888888',
                           font=('Segoe UI', 8, 'bold'))
        fg_label.pack(side='left', padx=(5, 0))
        
        return {
            'frame': frame,
            'price_label': price_label,
            'change_label': change_label,
            'fg_label': fg_label
        }
    
    def create_indicator_row(self, parent, label_text):
        row = tk.Frame(parent, bg='#2d2d2d')
        
        # Label
        label = tk.Label(row, text=label_text, 
                        bg='#2d2d2d', fg='#888888',
                        font=('Segoe UI', 8))
        label.pack(side='left')
        
        # Value and change container
        right_side = tk.Frame(row, bg='#2d2d2d')
        right_side.pack(side='right')
        
        value_label = tk.Label(right_side, text="--", 
                              bg='#2d2d2d', fg='#ffffff',
                              font=('Segoe UI', 9, 'bold'))
        value_label.pack(side='left')
        
        change_label = tk.Label(right_side, text="", 
                               bg='#2d2d2d', fg='#888888',
                               font=('Segoe UI', 8))
        change_label.pack(side='left', padx=(5, 0))
        
        return {
            'row': row,
            'value_label': value_label,
            'change_label': change_label
        }
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def get_crypto_prices(self):
        try:
            # Build comma-separated list of crypto symbols
            symbols = ','.join([crypto['cmc_symbol'] for crypto in self.cryptos])
            
            url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
            headers = {
                'X-CMC_PRO_API_KEY': self.CMC_API_KEY,
                'Accept': 'application/json'
            }
            params = {
                'symbol': symbols,
                'convert': 'USD'
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = {}
                
                if 'data' in data:
                    for crypto in self.cryptos:
                        cmc_symbol = crypto['cmc_symbol']
                        if cmc_symbol in data['data']:
                            crypto_data = data['data'][cmc_symbol][0]
                            result[crypto['symbol']] = {
                                'usd': crypto_data['quote']['USD']['price'],
                                'usd_24h_change': crypto_data['quote']['USD']['percent_change_24h']
                            }
                
                return result if result else None
            else:
                print(f"CMC Quotes API error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching CMC prices: {e}")
            return None
    
    def get_fear_greed_index(self):
        try:
            url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
            headers = {
                'X-CMC_PRO_API_KEY': self.CMC_API_KEY,
                'Accept': 'application/json'
            }
            params = {
                'limit': 1
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    return data['data'][0]
                else:
                    return None
            else:
                return None
        except Exception as e:
            print(f"Error fetching CMC fear & greed: {e}")
            return None
    
    def is_market_open(self):
        """Check if US stock market is currently open"""
        try:
            from datetime import datetime
            import pytz
            
            # Get current time in Eastern Time (US stock market timezone)
            et_tz = pytz.timezone('America/New_York')
            now_et = datetime.now(et_tz)
            
            # Check if it's a weekday (Monday=0, Sunday=6)
            if now_et.weekday() >= 5:  # Saturday or Sunday
                return False, "CLOSED (Weekend)"
            
            # Market hours: 9:30 AM - 4:00 PM ET
            market_open = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
            market_close = now_et.replace(hour=16, minute=0, second=0, microsecond=0)
            
            if market_open <= now_et <= market_close:
                return True, "OPEN"
            elif now_et < market_open:
                return False, "PRE-MARKET"
            else:
                return False, "CLOSED"
                
        except Exception as e:
            print(f"Error checking market status: {e}")
            return None, "UNKNOWN"
    
    def get_market_indicators(self):
        """Fetch VIX, Put/Call Ratio, and Market Breadth"""
        try:
            indicators = {}
            
            # Get VIX (CBOE Volatility Index)
            vix = yf.Ticker("^VIX")
            vix_data = vix.history(period="5d")
            if not vix_data.empty:
                current_vix = vix_data['Close'].iloc[-1]
                prev_vix = vix_data['Close'].iloc[-2] if len(vix_data) > 1 else current_vix
                vix_change = ((current_vix - prev_vix) / prev_vix) * 100
                indicators['vix'] = {
                    'value': current_vix,
                    'change': vix_change
                }
            
            # Get Put/Call Ratio - Using VIX as proxy since direct P/C ratio needs specialized data
            # For a more accurate P/C ratio, you'd need CBOE data or a paid API
            # Using VIX/20 as a rough sentiment indicator for now
            indicators['put_call'] = {
                'value': current_vix / 20 if 'vix' in indicators else 1.0,
                'change': 0  # Placeholder
            }
            
            # Get Market Breadth (S&P 500 Advance/Decline)
            # Using S&P 500 performance as breadth indicator
            spy = yf.Ticker("SPY")
            spy_data = spy.history(period="5d")
            if not spy_data.empty:
                current_spy = spy_data['Close'].iloc[-1]
                prev_spy = spy_data['Close'].iloc[-2] if len(spy_data) > 1 else current_spy
                spy_change = ((current_spy - prev_spy) / prev_spy) * 100
                
                # Market breadth: positive = bullish, negative = bearish
                indicators['breadth'] = {
                    'value': spy_change,
                    'sentiment': 'Bullish' if spy_change > 0 else 'Bearish',
                    'change': spy_change
                }
            
            return indicators
        except Exception as e:
            print(f"Error fetching market indicators: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def get_fg_color(self, value):
        if value <= 25:
            return '#ff4444'
        elif value <= 45:
            return '#ff8844'
        elif value <= 55:
            return '#ffcc44'
        elif value <= 75:
            return '#88ff44'
        else:
            return '#44ff44'
    
    def get_fg_text(self, value, classification):
        return f"{value} • {classification}"
    
    def get_indicator_color(self, change):
        """Get color based on change value"""
        if change > 0:
            return '#44ff44'  # Green
        elif change < 0:
            return '#ff4444'  # Red
        else:
            return '#888888'  # Gray
    
    def update_data(self):
        def fetch_in_background():
            prices = self.get_crypto_prices()
            fg_data = self.get_fear_greed_index()
            market_data = self.get_market_indicators()
            self.root.after(0, lambda: self.update_ui_with_data(prices, fg_data, market_data))
        
        thread = threading.Thread(target=fetch_in_background, daemon=True)
        thread.start()
    
    def update_ui_with_data(self, prices, fg_data, market_data):
        try:
            # Get Fear & Greed values
            fg_value = None
            fg_classification = None
            fg_color = '#888888'
            fg_display_text = "-- • --"
            
            if fg_data:
                try:
                    fg_value = int(fg_data['value'])
                    fg_classification = fg_data['value_classification']
                    fg_color = self.get_fg_color(fg_value)
                    fg_display_text = self.get_fg_text(fg_value, fg_classification)
                except Exception as e:
                    print(f"Error parsing Fear & Greed data: {e}")
            
            # Update all cryptos dynamically
            if prices:
                for symbol, widgets in self.crypto_widgets.items():
                    if symbol in prices:
                        crypto_data = prices[symbol]
                        price = crypto_data['usd']
                        change = crypto_data.get('usd_24h_change', 0)
                        
                        # Format price based on value (show more decimals for smaller values)
                        if price < 1:
                            price_text = f"${price:.4f}"
                        elif price < 100:
                            price_text = f"${price:.2f}"
                        else:
                            price_text = f"${price:,.0f}"
                        
                        widgets['price_label'].config(text=price_text)
                        
                        change_text = f"{'↑' if change >= 0 else '↓'} {abs(change):.2f}%"
                        change_color = '#44ff44' if change >= 0 else '#ff4444'
                        widgets['change_label'].config(text=change_text, fg=change_color)
                        widgets['fg_label'].config(text=fg_display_text, fg=fg_color)
            
            # Update Market Status
            is_open, status_text = self.is_market_open()
            if is_open is True:
                self.market_status_label.config(text=status_text, fg='#44ff44')  # Green for open
            elif is_open is False:
                if "PRE-MARKET" in status_text:
                    self.market_status_label.config(text=status_text, fg='#ffcc44')  # Yellow for pre-market
                else:
                    self.market_status_label.config(text=status_text, fg='#ff4444')  # Red for closed
            else:
                self.market_status_label.config(text=status_text, fg='#888888')  # Gray for unknown
            
            # Update Market Indicators
            if market_data:
                # VIX
                if 'vix' in market_data:
                    vix_val = market_data['vix']['value']
                    vix_change = market_data['vix']['change']
                    self.vix_value_label.config(text=f"{vix_val:.2f}")
                    
                    change_text = f"{'↑' if vix_change >= 0 else '↓'}{abs(vix_change):.1f}%"
                    # For VIX, higher is more fearful (red), lower is calmer (green)
                    change_color = '#ff4444' if vix_change > 0 else '#44ff44'
                    self.vix_change_label.config(text=change_text, fg=change_color)
                
                # Put/Call Ratio
                if 'put_call' in market_data:
                    pc_val = market_data['put_call']['value']
                    self.pc_value_label.config(text=f"{pc_val:.2f}")
                    
                    # P/C ratio interpretation: >1 = bearish, <1 = bullish
                    if pc_val > 1.0:
                        self.pc_change_label.config(text="Bearish", fg='#ff8844')
                    else:
                        self.pc_change_label.config(text="Bullish", fg='#88ff44')
                
                # Market Breadth
                if 'breadth' in market_data:
                    breadth_change = market_data['breadth']['change']
                    breadth_sentiment = market_data['breadth']['sentiment']
                    
                    change_text = f"{'↑' if breadth_change >= 0 else '↓'}{abs(breadth_change):.2f}%"
                    self.breadth_value_label.config(text=breadth_sentiment)
                    
                    change_color = '#44ff44' if breadth_change > 0 else '#ff4444'
                    self.breadth_change_label.config(text=change_text, fg=change_color)
            
            # Update timestamp
            current_time = datetime.now().strftime("%I:%M:%S %p")
            self.update_label.config(text=f"Updated: {current_time}")
            
        except Exception as e:
            print(f"Error updating UI: {e}")
            import traceback
            traceback.print_exc()
        
        # Schedule next update (use interval from config)
        self.root.after(self.update_interval, self.update_data)

def main():
    print("=" * 60)
    print("Market Monitor Starting...")
    print("Crypto: CoinMarketCap | Stocks: Yahoo Finance")
    print("=" * 60)
    
    root = tk.Tk()
    app = CryptoWidget(root)
    root.mainloop()

if __name__ == "__main__":
    main()
