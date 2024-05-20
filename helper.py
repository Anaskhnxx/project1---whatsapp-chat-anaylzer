import regex as  re 
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter
def fetch_stats(selected_user , df):
    
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    nums_msgs = df.shape[0]
    
    words =[]
    for msg in df['message']:
         words.extend(msg.split())
         
    num_media_msgs = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    
    links = []
    for msg in df['message']:
        links.extend(re.findall("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$", msg))
         
         
    
    return nums_msgs , len(words) , num_media_msgs , len(links)



def most_busy_user(df):
    x = df['users'].value_counts().head()
    df= round((df['users'].value_counts()/df.shape[0])*100 ,2).reset_index().rename(columns={'index':'name' , 'users': 'percent' })
    
    return x , df

# wordcloud
# def create_wordcloud(selected_user , df):
#     if selected_user != 'Overall':
#         df = df[df['users'] == selected_user]
    

#     wc = WordCloud(width = 500 , height=500, min_font_size = 10 , background_color='white')
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc
# wordcloud end



def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('dates').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def most_common_words(selected_user , df):
    
    f =open('stop_hinglish.txt','r' )
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
        
    temp =df[df['users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words= []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df