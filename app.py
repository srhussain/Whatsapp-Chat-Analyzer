import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp chat analysis")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    # st.text(data)
    df=preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show Analysis w.r.t ",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1 :
            st.header("Total Message")
            st.markdown(
            f"<h1 style='color: blue;'>{num_messages}</h1>",
            unsafe_allow_html=True)

        with col2:
            st.header("Total Words")
            st.markdown(
            f"<h1 style='color: green;'>{words}</h1>",
            unsafe_allow_html=True)
        
        with col3:
            st.header("Media Shared")
            st.markdown(
            f"<h1 style='color: purple;'>{num_media_messages}</h1>",
            unsafe_allow_html=True)

        with col4:
            st.header("Links Shared")
            st.markdown(
            f"<h1 style='color: red;'>{links}</h1>",
            unsafe_allow_html=True)

        # Finding the busiest users in the group(Group Level)

        if selected_user=='Overall':
            st.title("Most Busy Users")
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)

            with col1 :
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2 :
                st.dataframe(new_df)

        # Word cloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #Most Common Words

        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most common words")
        st.pyplot(fig)
            
           
            