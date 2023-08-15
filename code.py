import os
import requests
import googleapiclient.discovery
from cleantext import clean
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from textblob import TextBlob
from pytube import YouTube
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load Lottie animation JSON from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Summarize text using TextRank algorithm
def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    from sumy.summarizers.text_rank import TextRankSummarizer
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, 2)
    text_summary = ""
    for sentence in summary:
        text_summary += str(sentence)
    return text_summary

# Analyze sentiment and classify comments
def analyze_comments(comments):
    high_positive, high_negative, positive, negative, neutral = [], [], [], [], []
    
    for comment in comments:
        text = TextBlob(comment)
        subjectivity = text.sentiment.subjectivity
        polarity = text.sentiment.polarity
        
        if subjectivity == 0 or polarity == 0:
            neutral.append(comment)
        elif polarity > 0.70:
            high_positive.append(comment)
        elif polarity < -0.70:
            high_negative.append(comment)
        elif polarity <= 0.70 and polarity > 0:
            positive.append(comment)
        elif polarity >= -0.70 and polarity < 0:
            negative.append(comment)
        else:
            neutral.append(comment)
    
    return high_positive, high_negative, positive, negative, neutral

# Calculate sentiment rank
def rank_finder(comment):
    if len(comment) > 0:
        return abs(sum(comment) / len(comment))
    else:
        return None

# Main function
def main():
    st.set_page_config(page_title='Comment Analysis', layout='wide', page_icon='<a target="_blank" href="https://icons8.com/icon/84909/youtube">YouTube</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>')
    st.markdown(f"<h1 style='text-align: center; color: Tomato;'>YouTube Comment Analysis</h1>", unsafe_allow_html=True)

    # Input YouTube video URL
    video_id = st.text_input("Enter YouTube URL")
    yt = YouTube(video_id)
    index = video_id.rfind("=")
    id = video_id[index + 1:]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "YOUR_DEVELOPER_KEY"  # Replace with your actual developer key
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    
    try:
        st.set_page_config(page_title = 'Comment Analysis', 
        layout='wide',
        page_icon='<a target="_blank" href="https://icons8.com/icon/84909/youtube">YouTube</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>')
        st.markdown(f"<h1 style='text-align: center; color: Tomato;'>YouTube Comment Analysis</h1>", unsafe_allow_html=True)
        video_id = st.text_input("Enter YouTube URL")
        yt = YouTube(video_id)
        index = video_id.rfind("=")
        id = video_id[index + 1:]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "YOUR_DEVELOPER_KEY"
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
        request = youtube.commentThreads().list(
            part="id,snippet",
            maxResults=100,
            order="relevance",
            videoId= id
        )
        response = request.execute()
        authorname = []
        comments = []
        high_positive=[]
        high_negative=[]
        positive = []
        negative = []
        neutral = []
        for i in range(len(response["items"])):
            authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
            comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            df_1 = pd.DataFrame(comments, index = authorname,columns=["Comments"])
        for i in range(len(df_1)):
            text =  TextBlob(df_1.iloc[i,0])
            subjectivity = text.sentiment.subjectivity
            polarity = text.sentiment.polarity
            if subjectivity==0 or polarity==0:
                neutral.append(df_1.iloc[i,0]) 
            elif polarity>0.70:
                high_positive.append(df_1.iloc[i,0])
            elif polarity<-0.70:
                high_negative.append(df_1.iloc[i,0])
            elif polarity<=0.70 and polarity>0:
                positive.append(df_1.iloc[i,0])
            elif polarity>=-0.70 and polarity<0:
                negative.append(df_1.iloc[i,0])
            else:
                neutral.append(df_1.iloc[i,0])
        def summarize(text):
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            from sumy.summarizers.text_rank import TextRankSummarizer
            summarizer = TextRankSummarizer()
            summary = summarizer(parser.document, 2)
            text_summary = ""
            for sentence in summary:
                text_summary += str(sentence)
            return text_summary
        def rankFinder(comment):
            list_1 = []
            for ele in comment:
                t=TextBlob(ele)
                list_1.append(t.sentiment.polarity)
                if len(list_1)>0:
                    return abs(sum(list_1)/len(list_1))
                else:
                    pass
        # Rest of your code...
        pass
    
    except:
        pass

if __name__ == "__main__":
    main()
