import sys 
from google.cloud import storage


def get_blobs(bucket_name,prefix,delimiter=None):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)
    return blobs
#convert the byte size to actual size for readability
def convert_size(size_bytes):
    """Converts bytes into a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
#get the top level directories of a given prefix 
def get_top_folders(bucket_name,prefix):
    blobs = get_blobs(bucket_name,prefix=prefix,delimiter="/")
    for blob in blobs:
        blob.name # required to go through the blobs to load all the prefixes as its an iterator object
    return list(blobs.prefixes)
#for each prefix passed return the total size in bytes and the total number of files, also iterates through the subfolders
def get_folder_size(bucket_name,prefix):
    blobs = get_blobs(bucket_name,prefix=prefix,delimiter=None)
    total_size = 0
    total_blobs = 0 
    for blob in blobs:
        total_size += blob.size
        total_blobs += 1
    return total_size,  total_blobs #return both size and count but only interested in size for now 

#main entry function, calls helpers and outputs the results
if __name__=="__main__":
    path = sys.argv[1] #entry point via specification of bucket like so: python get_size.py gs://BUCKET/PREFIX/
    path = path.replace("gs://","") #in case this format is passed 
    print(path)
    path = path.strip("/") # standarise the format
    bucket = path.split("/")[0]

    path = "/".join(path.split("/")[1:])+"/"
    print(f"Bucket: {bucket}, Path: {path}")
    
    folders = get_top_folders(bucket,path)
    print(f"Found Folders: {folders}")
    all_sizes = {}
    
    for folder in folders:
        print(f"Collecting sizes for folder: {folder}")
        folder_size, folder_blobs = get_folder_size(bucket,folder)
        all_sizes[folder] = convert_size(folder_size)
    
    #output results
    with open(f"{path.rstrip('/')}.size","w") as f:
        for folder, size in all_sizes.items():
            f.write(f"{folder} {size}\n")
