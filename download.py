import gdown
import os

url = 'https://drive.google.com/uc?id=1p4N3XeceF38W9e6FEDs36710wd-cn5d7'
output = 'data.tar.gz'
gdown.download(url, output, quiet=False) 

os.system("tar -xzvf data.tar.gz")
