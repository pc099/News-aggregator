import json,os
import pandas as pd
import urllib.request
from utils import countdown

def Catagorical_Retrive_news(category, apikey, seconds, headline_count, country):
    """
    Retrieve news articles for each category and country.
    """
    Final_dict = {
        'Title': [],
        'Description': [],
        'Category': [],
        'Country': []
    }

    for cat in category:
        for cnt in country:
            url = f"https://gnews.io/api/v4/top-headlines?category={cat}&lang=en&country={cnt}&max={headline_count}&apikey={apikey}"

            print(f"Category: {cat} For country {cnt}")
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode("utf-8"))
                articles = data["articles"]

                for article in articles:
                    title = article['title']
                    description = article['description']
                    country = cnt

                    Final_dict['Title'].append(title)
                    Final_dict['Description'].append(description)
                    Final_dict['Category'].append(cat)
                    Final_dict['Country'].append(country)

                    print(f"Title: {title}")
                    print(f"Description: {description}")

            print(f"The {cat} Category Request is finished...")
            print(f"Waiting for {seconds} seconds...")
            countdown(seconds)

    return Final_dict


if __name__ == '__main__':
    seconds = 10
    headline_count = 100
    apikey = "X"
    category = ["general", "world", "nation", "business", "technology", "entertainment", "sports", "science", "health"]
    value = ['au', 'br', 'ca', 'cn', 'eg', 'fr', 'de', 'gr', 'hk', 'in', 'ie', 'il', 'it', 'jp', 'nl', 'no', 'pk',
             'pe', 'ph', 'pt', 'ro', 'ru', 'sg', 'es', 'se', 'ch', 'tw', 'ua', 'gb', 'us']
    file_path = os.path.join(os.getcwd(), "Headlines_dataset.csv")

    dataset = Catagorical_Retrive_news(category=category, apikey=apikey, seconds=seconds,
                                       headline_count=headline_count, country=value)

    df = pd.DataFrame(dataset)
    df.to_csv(file_path, index=False, mode='a')


data = {
    'Name': ['Australia', 'Brazil', 'Canada', 'China', 'Egypt', 'France', 'Germany', 'Greece', 'Hong Kong', 'India',
             'Ireland', 'Israel', 'Italy', 'Japan', 'Netherlands', 'Norway', 'Pakistan', 'Peru', 'Philippines',
             'Portugal', 'Romania', 'Russian Federation', 'Singapore', 'Spain', 'Sweden', 'Switzerland', 'Taiwan',
             'Ukraine', 'United Kingdom', 'United States'],
    'Value': ['au', 'br', 'ca', 'cn', 'eg', 'fr', 'de', 'gr', 'hk', 'in', 'ie', 'il', 'it', 'jp', 'nl', 'no', 'pk',
              'pe', 'ph', 'pt', 'ro', 'ru', 'sg', 'es', 'se', 'ch', 'tw', 'ua', 'gb', 'us']
}
