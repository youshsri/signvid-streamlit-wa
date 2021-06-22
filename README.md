# Signvid App

## Introduction
Signvid is a web application that allows the user to translate a YouTube video via its URL to SSE, developed by BME Team 12 for our Design and Professional Practise 2 Group Project at Imperial College London.

The application performs this function by downloading the respective YouTube video to the local directory. The application will then retrieve the transcript of the speech present in its audio and the respective signs if present in the SSE sign database. The signs retrieved will then be superimposed on the original video and outputted to the user as a translation. 

## Installation
To run the web application locally, please follow these instructions.

Note: the program currently isn't compatible with Windows due to the differences in paths of files in MacOS and Windows.

1. Clone the repository to your PC.
2. Start a virtual environment present in the cloned repository.
3. Run the following command in Terminal to install the necessary packages: ```pip install -r requirements.txt```
4. Run the following command in Terminal to start the web application: ```streamlit run signvid.py```
5. The application should be ready for use on your PC's local port on your web browser.

## Notes
As of now, the program cannot be deployed online as a bug is encounted when trying to play the translated video. In order to rectify this, the application is currently being updated to work with the Django framework. Updates will be provided over the summer of 2021.
