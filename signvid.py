import streamlit as st
import s2s_wa_v2 as s2s
import os
import shutil

# create columns to organise web app
col1,col2,col3 = st.beta_columns([3.3,1,5])

# centering of image
with col2:
    st.image("SignVidLogo.jpg", width = 150)

st.markdown("<h1 style='text-align: center; color: black;'>Welcome to SignVid!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Enter a YouTube URL and we will translate it into Sign Supported English", unsafe_allow_html=True)

URL = st.text_input("Enter a YouTube URL here...")

# check if file is local to directory or url link to YouTube
if URL:

    # check if the file is not a YouTube url
    if "youtube" not in URL:
        st.error('''Sorry, the text you entered is not a valid YouTube URL. Please try again.''')

    # check if the file is a YouTube url
    if "youtube" in URL:
        try:
            st.video(URL)

            with st.spinner("Processing video..."):
                runtime, dirname = s2s.main(URL)

            if runtime == False:
                st.error('''Sorry, the video you entered is longer than 10 minutes. 
                Please try a shorter video.''')
            else:
                st.balloons()
                st.success("Video processed! You can view your translated video below:")
                st.video(runtime)

                # return to original directory and remove user_request to save memory
                if st.button("Clear"):
                    shutil.rmtree(dirname)

        except:
            st.error('''Sorry, the text you entered is not a valid YouTube URL. Please try again.''')

about = st.sidebar.beta_expander("About us")
about.write("We are a team of students from Imperial College London who are developing this web application for our DAPP2 project!")
#Let's rewrite this
contact = st.sidebar.beta_expander("Get in touch")
contact.write("If you'd like to get in touch with our team, please contact us at: ...")
#Let's rewrite this
feedback = st.sidebar.beta_expander("Feedback")
feedback.write("We'd love to hear your feedback on how we can improve this service! Please click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ) to access our feedback form.")
