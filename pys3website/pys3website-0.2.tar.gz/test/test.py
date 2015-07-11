import json
from boto.s3.connection import Location
from pys3website import pys3website

def run():
    f = open("s3authkey.json", "r")
    auth = json.loads(f.read())
    f.close()

    mywebsite = pys3website.s3website(
        bucket_name = "richreview.edx",
        location = Location.DEFAULT,
        index_page = "index.html",
        err_page = "error.html",
        key_id = auth["access_key_id"],
        secret_key = auth["secret_access_key"]
    )

    mywebsite.clear()

    mywebsite.update(local_path = "mywebsite")

    print mywebsite.get_url(local_path = "mywebsite")

if __name__ == "__main__":
    run()