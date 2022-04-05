import numpy as np
import streamlit as st
from PIL import Image
import os
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io

st.set_page_config(page_title='InNews: A Summarised News Portal',
                   # page_icon='icon.ico'
                   )

def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list

def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((707, 400), )
        st.image(image, use_column_width=False)
    except:
        image = Image.open('./Meta/no_image.jpg')
        image = image.resize((707, 400), )
        st.image(image, use_column_width=False)


def display_news(list_of_news,news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except:
            pass
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h5 style='text-align: center; text-justify: inter-word;'>{}"</h5>'''.format(news_data.text),
                unsafe_allow_html=True)
            # st.markdown(news_data.text)
        st.success(news.pubDate.text)
        if c >= news_quantity:
            break
def run():
    st.title("InNews: A Summarised News Portal")
    image = Image.open('./Meta/newspaper.png')


    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")
    category = ['--Select--', 'Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)
    if cat_op == category[0]:
        st.warning('Please select Type!!')
    elif cat_op == category[1]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
        news_list = fetch_top_news()
        display_news(news_list,no_of_news)
    elif cat_op == category[2]:
        av_topics = ['Choose Topic','WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic",av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            st.subheader("✅ Here are the some {} News for you".format(chosen_topic))
            news_list = fetch_category_news(chosen_topic)
            display_news(news_list, no_of_news)

    elif cat_op == category[3]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)
        st.subheader("✅ Here are the some {} News for you".format(user_topic))
        if st.button("Search"):
            user_topic = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic)
            display_news(news_list,no_of_news)

run()