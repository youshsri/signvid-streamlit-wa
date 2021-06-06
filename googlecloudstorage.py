import os
from google.cloud import storage

# initialise google cloud storage API
def initilise_gcs(path_json_file):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_json_file
    storage_client = storage.Client()
    return storage_client

# main function
def main():
    initilise_gcs()

if __name__ == "__main__":
    main()