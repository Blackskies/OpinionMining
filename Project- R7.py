import keys
import re
import tweepy
import easygui
from tweepy import OAuthHandler
from textblob import TextBlob
from Tkinter import *
import tkMessageBox
import Tkinter
import matplotlib.pyplot as plt
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(keys.consumer_key, keys.consumer_secret)
            # set access token and secret
            self.auth.set_access_token(keys.access_token, keys.access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 		
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets
		  
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    # Tweets lists
    postweet_print = []
    negtweet_print = []
    neutweet_print = []
    Results_tweets = []
   
    #Using GUI for user input and Asking User for the search topic
    guitopic = easygui.enterbox("Enter the text you want to analyse :\t",'Sentiment Analysis','e.g:@happy')
    
    #Analysis is Being done please wait statement 
    easygui.msgbox("Analysis is Being done please wait",'Wait!!!!!')
    
    # calling function to get tweets
    tweets = api.get_tweets(query = guitopic, count = 100000)
    
    try:
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    
        # percentage of positive tweets
        posi_per=(100*len(ptweets)/len(tweets))
        Results_tweets.append('Positive tweets percentage: '+ str(posi_per)+ "%")
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # picking neutral tweets
        neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        # percentage of negative tweets
        nega_per =(100*len(ntweets)/len(tweets))
        Results_tweets.append("Negative tweets percentage: " + str(nega_per)+"%")
        # percentage of neutral tweets
        a=len(ntweets)
        b=len(ptweets)
        neut_per=((100*(len(tweets)-a-b)/len(tweets)))
        Results_tweets.append("Neutral tweets percentage: "+str(neut_per)+"%")

        posno=(100*len(ptweets)/len(tweets))
        negno=(100*len(ntweets)/len(tweets))
        
        # Creating a List box for Tweets Analysis
        resulttweets = Tk()
        percentagetweets = Listbox(resulttweets)
        percentagetweets.config(width=100)

        # Adding results to the List
        i=0
        for pr in Results_tweets :
            percentagetweets.insert(i,pr)
            i=i+1
        percentagetweets.pack()
        
        # Creating GUI for Displaying the Positive Tweets
        print_postweet = Tk()
        postweets = Listbox(print_postweet)

        # Creating Scroll Bar for Results
        sb = Scrollbar(print_postweet,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=postweets.yview)
        postweets.configure(yscrollcommand=sb.set)
        
        # Creating GUI for Displaying the Neutral Tweets
        print_neutweet = Tk()
        neutweetstk = Listbox(print_neutweet)

        # Creating Scroll Bar for Results
        sb = Scrollbar(print_neutweet,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=neutweetstk.yview)
        neutweetstk.configure(yscrollcommand=sb.set)
        
        # Creating GUI for Displaying the Positive Tweets
        print_negtweet = Tk()
        negtweets = Listbox(print_negtweet)

        # Creating Scroll Bar for Results
        sb1 = Scrollbar(print_negtweet,orient=VERTICAL)
        sb1.pack(side=RIGHT,fill=Y)
        sb1.configure(command=negtweets.yview)
        negtweets.configure(yscrollcommand=sb1.set)

        # Changing the width of the Tweets Window
        postweets.config(width=200)
        negtweets.config(width=200)
        neutweetstk.config(width=200)
        
        # Setting Titles to the Windows
        print_postweet.wm_title("Positive Tweets")
        print_negtweet.wm_title("Negetive Tweets")
        print_neutweet.wm_title("Neutral Tweets")
        resulttweets.wm_title("Analysed Data Reports")

        i=0
        # Adding the Neutral Tweets to Lists in GUI
        for tweet in neutweets[:100]:
            neutweet_print.append(tweet['text'])
            neutweetstk.insert(END,tweet['text'])
            i=i+1
        neutweetstk.pack()
            
        i=0
        # Adding the Positive Tweets to Lists in GUI
        for tweet in ptweets[:100]:
            postweet_print.append(tweet['text'])
            postweets.insert(END,tweet['text'])
            i=i+1
        postweets.pack()
        
        j=0
        # Adding the Negetive Tweets to Lists in GUI
        for tweet in ntweets[:100]:
            negtweet_print.append(tweet['text'])
            negtweets.insert(END,tweet['text'])
            j=j+1
        negtweets.pack()

        #Pie Chart Representation
        labels = 'Positive', 'Negative', 'Neutral'
        sizes = [posi_per, nega_per, neut_per]
        colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
        explode = (0, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis('equal')
        plt.show()
        
        #Ending loops of GUI
        resulttweets.mainloop()
        postweets.mainloop()
        negtweets.mainloop()
        neutweetstk.mainloop()
        
    except Exception:
        easygui.msgbox("\n No tweets found with " + guitopic + " Tag " ,'Error')
        
if __name__ == "__main__":
    # calling main function
    main()
