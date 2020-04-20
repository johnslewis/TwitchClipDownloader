# This breaks Twitch's TOS, use at your own risk.

## Uses Twitch's private api GQL, so if Twitch makes any updates, it may break. (Working as of 4/19/20) 

You need a clientID to do this (not the kraken client id, a gql clientId). For whatever reason, these are not unique. You can find one online if you snoop around other people's gql code snippets ;)

## How to use:
  **python twitchClips.py broadcaster duration limit**

  broadcaster = channel of clips you want(ex. destiny, reckful, mitchjones)
  
  duration = the time period you want the top clips from (options are ["LAST_WEEK", "LAST_DAY", "LAST_MONTH", "ALL_TIME"])
  
  limit = the number of clips you want from that time period (twitch's limit is 100)

  example = python twitchClips.py destiny LAST_WEEK 10

## Dependencies:

   python3
  
   requests (pip install requests)


Oh yeah keep the clips folder there, I should probably fix that.

## Future Updates:
  Make sure clips folder is there
  
  Merge all clips together to automate making clip highlights


I'll probably flush out this readme and make it pretty at some point. 

  


