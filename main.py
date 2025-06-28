#All the print statements are for debugging if we want to make changes
import csv
from eventregistry import *
from datetime import date, timedelta
import time

def main():
    event = EventRegistry(apiKey="632ea8d1-1f73-4d18-85e6-29d10e8acd07")
    yahoo_finance = event.getNewsSourceUri("finance.yahoo.com")
    
    companies_to_query = [
        {"name": "Tesla", "keywords": ["Tesla OR TSLA"]},
        {"name": "Apple", "keywords": ["Apple OR AAPL"]},
        {"name": "Microsoft", "keywords": ["Microsoft OR MSFT"]},
        {"name": "Amazon", "keywords": ["Amazon OR AMZN"]},
        {"name": "Google", "keywords": ["Google OR GOOGL"]},
        {"name": "Meta", "keywords": ["Meta OR META"]},
        {"name": "Nvidia", "keywords": ["Nvidia OR NVDA"]}
    ]
    CSV_HEADER = ["Company", "Date", "Title"]

    #print("Opening dataSet.csv for writing...")
    with open("dataSet.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADER)
        #print("CSV header written. Starting data fetch...")

        # Loop through each company
        for company in companies_to_query:
            company_name = company["name"]
            keywords = company["keywords"]
            today_date = date.today()

            for day_offset in range(5):
                target_date = today_date - timedelta(days=day_offset)
                date_str = target_date.strftime("%Y-%m-%d")
                #print(f"  [?] Querying {company_name} for date: {date_str}")

                try:
                    # Create a new, specific query for each day.
                    temp_query = QueryArticlesIter(
                        keywords=keywords,
                        sourceUri=yahoo_finance,
                        dataType=["news"],
                        dateStart=date_str,
                        dateEnd=date_str
                    )
                    results = temp_query.execQuery(
                        event,
                        sortBy="date",
                        maxItems=10
                    )
                    
                    # Process results for the current day
                    for article in results:
                        article_title = article.get('title', 'No Title Found')
                        article_date = article.get('date', 'No Date Found')
                        writer.writerow([company_name, article_date, article_title])
        
                except Exception as e:
                    print(f"  [!] An error occurred on this day for {company_name}: {e}")
            
            #print(f"--- Finished: {company_name} ---")

    #print("\n==========================================")
    #print("      All companies processed!")
    #print("==========================================")
if __name__ == "__main__":
    main()
