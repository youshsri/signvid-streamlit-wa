# import all necessary libraries
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip
from pydub import AudioSegment, silence
import speech_recognition as sr
import pafy as pf
import os

# define all functions required for function of main program
def check_existing_user_requests():
    '''
    This function will check for previous user requests and create a directory
    to store the relavant outputs from the running of the main program for each
    respective user.
    '''

    # initialise directory name
    directory = 'user_request'

    # initialise index
    index = 1

    # check for previous user requests
    for filename in os.listdir():
        if filename.startswith('user_request'):
            index += 1

    # if no user request before, create first user_request folder
    if index == 1:
        directory = directory + str(1)
        os.mkdir(directory)
        return directory
    # else, create user_request folder corresponding to user number
    else:
        directory = directory + str(index)
        os.mkdir(directory)
        return directory

def download_YT_video(url, video_name, directory_name):
    
    '''
    This function will return a YT video in mp4 format to a bucket in the Google Cloud Storage.
    This function requires a url from the user and a filename for the saved file.
    '''

    try:
        # create pafy object 
        video = pf.new(url)

        # gets best video stream of mp4 format
        best = video.getbest(preftype='mp4')

        # create new video name by adding .mp4 extension
        video_file_path = video_name + '.mp4'

        # create path
        path = directory_name + '/' + video_file_path

        # downloads video into local directory
        best.download(filepath=path, quiet=False)

        # return filename
        return video_name, path
    except:
        raise ValueError("URL is not valid")
    
def get_wav(dir, path):
    
    '''
    Takes an mp4 file and converts into a .wav file that can be transcribed.
    The .wav file has the name enter
    '''
    
    # create an AudioFileClip instance of mp4 file downloaded
    audioclip = AudioFileClip(path)

    # define path to export mp3 file to
    path_mp3 =  os.path.abspath(dir) + "/" + "audio.mp3"

    # define path to export wav file to
    path_wav =  os.path.abspath(dir) + "/" + "audio.wav"

    # export mp3 file to specified location
    audioclip.write_audiofile(path_mp3)

    # convert mp3 to wav
    sound = AudioSegment.from_mp3(path_mp3)
    sound.export(path_wav, format="wav")

def main(url):

    # check if any user requests already exist
    dir_name = check_existing_user_requests()

    # pre-define length of clips that will be translated
    videolength = 10

    # name that the video will have when saved on your computer
    video_name = 'video_file'

    # download YT video and return file name
    video_name, path = download_YT_video(url, video_name, dir_name)

    # retrieve wav file
    try:
        get_wav(dir_name, path)

    except:
        return os.listdir(dir_name)


