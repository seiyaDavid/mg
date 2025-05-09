# Trade Agent

[Previous sections remain unchanged until Non-Technical Guide...]

## 📚 Non-Technical Guide to Trading Terms

### Price Analysis Terms
1. **Volatility**
   - What it means: How much a stock's price moves up and down
   - Why it matters: Higher volatility means higher risk and potential for bigger gains or losses
   - How we calculate it: We look at how much the stock price varies from its average over time
   - Example: A stock with 20% volatility means its price typically moves up or down by 20% over a year. For a $100 stock, this means it might move between $80 and $120 in a typical year.

2. **Price Change**
   - What it means: How much the stock price has moved over a period
   - Why it matters: Shows the stock's recent performance trend
   - How we calculate it: We compare the current price to the price at the start of our analysis period
   - Example: A -11.93% price change means a $100 stock has decreased to $88.07 over the period.

### Technical Indicators
1. **MACD (Moving Average Convergence Divergence)**
   - What it means: A tool that shows if a stock is trending up or down
   - Why it matters: Helps identify potential buying or selling opportunities
   - How we calculate it: We compare two moving averages of the stock price
   - Example: A MACD of -2.5151 suggests a downward trend, while +14.1768 indicates a strong upward trend.

2. **RSI (Relative Strength Index)**
   - What it means: A measure of how overbought or oversold a stock is
   - Why it matters: Helps identify if a stock might be due for a price correction
   - How we calculate it: We look at recent price gains versus losses
   - Example: RSI of 87.12 (like MSFT) suggests the stock might be overbought, while 50.60 (like AAPL) indicates neutral conditions.

### Risk Metrics
1. **Risk Score (0-100)**
   - What it means: A single number representing overall risk
   - Why it matters: Higher scores mean higher risk
   - How we calculate it: We combine scores from volatility, technical indicators, sentiment, and price changes
   - Example: A risk score of 67.60 (like AAPL) indicates moderate-high risk, while 59.26 (like MSFT) suggests moderate risk.

2. **CVaR (Conditional Value at Risk)**
   - What it means: The average loss we might expect in worst-case scenarios
   - Why it matters: Helps understand potential downside risk
   - How we calculate it: We look at the average of the worst 5% of daily returns
   - Example: A CVaR of -0.095 means that in the worst 5% of trading days, the stock loses an average of 0.095% of its value. For a $100,000 investment, this means you might expect to lose $95 in these worst-case scenarios.

3. **Sharpe Ratio**
   - What it means: How much return you get for the risk you take
   - Why it matters: Higher ratios mean better risk-adjusted returns
   - How we calculate it: We compare returns to the risk-free rate and volatility
   - Example: A Sharpe ratio of 1.5 means the stock returns 1.5% for each 1% of risk taken. A ratio above 1.0 is generally considered good.

4. **Sortino Ratio**
   - What it means: Similar to Sharpe ratio, but focuses on downside risk
   - Why it matters: Shows how well the stock performs in bad markets
   - How we calculate it: We compare returns to downside volatility
   - Example: A Sortino ratio of 2.0 means the stock returns 2% for each 1% of downside risk. Higher is better, with 2.0 being considered excellent.

5. **Calmar Ratio**
   - What it means: Return compared to maximum loss
   - Why it matters: Shows if returns are worth the risk of maximum loss
   - How we calculate it: We divide annual return by maximum drawdown
   - Example: A Calmar ratio of 1.5 means the annual return is 1.5 times the maximum loss. A ratio above 1.0 suggests good risk-adjusted returns.

### Sentiment Analysis
1. **Compound Score (-1 to 1)**
   - What it means: Overall market sentiment about the stock
   - Why it matters: Shows if news and social media are positive or negative
   - How we calculate it: We analyze news headlines and social media posts
   - Example: A score of 0.31 (like AAPL) indicates moderately positive sentiment, while -0.5 would indicate negative sentiment.

2. **Sentiment Volatility**
   - What it means: How much sentiment changes over time
   - Why it matters: High volatility might indicate uncertainty
   - How we calculate it: We measure how much sentiment scores vary
   - Example: A volatility of 0.51 (like AAPL) indicates moderate sentiment swings, while 0.20 (like GOOGL) suggests more stable sentiment.

### Component Scores
1. **Volatility Score**
   - What it means: How much the stock price moves around
   - Why it matters: Higher scores mean more risk
   - How we calculate it: Based on price movement patterns
   - Example: A volatility of 0.3968 (like AAPL) indicates moderate price swings, while 0.3065 (like MSFT) suggests more stable prices.

2. **Technical Score**
   - What it means: What technical indicators suggest
   - Why it matters: Shows if technical analysis suggests buying or selling
   - How we calculate it: We combine MACD and RSI signals
   - Example: A high technical score with RSI of 87.12 and positive MACD suggests strong upward momentum.

3. **Sentiment Score**
   - What it means: How the market feels about the stock
   - Why it matters: Shows if news and social media are positive or negative
   - How we calculate it: We analyze news and social media sentiment
   - Example: A compound score of 0.31 with low volatility suggests consistent positive sentiment.

4. **Price Change Score**
   - What it means: How the stock price has moved recently
   - Why it matters: Shows recent performance trend
   - How we calculate it: We look at recent price movements
   - Example: A -11.93% change (like AAPL) indicates a significant price decline, while +4.82% (like MSFT) shows positive momentum.

[Rest of the README remains unchanged...]
