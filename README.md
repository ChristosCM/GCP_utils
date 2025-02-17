# GCP_utils
Helpful utilities for interacting with the Google Cloud Platform.


## get_size_gcp_blob
Recursive human readable storage size information for each top level "directory" of a GCP path. 
### Example Usage
```bash
python get_size_gcp_blob.py gs://BUCKET/OPTIONAL_PATH/
```
Creates OPTIONAL_PATH.size file 