# filename: signvid.py

# import all necessary modules
import streamlit as st
import s2s_wa_v2 as s2s
import os

# create columns to organise web app
col1,col2,col3 = st.beta_columns([3.3,1,5])

# centering of image
with col2:
    st.image("SignVidLogo.jpg", width = 150)

# color contrast with dark mode and use of font friendly towards dyslexic individuals - improves user experience
st.markdown("<h1 style='font-family:Verdana; text-align: center; color: green;'>Welcome to SignVid!</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-family:Verdana; text-align: center; color: green;'>Enter a YouTube URL and we will translate it into Sign Supported English", unsafe_allow_html=True)
index = 0

# text input for the user
URL = st.text_input("")

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
                video = s2s.main(URL)

            # error raised if video is longer than 10 minutes
            if video == 1:
                st.error('''Sorry, the video you entered is longer than 10 minutes.
                Please try a shorter video.''')
            
            # error raised if there are 10 user_request folders present or more
            elif video == 2:
                st.error('''Sorry, you've made too many requests in a single session. Please refresh the page and start a new session.''')

            # otherwise, continue with main program
            else:

                # define sign_video_filename for use
                sign_video_path = os.getcwd() + "/with_signs.mp4"

                # write composite video into directory and read its bytes to be returned
                video.write_videofile(sign_video_path)
                video_opened = open(sign_video_path, 'rb')
                video_bytes = video_opened.read()
                
                # deliver success message
                st.balloons()
                st.success("Video processed! You can view your translated video below:")

                # read translated video and open it on user screen
                st.video(video_bytes)

                # change back to original directory
                os.chdir("..")

        # exception occurs if video could not be processed or does not exist
        except:
            st.error('''Sorry, the video you entered could not be processed or does not exist.''')

# about us sidebar
about = st.sidebar.beta_expander("About us")
about.write("We are a team of students from Imperial College London who are developing this web application for our DAPP2 project!")

# contact details sidebar
contact = st.sidebar.beta_expander("Get in touch")
contact.write("If you'd like to get in touch with our team, please fill out this [form] (https://forms.gle/QakxiBo3bzo5ZuhL7).")

# feedback sidebar
feedback = st.sidebar.beta_expander("Feedback")
feedback.write("We'd love to hear your feedback on how we can improve this service! Please click [here](https://docs.google.com/forms/d/e/1FAIpQLSdeqeT-WHNezWZBbbEmB0y68ce1s4ZXmFC9CSBccFqce02O1g/viewform?usp=sf_link) to access our feedback form.")

# acknowledgements sidebar
acknowledge = st.sidebar.beta_expander("Acknowledgements")
acknowledge.write('''We'd like to thank the Pace Centre for providing such an intellectually stimulating project! 
We'd also like to thank the people at SignStation from the University of Bristol for providing sign videos necessary 
for our app's translation process!''')