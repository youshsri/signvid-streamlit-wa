import os
from google.cloud import storage

# initialise google cloud storage API
def initilise_gcs():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'googlecloudkey.json'
    storage_client = storage.Client()
    return storage_client

# main function
def main():
    initilise_gcs()

if __name__ == "__main__":
    main()