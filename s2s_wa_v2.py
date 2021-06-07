# import all necessary libraries
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip
from numpy.core.fromnumeric import resize
import speech_recognition as sr
#import googlecloudstorage as gcs
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

        # get VideoFileClip instance of original video
        org_video = VideoFileClip(path)

        # change directory
        os.chdir(directory_name)

        # return filename
        return video_file_name, org_video

def get_wav(video_file_name):

    '''
    Takes an mp4 file and converts into a .wav file that can be transcribed.
    The .wav file has the name enter
    '''

    # create an AudioFileClip instance of mp4 file downloaded
    audioclip = AudioFileClip(video_file_name)

    # define name to export wav file as
    filename_wav =  "audio.wav"

    # export mp3 file to specified location
    audioclip.write_audiofile(filename_wav)

    # remove mp4 file
    os.remove(video_file_name)

    # return filename of wav file
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

    # delete wav file once subclip process is completed
    os.remove(wav_file)

    return clips

def get_transcript(subclip_dict):

    '''
    This is function uses Google's speech recognition engine to convert the audio to text.
    Takes a filename and returns a string.
    '''

    # initialise complete transcript list
    complete_transcript = []

    # define filename extension
    filename_ext = ".wav"

    # use the audio file as the audio source
    r = sr.Recognizer()

    for key in subclip_dict:

        # get respective filename of key
        filename = key + filename_ext

        # read the entire audio file
        with sr.AudioFile(filename) as source:
            audio = r.record(source)

        # apply speech recognition to get transcript as a list
        # delete subclip after speech recognition on it is complete
        try:
            complete_transcript.append(r.recognize_google(audio))
            os.remove(filename)
        # if silent (error), return None
        except:
            complete_transcript.append(None)
            os.remove(filename)

    # returns complete transcript of video
    return complete_transcript

def retrieve_file(word, directory):

    '''
    Checks if the video is in the database or not.
    '''

    # check if actual word or error
    if word != None:
        file_object = str(word) + ".mp4"

        # change directory to sse_dataset
        os.chdir(".."), os.chdir("sse_dataset")

        # check if sign exists in video database
        if file_object in os.listdir():

            # create path of sign video
            file_path = os.getcwd() + "/" + file_object

            # create VideoFileClip instance of sign video
            file_clip = VideoFileClip(file_path)

            # exit to previous directory
            os.chdir(".."), os.chdir(directory)

            # ensures each sign video is same size
            file_clip = file_clip.resize((320,240))

            return file_clip

        else:
            os.chdir(".."), os.chdir(directory)
            return False

    else:
        return False

def get_signs(transcript, videolength, directory):

    '''
    Takes a transcript and the length of the video that is the transcript of.
    It returns a video of max that length of a signer doing those signs.
    '''

    # initialise necessary variables
    video_array = []
    sign_translations = {}
    index = 0

    # iterate through each segment transcribed in transcript
    for segment in transcript:

        # check if segment was silent or not
        if segment == None:
            continue

        # else, follow this process
        else:

            # splits sentence string into a list of word strings
            segment = segment.split(" ")

            for word in segment:
                video = retrieve_file(word, directory)

                # check if respective sign for word was downloaded
                if video != False:

                    # create filename
                    file_clip = video

                    # append file to list
                    video_array.append(file_clip)

            # initiate concatenation if video_array has more 1 file or more
            if len(video_array) >= 1:

                # retrieve first video as starting point for concatenation as VideoFileClip instance
                sign_video = video_array[0]

                # concatenation process
                for i in range(1,len(video_array)):

                    # make VideoFileClip instance of next sign video
                    addition = video_array[i]

                    # concatenation
                    sign_video = concatenate_videoclips([sign_video, addition])

                # clear video_array for next segment
                video_array.clear()
            
            # if no words are present in the sign database
            else:
                sign_video = retrieve_file("blackscreen", directory)

            # retrieve duration of sign translation
            sign_video_dur = sign_video.duration

            # if duration is longer, speed up the sign translations
            if sign_video_dur >= videolength:
                factor = sign_video_dur/videolength

                sign_video = sign_video.fx(vfx.speedx, factor)

            # if duration is shorter, keep it at same speed
            if sign_video_dur < videolength:

                blackscreen = retrieve_file("blackscreen", directory)

                blackscreen_time = 10 - sign_video_dur

                multiplier = 10 / blackscreen_time

                blackscreen = blackscreen.fx(vfx.speedx, multiplier)

                sign_video = concatenate_videoclips([sign_video, blackscreen])

            # update index for key labels of sign_translations dictionary
            index += 1

            sign_translations["video" + str(index)] = sign_video

    return sign_translations

def main(url):

    try:
        # check if any user requests already exist
        dir_name = check_existing_user_requests()

        # pre-define length of clips that will be translated
        videolength = 10

        # name that the video will have when saved on your computer
        video_name = "video_file"

        # download YT video and return file name
        video_file_name, original_vid = download_YT_video(url, video_name, dir_name)

        # retrieve wav file
        wav_file = get_wav(video_file_name)

        # create subclips
        subclip_dictionary = create_subclips(wav_file)

        # get transcript of video
        transcript = get_transcript(subclip_dictionary)

        # get sign translations from transcript
        sign_translations = get_signs(transcript, videolength, dir_name)

        # retrieve first sign translation for first segment of transcript
        sign_concat = sign_translations["video1"]

        # concatenation proces
        for key in sign_translations:

            if key != "video1":

                sign_concat = concatenate_videoclips([sign_concat, sign_translations[key]])

        # composite sign videos onto original video
        video = CompositeVideoClip([original_vid, sign_concat.set_position(("right", "bottom"))])

        # define sign_video_filename for use
        sign_video_filename = "with_signs.mp4"

        # define path for video with signs
        path = os.getcwd() + "/" + sign_video_filename

        # write composite video into directory
        video.write_videofile(sign_video_filename)

        return path, dir_name, transcript

    except:
        # if video duration exceeds 10 minutes, then remove user_request directory and return error
        shutil.rmtree(dir_name)
        return False
