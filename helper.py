from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df= df[df['user']==selected_user]
    #1.fetch number of messages
    num_messages=df.shape[0]
    #2 Fetch the Total Number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    #fetch number of media messages
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]


    #fetch no of links share in a media
    extractor=URLExtract()

    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    links

    return num_messages,len(words),num_media_messages,len(links)


def most_busy_user(df):
    x=df['user'].value_counts().head()
    if 'group_notification' in x.index:
        x = x.drop('group_notification')
    
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
    columns={'user':'name','count':'percent'}
    )
    df=df[df['name']!='group_notification']
    
    return x,df


def create_wordcloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df= df[df['user']==selected_user]
    temp=df[df['message']!='<Media omitted>\n']
    
    def remove_stopwords(message):
        return " ".join(
            word for word in message.lower().split() if word not in stop_words
            )
    temp = temp.copy()
    temp['message']=temp['message'].apply(remove_stopwords)
    wc=WordCloud(width=400,height=400,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    if selected_user!='Overall':
        df= df[df['user']==selected_user]
    df=df[df['message']!='<Media omitted>\n']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    stop_words=set(stop_words)
    words=[]
    df=df[df['message']!='<Media omitted>\n']
    words = [
    word 
    for message in df['message'] 
    for word in message.lower().split() 
    if word not in stop_words]
    most_common_df= pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
    

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df= df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':    
        df= df[df['user']==selected_user]
    # df['month_num']=df['date'].dt.month
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i])+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline
    
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


