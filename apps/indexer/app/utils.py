import os
import tarfile

import boto3


def download_artifact(endpoint_url, bucket, key, dest, tar_zip):
    s3 = boto3.client("s3", endpoint_url=endpoint_url, use_ssl=False, verify=False)

    print(f"downloading arifact {key} to {dest}")
    dirname = os.path.dirname(dest)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if not tar_zip:
        s3.download_file(bucket, key, dest)
    else:
        temp_dest = dest + ".temp"
        temp_dir = dirname + "_temp"
        os.makedirs(temp_dir, exist_ok=True)
        s3.download_file(bucket, key, temp_dest)
        with tarfile.open(temp_dest, "r:gz") as tarObj:
            tarObj.extractall(temp_dir)
        if len(os.listdir(temp_dir)) == 1:
            os.rename(os.path.join(temp_dir, os.listdir(temp_dir)[0]), dest)
        else:
            os.rename(temp_dir, dest)
        os.rmdir(temp_dir)
        os.remove(temp_dest)
