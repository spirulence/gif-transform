from bottle import route, run, template, response, request
import requests
import queue
from wand.image import Image
import os


key = os.environ["GIPHY_API_KEY"]
endpoint = 'https://api.giphy.com/v1/gifs/random'
gif_endpoint = 'https://i.giphy.com'
gif_id_endpoint = 'https://api.giphy.com/v1/gifs'

#TODO Transform Image

@route('/gif')
def gif():
    print('Entry')
    # Query Paramters
    tag = request.query.tag or ''
    frame = request.query.frame
    r_gif_id = request.query.id or ''
    
    response.content_type = 'image/gif'
    
    # Sets Gif ID Based on Parameters
    ini_response = None
    if not r_gif_id:
        print('Getting GIF Random ID')
        gif_id = getRandomGifId(key, tag)
    else:
        print('Setting GIF ID')
        gif_id = r_gif_id

    # Gets Raw Gif
    print('Genreating URL')
    with requests.get(generateGifURL(gif_id), stream=True) as gif_response:
        
        raw_content = gif_response.raw.read()
        
        print('GIF Recieved')
        with Image(blob=raw_content) as image:
            image.coalesce()
            print('GIF Parsed')
            if frame:
                print('Returning Frame')
                return getImageFrame(image.sequence, int(frame))
            else:
                print('Returning Image')
                return raw_content


def getRandomGifId(key:str, tag:str) -> object:
    r = requests.get(endpoint, {'api_key' : key, 'tag' : tag})
    gid = r.json()['data']['id']
    return gid


def generateGifURL(gif_id):
    gif = requests.get(f'https://api.giphy.com/v1/gifs/{gif_id}', {'api_key': key, 'gif_id' : gif_id})
    return gif.json()['data']['images']['downsized']['url']


def getImageFrame(image_sequence, frame:int) -> object:
    if frame > (length := len(image_sequence) - 1):
        frame = length
    elif frame < 0:
        frame = 0
    
    i = Image(image=image_sequence[frame])
    i_formatted = i.make_blob()
    return i_formatted


run(host='0.0.0.0', port=8080, debug=True)