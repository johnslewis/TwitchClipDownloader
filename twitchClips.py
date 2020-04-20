import requests
import json
import sys
import os


# constants

gqlUrl = "https://gql.twitch.tv/gql"


# for whatever reason these arent unique to 1 person, grabbed from somewhere online
clientId = ""


# getVideoUrls constants

# from what i can tell, this is some sort of unique instruction for getting clip information
sha256HashClipUrl = "9bfcc0177bffc730bd5a5a89005869d2773480cf1738c592143b5173634b7d15"
versionClipUrl = 1
operationNameClipUrl = "VideoAccessToken_Clip"



# what quality wish to return
maxQuality = ""
minQuality = ""


sha256HashTopClips = "b73ad2bfaecfd30a9e6c28fada15bd97032c83ec77a0440766a56fe0bd632777"
versionTopClips = 1
operationNameTopClips = "ClipsCards__User"


limitMax = 100



durations = ["LAST_WEEK", "LAST_DAY", "LAST_MONTH", "ALL_TIME"]


def getVideoUrls(slug):
  jsonRequest = {
      "extensions": {
          "persistedQuery": {
              "sha256Hash": sha256HashClipUrl, 
              "version": versionClipUrl
          }
      }, 
      "operationName": operationNameClipUrl, 
      "variables": {
          "slug": slug
      }
  }

  response = requests.post(gqlUrl \
    , data=json.dumps(jsonRequest), headers={'Client-ID': clientId})

  if (response.status_code == 200):
    response = response.json()
    
      
    maxFoundQuality = -1
    maxFoundQualityUrl = ""
    for x in range(0,  len(response["data"]["clip"]["videoQualities"])):

      

      clipQuality = response["data"]["clip"]["videoQualities"][x]["quality"]
      

      if(clipQuality == maxQuality):
          return response["data"]["clip"]["videoQualities"][x]["sourceURL"]

      elif int(clipQuality) > int(maxFoundQuality) and int(clipQuality) < int(maxQuality) and int(clipQuality) > int(minQuality):
        maxFoundQuality = clipQuality
        maxFoundQualityUrl = response["data"]["clip"]["videoQualities"][x]["sourceURL"]


    if maxFoundQuality != -1 and maxFoundQualityUrl != "":
      print("returned max quality url")
      return maxFoundQualityUrl
  else:
    print("error, statusCode = " + response.status_code)

      
      
  return False    


def getSlugs(channel, timeFilter, limit):
  jsonRequest = {
    "operationName": operationNameTopClips,
    "variables": {
      "login": channel,
      "limit": limit,
      "criteria": {
        "filter": timeFilter
      }
    },
    "extensions": {
      "persistedQuery": {
        "version": versionTopClips,
        "sha256Hash": sha256HashTopClips
      }
    }
  }


  response = requests.post(gqlUrl \
    , data=json.dumps(jsonRequest), headers={'Client-ID': clientId})

  slugs = []
  if (response.status_code == 200):
    response = response.json()

    # print(json.dumps(response, sort_keys=True, indent=4))

    clips = response["data"]["user"]["clips"]["edges"]
    
    for i in range(0, len(clips)):
      clipSlug = clips[i]["node"]["slug"]

      

      slugs.append(clipSlug)
      
  else:
    print("reponse code = " + str(response.status_code))
    print(json.dumps(response.json(), sort_keys=True, indent=4))

   
  return slugs


def setSettings():
     

  with open('settings.json') as json_file:
    data = json.load(json_file)

    global clientId
    clientId = data["clientId"]
    global maxQuality
    maxQuality = data["maxQuality"]
    global minQuality
    minQuality = data["minQuality"]


def downloadClips(videoUrls):
  

  for videoUrl in videoUrls:

    file_name = videoUrl.split('/')[-1]    

 

    # create response object 
    r = requests.get(videoUrl, stream = True) 

    # download started 
    print(os.getcwd())
    with open(os.getcwd()+"/clips/" + file_name, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 

 




def main():

  if(len(sys.argv) == 4):
    channel = sys.argv[1]
    duration = sys.argv[2]
    limit = int(sys.argv[3])

    if limit > limitMax:
      print("limit too high")
      return

    durationFound = False
    for i in range(0, len(durations)):
      if(duration == durations[i]):
        durationFound = True
        break
    
    if durationFound == False:
      print("incorrect duration")
      return

  else:
    print("too few arguments")
    return


  setSettings()


  slugs = getSlugs(channel, duration, limit)

  
  videoUrls = []
  for i in range(0, len(slugs)):
    videoUrls.append(getVideoUrls(slugs[i]))
  
  print(videoUrls)

  downloadClips(videoUrls)


   

  

  

  

main()