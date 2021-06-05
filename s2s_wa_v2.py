# import all necessary libraries
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip
from pydub import AudioSegment, silence
import speech_recognition as sr
import pafy as pf
import os
import shutil

# define all functions required for function of main program
def check_existing_user_requests():
    '''
    This function will check for previous user requests and create a directory
    to store the relavant outputs from the running of the main program for each
    respective user.
    '''

    # initialise directory name
    directory = 'user_request'

    # initialise index and list of user_requests
    index = 0
    user_req_num = []

    # check for previous user requests
    for filename in os.listdir():
        # if previous user_requests exist, add the # of the user_request to list
        if filename.startswith('user_request'):

            index += 1

            if int(filename[-1]) >= 1:
                user_req_num.append(int(filename[-1]))

    # if no user requests were found, then create default user_request1
    if index == 0:
        directory = directory + str(1)
        os.mkdir(directory)
        return directory
    # else, create user_request correlated to the user
    else:
        directory = directory + str(max(user_req_num)+1)
        os.mkdir(directory)
        return directory

def download_YT_video(url, video_name, directory_name):
    
    '''
    This function will return a YT video in mp4 format to a bucket in the Google Cloud Storage.
    This function requires a url from the user and a filename for the saved file.
    '''

    
    # create pafy object 
    video = pf.new(url)

    # check if video is longer than 10 minutes
    if int(video.length) >= 600:
        raise Exception("Video is too long!")
    else:
        # gets best video stream of mp4 format
        best = video.getbest(preftype="mp4")

        # create new video name by adding .mp4 extension
        video_file_name = video_name + ".mp4"

        # create path
        path = directory_name + "/" + video_file_name

        # downloads video into local directory
        best.download(filepath=path, quiet=False)

        # return filename
        return video_file_name
    
def get_wav(dir, video_file_name):
    
    '''
    Takes an mp4 file and converts into a .wav file that can be transcribed.
    The .wav file has the name enter
    '''
    
    # change to user_request directory 
    os.chdir(dir)

    # create an AudioFileClip instance of mp4 file downloaded
    audioclip = AudioFileClip(video_file_name)

    # define name to export wav file as
    filename_wav =  "audio.wav"

    # export mp3 file to specified location
    audioclip.write_audiofile(filename_wav)

    return filename_wav

def create_subclips(wav_file):
    '''
    Takes an audiofile and splits it into 10 seconds intervals,
    and then returns a dictionary with the 10 second audiofiles.
    1st 10 seconds has key subclip1, 2nd has key subclip2 and so on.
    Also saves the subclips as .wav files
    '''

    # create AudioFileClip instance from wav file
    audio = AudioFileClip(wav_file)

    # find length of AudioFileClio instance
    length = audio.duration

    # find number of subclips to create
    turns = int(length / 10) + 1

    # create subclip dictionary
    clips = {}

    # intialise index
    i = 1

    # create subclips
    while i <= turns:

        if i < turns:

            beginning = (i-1)*10
            end = i*10

            clips['subclip' + str(i)] = (audio.subclip(beginning, end))

        if i == turns:

            beginning = (i-1)*10
            end = length

            clips['subclip' + str(i)] = (audio.subclip(beginning, end))


        i = i + 1

    for subclips in clips:

        clips[subclips].write_audiofile(subclips + '.wav')

    return clips

def main(url):

    try:
        # check if any user requests already exist
        dir_name = check_existing_user_requests()

        # pre-define length of clips that will be translated
        videolength = 10

        # name that the video will have when saved on your computer
        video_name = 'video_file'

        # download YT video and return file name
        video_file_name = download_YT_video(url, video_name, dir_name)

        # retrieve wav file
        wav_file = get_wav(dir_name, video_file_name)

        # create subclips
        create_subclips(wav_file)

        # return to original directory and remove user_request to save memory
        os.chdir("..") 
        shutil.rmtree(dir_name)
        
        return True
    
    except:
        # if video duration exceeds 10 minutes, then remove user_request directory and return error
        shutil.rmtree(dir_name)
        return False