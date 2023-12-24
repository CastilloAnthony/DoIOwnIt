import socket
import requests
#import uuid
#import OidcRP
#from oidcrp import RP

def checkSteam(id):#username, id):
    # API Info: https://developer.valvesoftware.com/wiki/Steam_Web_API#Community_pages_parameters
    '''
    rp = RP(client_id=str(uuid.uuid4()),
        client_secret=str(uuid.uuid4()),
        redirect_uris=['https://steamcommunity.com/openid/id/'],
        issuer='https://steamcommunity.com/openid/')
    
    url2 = 'https://steamcommunity.com/openid/id/'+username
    url3 = 'https://store.steampowered.com/account/' # Shows their steamId once logged in.
    '''
    print('Steam ID: '+str(id))
    apiKey = 'DE1229F7804C02713461020BBC2AAE67'
    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+apiKey+'&steamid='+id+'&include_appinfo=True'+'&format=json'
    response = requests.get(url)
    response.json()
    listOfGames = []
    for i in response.json()['response']['games']:
        listOfGames.append(i['name'])
    listOfGames.sort()
    return listOfGames

def checkEpic(username):
    print('Epic is not Supported.\n'+username)

def checkBattleNet(username):
    pass

def checkGog(username):
    pass

def checkEa(username):
    pass

def checkUplay(username):
    pass

def checkXboxLive(username):
    pass

def checkPlaystation(username):
    apiKey= {"npsso":"6aAFJd53dTJLVmtUXmwsOjgQYpiQZM1OfWk7L8O8CQ1XfAEOwcZVntp3gYbdkvCy"}

def checkNintendo(username):
    pass