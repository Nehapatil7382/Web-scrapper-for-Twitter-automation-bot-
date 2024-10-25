from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

intervalTime = 10

def analyze_sentiment(text):
    negative_keywords = ["weapon violence", "violence", "gun", "shooting", "attack"]
    
    if any(keyword in text.lower() for keyword in negative_keywords):
        return -1  

    analysis = TextBlob(text)
    return analysis.sentiment.polarity  

def twitter_login(username, password):
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="username"]'))).send_keys(username)
    
    tweet_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
    time.sleep(2)
    tweet_button.click()
    time.sleep(3)
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[autocomplete="current-password"]'))).send_keys(password)
    time.sleep(5)
    tweet_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
    tweet_button.click()
    time.sleep(20)  

def post_tweets(directory_path, json_data):
    print("Started posting tweets!")
    
    for file in json_data:
        driver.get("https://twitter.com/compose/tweet")
        wait = WebDriverWait(driver, 20)
        time.sleep(2)  

        content = file.get("content", "")
        if content:
            sentiment_score = analyze_sentiment(content)
            print(f"Tweet Content: {content}, Sentiment Score: {sentiment_score}")
            
            if sentiment_score < 0:  
                print(f"Skipping negative content: {content}")
                continue
            
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]'))).send_keys(content)
            time.sleep(10)  
            
            if "image" in file:
                image_path = os.path.join(directory_path, file["image"])
                driver.find_element(By.CSS_SELECTOR, 'input[data-testid="fileInput"]').send_keys(image_path)
                time.sleep(10)  
            
            if "video" in file:
                video_path = os.path.join(directory_path, file["video"])
                driver.find_element(By.CSS_SELECTOR, 'input[data-testid="fileInput"]').send_keys(video_path)
                time.sleep(15)  
            
            print("Posting tweet...")
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="tweetButton"]').click()
            time.sleep(10)  

            for t in range(int((intervalTime - 10) / 10)):
                time.sleep(10)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    print("Completed posting tweets!")

def visualize_sentiment(sentiment_scores, tweet_contents):
    plt.figure(figsize=(10, 6))
    plt.plot(sentiment_scores, marker='o', linestyle='-', color='b', label='Sentiment Score')
    plt.title('Sentiment Analysis of Tweets')
    plt.xlabel('Tweet Index')
    plt.ylabel('Sentiment Score')
    plt.axhline(0, color='red', linestyle='--')  # Line for neutral sentiment
    plt.fill_between(range(len(sentiment_scores)), sentiment_scores, 0, where=(np.array(sentiment_scores) > 0), color='green', alpha=0.5, label='Positive Sentiment')
    plt.fill_between(range(len(sentiment_scores)), sentiment_scores, 0, where=(np.array(sentiment_scores) < 0), color='orange', alpha=0.5, label='Negative Sentiment')
    plt.xticks(range(len(tweet_contents)), [f'Tweet {i+1}' for i in range(len(tweet_contents))], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

twitter_username = 'enter_your_username'
twitter_password = 'enter_your_password'
directory_path = os.path.abspath('./posts')

json_data = [
    {"content": "learning", "image": "1.jpg"},
    {"content": "coding", "video": "2.mp4"},
    {"content": "Weapon violence should stop", "image": "3.png"},
]

driver = webdriver.Chrome()

twitter_login(twitter_username, twitter_password)
time.sleep(5)

post_tweets(directory_path, json_data)

driver.quit()

visualize_sentiment([analyze_sentiment(tweet["content"]) for tweet in json_data], [tweet["content"] for tweet in json_data])
