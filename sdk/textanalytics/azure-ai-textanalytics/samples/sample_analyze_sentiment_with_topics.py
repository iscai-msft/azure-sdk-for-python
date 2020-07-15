# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_sentiment_with_topics.py

DESCRIPTION:
    This sample demonstrates how to analyze sentiment at a more granular level, looking
    at the sentiment and opinions of topics.
    This feature is only available for clients with api version v3.1-preview.1.

    In this sample, we will be a customer who is trying to figure out whether they should stay
    at a specific hotel. We will be looking at which parts of the hotel are good, and which are
    not.

USAGE:
    python sample_analyze_sentiment_with_topics.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_TEXT_ANALYTICS_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_TEXT_ANALYTICS_KEY - your Text Analytics subscription key
"""

import os


class AspectBasedSentimentAnalysisSample(object):
    def aspect_based_sentiment_analysis(self):
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.textanalytics import TextAnalyticsClient, ApiVersion

        endpoint = os.environ["AZURE_TEXT_ANALYTICS_ENDPOINT"]
        key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]

        text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
            api_version=ApiVersion.V3_1_preview_1
        )

        # In this sample we will be combing through the reviews of a potential hotel to stay at: Hotel Foo.

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

        result = text_analytics_client.analyze_sentiment(documents, show_topics=True)
        doc_result = [doc for doc in result if not doc.is_error]

        print("\n\nLet's see how many positive and negative reviews of this hotel I have right now")
        positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
        negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]
        print("...We have {} positive reviews and {} negative reviews. ".format(len(positive_reviews), len(negative_reviews)))
        print("\nLooks more positive than negative, but still pretty mixed, so I'm going to drill deeper into the individual topics of each review")

        print("\nIn order to do that, I'm going to sort them based on whether people have positive, mixed, or negative feelings about these topics")
        positive_topics = []
        mixed_topics = []
        negative_topics = []

        for document in doc_result:
            for sentence in document.sentences:
                for topic in sentence.topics:
                    if topic.sentiment == "positive":
                        positive_topics.append(topic)
                    elif topic.sentiment == "mixed":
                        mixed_topics.append(topic)
                    else:
                        negative_topics.append(topic)

        print("\n\nLet's look at the {} positive topics of this hotel".format(len(positive_topics)))
        for topic in positive_topics:
            print("...Reviewers have the following opinions for the overall positive '{}' feature of the hotel".format(topic.text))
            for opinion in topic.opinions:
                print("......'{}' opinion '{}'".format(opinion.sentiment, opinion.text))

        print("\n\nNow let's look at the {} topics with mixed sentiment".format(len(mixed_topics)))
        for topic in mixed_topics:
            print("...Reviewers have the following opinions for the overall mixed '{}' quality of the hotel".format(topic.text))
            for opinion in topic.opinions:
                print("......'{}' opinion '{}'".format(opinion.sentiment, opinion.text))

        print("\n\nFinally, let's see the {} negative topics of this hotel".format(len(negative_topics)))
        for topic in negative_topics:
            print("...Reviewers have the following opinions for the overall negative '{}' topic of the hotel".format(topic.text))
            for opinion in topic.opinions:
                print("......'{}' opinion '{}'".format(opinion.sentiment, opinion.text))

        print(
            "\n\nLooking at the breakdown, even though there were more positively reviewed topics of this hotel, "
            "I care the most about the food and the toilets in a hotel, so I will be staying elsewhere"
        )


if __name__ == '__main__':
    sample = AspectBasedSentimentAnalysisSample()
    sample.aspect_based_sentiment_analysis()
