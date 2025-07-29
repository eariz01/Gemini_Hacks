import google.generativeai as genai

genai.configure(api_key="Add Personal API Key")
model = genai.GenerativeModel("gemini-2.5-flash")

def classify_data_sentiment(headline: str, date: str = None):
  prompt = f'Classify the Sentiment of the following Headline as Positive, Negative, or Neutral and give a brief reason as to why:\n\n"{headline}"'

  response = model.generate_content(prompt)

  return{
    "headline" : headline,
    "Date Posted" : date,
    "gemini_response": response.text
  }

test_result = classify_data_sentiment("Amazon shares a drop after a weak holiday forecast\n")
print(test_result)

                           
  
