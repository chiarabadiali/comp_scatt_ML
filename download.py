import gdown
import os

url = 'https://drive.google.com/uc?id=1FskrJdFAyPQLaFOoFSpHsX822h83q4Hu'
output = 'data.tar.gz'
gdown.download(url, output, quiet=False) 

os.system("tar -xzvf data.tar.gz")
