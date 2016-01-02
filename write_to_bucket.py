from apiclient import discovery
from oauth2client.client import GoogleCredentials
# Get the application default credentials. When running locally, these are
# available after running `gcloud init`. When running on compute
# engine, these are available from the environment.
credentials = GoogleCredentials.get_application_default()

# Construct the service object for interacting with the Cloud Storage API -
# the 'storage' service, at version 'v1'.
# You can browse other available api services and versions here:
#     https://developers.google.com/api-client-library/python/apis/
service = discovery.build('storage', 'v1', credentials=credentials)