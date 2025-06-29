import pandas as pd
from datetime import timedelta

def overall_sentiment(sentiments):
    """Calculate overall sentiment from numeric scores (-2 to 2)"""
    if not sentiments:
        return 'No Data'
    
    # Convert to numeric if they're strings
    numeric_sentiments = []
    for sentiment in sentiments:
        if isinstance(sentiment, str):
            try:
                numeric_sentiments.append(float(sentiment))
            except ValueError:
                numeric_sentiments.append(0)
        else:
            numeric_sentiments.append(sentiment)
    
    if not numeric_sentiments:
        return 'No Data'
    
    avg_score = sum(numeric_sentiments) / len(numeric_sentiments)
    
    # Convert average score to sentiment label
    if avg_score >= 1.5:
        return 'Very Positive!'
    elif avg_score >= 0.5:
        return 'Positive'
    elif avg_score >= -0.5:
        return 'Neutral'
    elif avg_score >= -1.5:
        return 'Negative'
    else:
        return 'Very Negative!'

def main():
    # Read the sentiment data that geminiAPI.py has already processed
    try:
        results_df = pd.read_csv('sentiment_data.csv')
        print(f"Loaded {len(results_df)} sentiment records from sentiment_data.csv")
    except FileNotFoundError:
        print("sentiment_data.csv not found. Please run geminiAPI.py first to generate the sentiment data.")
        return
    
    # Check that the required columns are present
    if not {'ticker', 'date', 'sentiment_value'}.issubset(results_df.columns):
        print("CSV must contain 'ticker', 'date', and 'sentiment_value' columns.")
        return
    
    # Convert date column to datetime
    results_df['date'] = pd.to_datetime(results_df['date'], format='%Y-%m-%d', errors='coerce')
    
    # Generate summary statistics
    latest_date = results_df['date'].max() if not results_df.empty else None
    if latest_date:
        output_rows = []
        
        for ticker in results_df['ticker'].dropna().unique():
            company_df = results_df[results_df['ticker'] == ticker]
            
            # Create masks for different time periods
            mask_24h = company_df['date'] >= (latest_date - timedelta(days=1))
            mask_7d = company_df['date'] >= (latest_date - timedelta(days=6))
            mask_30d = company_df['date'] >= (latest_date - timedelta(days=29))
            
            # Get sentiment values for each period
            sentiment_24h = overall_sentiment(company_df.loc[mask_24h, 'sentiment_value'].tolist())
            sentiment_7d = overall_sentiment(company_df.loc[mask_7d, 'sentiment_value'].tolist())
            sentiment_30d = overall_sentiment(company_df.loc[mask_30d, 'sentiment_value'].tolist())
            
            output_rows.append({
                'ticker': ticker,
                'day': sentiment_24h,
                'week': sentiment_7d,
                'month': sentiment_30d
            })
        
        summary_df = pd.DataFrame(output_rows)
        summary_df.to_csv('sentiment_summary.csv', index=False)
        print(f"Summary saved to 'sentiment_summary.csv' with {len(summary_df)} companies.")
    else:
        print("No valid dates found in the data.")

if __name__ == "__main__":
    main() 