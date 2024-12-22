import urllib.request

url = 'https://github.com/THUDM/GLM-4'

aimHTML = urllib.request.urlopen(url)

print(aimHTML.read())
