import os
import boto
import json

policy_template = {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "PublicReadForGetBucketObjects",
			"Effect": "Allow",
			"Principal": "*",
			"Action": [
				"s3:GetObject"
			],
			"Resource": [
				"arn:aws:s3:::<bucket_name>/*"
			]
		}
	]
}

class s3website:
    bucket = ""
    bucket_name = ""
    def __init__(self, bucket_name, location, index_page, err_page,
                 key_id, secret_key):
        self.bucket_name = bucket_name
        conn = boto.connect_s3(key_id,secret_key)

        try:
            self.bucket = conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError as e:
            if(e.status == 404): #not found
                self.bucket = conn.create_bucket(
                    bucket_name, location=location, policy='public-read')

    def update(self, local_path, prefix):
        for path, dirs, files in os.walk(local_path):
            for file in files:
                key_path = os.path.join(path, file).replace("\\", "/").replace(local_path, prefix, 1)
                if to_upload(get_path_components(key_path)):
                    print "upload:", os.path.join(path, file),
                    key = self.bucket.new_key(key_path)
                    key.set_contents_from_filename(os.path.join(path, file))
                    print 'done'

        self.bucket.configure_website(suffix="index.html")
        self.bucket.set_policy(json.dumps(policy_template).replace("<bucket_name>",self.bucket_name))

    def clear(self, prefix):
        print "clear", prefix,
        keys = self.bucket.list()
        self.bucket.delete_keys([key.name for key in keys if key.name[:len(prefix)+1] == prefix + "/"])
        print "done"

    def get_url(self, prefix):
        return self.bucket.get_website_endpoint() + "/" + prefix

def get_path_components(path):
    tpl = os.path.split(path)
    if(tpl[0] == ""):
        return [tpl[1]]
    else:
        return get_path_components(tpl[0]) + [tpl[1]]
def to_upload(path_components):
    for s in path_components:
        if s[0] == ".":
            return False
    return True