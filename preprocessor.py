import re
import pandas as pd

def preprocess(data):
    # For 24 Hour Data
    pattern1=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    # For 12 Hour Data
    pattern2 = pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:AM|PM|am|pm)?\s-\s'
    messages1=re.split(pattern1,data)[1:]
    messages2=re.split(pattern2,data)[1:]
    if messages1:
        dates=re.findall(pattern1,data)
    else:
        dates=re.findall(pattern2,data)

    # Remove \u202f spaces from time stamp
    dates
    normalized_dates = [date.replace("\u202f", " ") for date in dates]
    dates=normalized_dates[:]
    
    #check which one have data
    if messages1:
        df=pd.DataFrame({'user_message':messages1,'message_date':dates})
        # convert nessage date type
        df['message_date']=pd.to_datetime(df['message_date'],format = '%m/%d/%y, %H:%M - ')
    else:
        df=pd.DataFrame({'user_message':messages2,'message_date':dates})
        # conert nessage date type
        df['message_date']=pd.to_datetime(df['message_date'],format = '%m/%d/%y, %I:%M %p - ')
    
    df.rename(columns={'message_date':'date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]: #username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    df['year']=df['date'].dt.year
    df['only_date']=df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
