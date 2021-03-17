import gdown
import os

url = 'https://drive.google.com/uc?id=1jaNbWSjjVsm1sFjO5kKe-XnygPyDp-_X'
output = 'data.tar.gz'
gdown.download(url, output, quiet=False) 

os.system("tar -xzvf data.tar.gz")
