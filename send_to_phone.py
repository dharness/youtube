import requests

url = "http://192.168.0.163/upload.json"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"files[]\"; filename=\"FINALLY Upgrading my 4 year old Gaming Rig!.mp4\"\r\nContent-Type: video/mp4\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Host': "192.168.0.163",
    # 'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

files = {'files[]': open('downloads/FINALLY Upgrading my 4 year old Gaming Rig!.mp4', 'rb')}

r = requests.post(url, files=files, headers=headers)
print(r.text)
# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)