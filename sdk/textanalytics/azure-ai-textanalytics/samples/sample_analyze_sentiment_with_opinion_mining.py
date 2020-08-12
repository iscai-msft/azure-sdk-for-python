# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_sentiment_with_opinion_mining.py

DESCRIPTION:
    This sample demonstrates how to analyze sentiment on a more granular level, mining individual
    opinions from reviews (also known as aspect-based sentiment analysis).
    This feature is only available for clients with api version v3.1-preview.1.

    In this sample, we will be a customer who is trying to figure out whether they should stay
    at a specific hotel. We will be looking at which aspects of the hotel are good, and which are
    not.

USAGE:
    python sample_analyze_sentiment_with_opinion_mining.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_TEXT_ANALYTICS_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_TEXT_ANALYTICS_KEY - your Text Analytics subscription key
"""

import os


class AnalyzeSentimentWithOpinionMiningSample(object):
    def sample_analyze_sentiment_with_opinion_mining(self):
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.textanalytics import TextAnalyticsClient
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        endpoint = os.environ["AZURE_TEXT_ANALYTICS_ENDPOINT"]
        key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]

        text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        print("In this sample we will be combing through the reviews of a potential hotel to stay at: Hotel Foo.")

        print(
            "I first found a handful of reviews for Hotel Foo. Let's see if I want to stay here."
        )

        documents = [
            "The food and service were unacceptable, but the concierge were nice",
            "The rooms were beautiful but dirty. The AC was good and quiet, but the elevator was broken",
            "The breakfast was good, but the toilet was smelly",
            "Loved this hotel - good breakfast - nice shuttle service.",
            "I had a great unobstructed view of the Microsoft campus"
        ]

        result = text_analytics_client.analyze_sentiment(documents, show_opinion_mining=True)
        doc_result = [doc for doc in result if not doc.is_error]

        print("\n\nLet's see how many positive and negative reviews of this hotel I have right now")
        positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
        negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]
        print("...We have {} positive reviews and {} negative reviews. ".format(len(positive_reviews), len(negative_reviews)))
        print("\nLooks more positive than negative, but still pretty mixed, so I'm going to drill deeper into the opinions of individual aspects of this hotel")

        print("\nIn order to do that, I'm going to sort them based on whether these opinions are positive, mixed, or negative")
        total_mined_opinions = []
        positive_mined_opinions = []
        mixed_mined_opinions = []
        negative_mined_opinions = []

        for document in doc_result:
            for sentence in document.sentences:
                for mined_opinion in sentence.mined_opinions:
                    aspect = mined_opinion.aspect
                    total_mined_opinions.append(mined_opinion)
                    if aspect.sentiment == "positive":
                        positive_mined_opinions.append(mined_opinion)
                    elif aspect.sentiment == "mixed":
                        mixed_mined_opinions.append(mined_opinion)
                    else:
                        negative_mined_opinions.append(mined_opinion)

        def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
            if word in [mo.aspect.text for mo in positive_mined_opinions]:
                return 'rgb(0, 255, 0)'
            elif word in [mo.aspect.text for mo in mixed_mined_opinions]:
                return 'rgb(60, 60, 60)'
            return 'rgb(255, 0, 0)'


        print("\n\nNow let's make a word cloud with the positive aspects in green and negative in red to better visualize")
        aspect_text = " ".join([mo.aspect.text for mo in total_mined_opinions])
        wordcloud = WordCloud(
            width=800, height=800, background_color='white', min_font_size=10
        ).generate(aspect_text)
        plt.figure()
        plt.title("Different hotel aspects")
        plt.imshow(wordcloud.recolor(color_func=color_func), interpolation="bilinear")
        plt.axis("off")
        plt.show()

        print(
            "\n\nLooking at the breakdown, even though there were more positive opinions of this hotel, "
            "I care the most about the food and the toilets in a hotel, so I will be staying elsewhere"
        )


if __name__ == '__main__':
    sample = AnalyzeSentimentWithOpinionMiningSample()
    sample.sample_analyze_sentiment_with_opinion_mining()
