from urllib import request, error, parse
import json
import base64

api_key = "8F-8k528Tpamx2MNHLdEKjNwZPTb5Nwv"
api_secret = "06vDuR4Cma7_wu4ujH8YzPRy47IihQb5"

def Detect(path):
    face_token = ''
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    img = open(path, 'rb')
    image_base64 = base64.b64encode(img.read())
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'image_base64': image_base64
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        face_token = ret["faces"][0]["face_token"]
        print(face_token)
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))
    return face_token

def DetectBase(img):
    face_token = ''
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'image_base64': img
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        face_token = ret["faces"][0]["face_token"]
        print(face_token)
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))
    return face_token


def Createset(name):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': name,
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        print(ret)
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))

def Deleteset(name):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/delete'
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': name,
        'check_empty':0
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        print(ret)
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))

def AddFace(outer_id, face_tokens):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': outer_id,
        'face_tokens': face_tokens
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        print(ret)
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))


def SeachFace(outer_id, face_token):
    face_token2 = ''
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    values = {
        'api_key': api_key,
        'api_secret': api_secret,
        'outer_id': outer_id,
        'face_token': face_token
    }
    data = parse.urlencode(values).encode('utf-8')
    req = request.Request(http_url)
    try:
        resp = request.urlopen(req, data=data, timeout=5)
        qrcont = resp.read()
        ret = json.loads(qrcont.decode('utf-8'))
        print(ret)
        face_token2 = ret['results'][0]['face_token']
    except error.HTTPError as e:
        print(e.read().decode('utf-8'))
    return face_token2


if __name__ == '__main__':
    #Deleteset('Student')
    Createset('Student')