import requests
import tarfile
import shutil
import tempfile
import os


license_key = os.environ['MAXMIND_LICENSE_KEY']
edition_ids = ['GeoLite2-ASN', 'GeoLite2-Country']
suffix = 'tar.gz'

for unique_id in edition_ids:
    url = f'https://download.maxmind.com/app/geoip_download?edition_id={unique_id}&license_key={license_key}&suffix={suffix}'
    response = requests.get(url)
    response.raise_for_status()
    
    # Create a temp dir for the extracted files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the response content to a file
        filename = f'{unique_id}.{suffix}'
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        with tarfile.open(filename, 'r:gz') as tar:
            tar.extractall(temp_dir)
        
        # Copy the extracted .mmdb files to the target dir
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.mmdb'):
                    source_file = os.path.join(root, file)
                    destination_file = os.path.join('/etc/nginx/geoip', file)
                    shutil.copy(source_file, destination_file)
        
        os.remove(filename)
