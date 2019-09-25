# RecogNet
Facial recognition from free-world overhead cameras - for improved security
in South Africa.

The first implementation is a Django API that can receive an image and
a data dictionary and return a data dictionary about the recognised 
person in question (prediction endpoint).

As part of the API init, the model is loaded, ready for prediction.

The backend stores images in blob storage, which is mapped to a PostgreSQL
database (Cloud SQL).

A k-means clustering job runs in the background, updating cluster id's
per entry in the PostgreSQL database. Each cluster is formed on 
images from known identities (obtained from the web).

Further, the matching algorithm does not simply have a facial recognition 
component, but is also able to compare data dictionaries about the person
in question. This results in an overall comparison score with associated 
threshold.

A web scraper is working in the background to add users and images to
Cloud Storage and the PostgreSQL DB, through the API store endpoint.

Camera image streaming to Cloud Storage occurs in real-time.
There are two storage buckets, unprocessed and processed.
If a file is uploaded into unprocessed, a cloud function is triggered
that hits the store endpoint and then moves the file in processed.

If no connection is available, images are stored on disk.
A job runs daily to identify if there are any images on disk that need
to be uploaded to Cloud Storage.