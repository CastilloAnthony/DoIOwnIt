from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import uuid
import time
import webbrowser
from difflib import get_close_matches
from processManager import ProcessManager
from serviceLib import checkSteam, checkEpic, checkBattleNet, checkGog, checkEa, checkUplay, checkXboxLive, checkPlaystation, checkNintendo

class Interface():
    def __init__(self):
        self.__interface = Flask(__name__, template_folder='./templates', static_folder='./static')
        self.__interface.secret_key = str(uuid.uuid4())
        self._configure_routes()
        self.__processManager = ProcessManager()
        self.__accounts = {'steam':None, 'epic':None, 'battleNet':None, 'gog':None, 'ea':None, 'uplay':None, 'xboxLive':None, 'playstation':None, 'nintendo':None,}
        self.__games = {'steam':None, 'epic':None, 'battleNet':None, 'gog':None, 'ea':None, 'uplay':None, 'xboxLive':None, 'playstation':None, 'nintendo':None,}
        self.__gameNames = []
        webbrowser.open("http://127.0.0.1:7777/")

    def __del__(self):
        del self.__interface, self.__processManager

    def run(self):
        self.__interface.run(host="0.0.0.0", port=7777)

    def _configure_routes(self):
        rulesList = [
            # Basic Routes
            {'route':'/', 'page':'home', 'function':self.home, 'methods':None},
            {'route':'/about', 'page':'about', 'function':self.about, 'methods':None},
            {'route':'/help', 'page':'help', 'function':self.help, 'methods':None},

            # Games Routes
            {'route':'/games', 'page':'games', 'function':self.games, 'methods':None},
            {'route':'/games/search', 'page':'search', 'function':self.search, 'methods':None},
            {'route':'/games/search/newSearch', 'page':'newSearch', 'function':self.newSearch, 'methods':['POST']},
            {'route':'/games/listGames', 'page':'listGames', 'function':self.listGames, 'methods':None},
            {'route':'/games/reload', 'page':'reload', 'function':self.reload, 'methods':None},

            # Services Routes
            {'route':'/services', 'page':'services', 'function':self.services, 'methods':None},
            {'route':'/services/steam', 'page':'steam', 'function':self.steam, 'methods':None},
            {'route':'/services/steam/newSteam', 'page':'newSteam', 'function':self.newSteam, 'methods':['POST']},
            {'route':'/services/epic', 'page':'epic', 'function':self.epic, 'methods':None},
            {'route':'/services/epic/newEpic', 'page':'newEpic', 'function':self.newEpic, 'methods':['POST']},
            {'route':'/services/battleNet', 'page':'battleNet', 'function':self.battleNet, 'methods':None},
            {'route':'/services/battleNet/newBattleNet', 'page':'newBattleNet', 'function':self.newBattleNet, 'methods':['POST']},
            {'route':'/services/gog', 'page':'gog', 'function':self.gog, 'methods':None},
            {'route':'/services/gog/newGog', 'page':'newGog', 'function':self.newGog, 'methods':['POST']},
            {'route':'/services/ea', 'page':'ea', 'function':self.ea, 'methods':None},
            {'route':'/services/ea/newEa', 'page':'newEa', 'function':self.newEa, 'methods':['POST']},
            {'route':'/services/uplay', 'page':'uplay', 'function':self.uplay, 'methods':None},
            {'route':'/services/uplay/newUplay', 'page':'newUplay', 'function':self.newUplay, 'methods':['POST']},
            {'route':'/services/xboxLive', 'page':'xboxLive', 'function':self.xboxLive, 'methods':None},
            {'route':'/services/xboxLive/newXboxLive', 'page':'newXboxLive', 'function':self.newXboxLive, 'methods':['POST']},
            {'route':'/services/playstation', 'page':'playstation', 'function':self.playstation, 'methods':None},
            {'route':'/services/playstation/newPlaystation', 'page':'newPlaystation', 'function':self.newPlaystation, 'methods':['POST']},
            {'route':'/services/nintendo', 'page':'nintendo', 'function':self.nintendo, 'methods':None},
            {'route':'/services/nintendo/newNintendo', 'page':'newNintendo', 'function':self.newNintendo, 'methods':['POST']},
            ]
        for i in rulesList:
            self.__interface.add_url_rule(i['route'], i['page'], i['function'], methods=i['methods'])
        del rulesList

    def home(self):
        return render_template('home.html')
    
    def about(self):
        return render_template('about.html')
    
    def help(self):
        return render_template('help.html')
    
    # Games
    def games(self):
        return render_template('games.html')

    def search(self):
        return render_template('search.html')
    
    def newSearch(self):
        searchTerm = str(request.form['game'])
        gameName, listOfGames, listOfServices = 'No results', [], []
        if (not self.__games['steam'] == None or 
            not self.__games['epic'] == None or 
            not self.__games['battleNet'] == None or 
            not self.__games['gog'] == None or 
            not self.__games['ea'] == None or 
            not self.__games['uplay'] == None or 
            not self.__games['xboxLive'] == None or 
            not self.__games['playstation'] == None or 
            not self.__games['nintendo'] == None
        ):
            games = {}
            for service in self.__games:
                if self.__games[service] != None:
                    for game in self.__games[service]:
                        if game not in self.__gameNames:
                            self.__gameNames.append(game)
                        if game not in games:
                            games[game] = [service]
                        else:
                            if service not in games[game]:
                                games[game].append(service)
            for game in games:
                if searchTerm.lower() in game.lower():
                    listOfGames.append(game)
            closeMatches = get_close_matches(searchTerm, listOfGames)
            print(listOfGames)
            print(closeMatches)
            if len(closeMatches) > 0:
                gameName = closeMatches[0]
                listOfServices = games[closeMatches[0]]
            elif len(listOfGames) > 0:
                gameName = listOfGames[0]
                listOfServices = games[listOfGames[0]]
            return render_template('newSearch.html', game=gameName, services=listOfServices)
        else:
            return redirect(url_for('services'))
    
    def listGames(self):
        if (not self.__games['steam'] == None or 
            not self.__games['epic'] == None or 
            not self.__games['battleNet'] == None or 
            not self.__games['gog'] == None or 
            not self.__games['ea'] == None or 
            not self.__games['uplay'] == None or 
            not self.__games['xboxLive'] == None or 
            not self.__games['playstation'] == None or 
            not self.__games['nintendo'] == None
        ):
            games = {}
            for service in self.__games:
                if self.__games[service] != None:
                    for game in self.__games[service]:
                        if game not in self.__gameNames:
                            self.__gameNames.append(game)
                        if game not in games:
                            games[game] = [service]
                        else:
                            if service not in games[game]:
                                games[game].append(service)
            return render_template('listGames.html', list=games)
        else:
            return redirect(url_for('games'))
    
    def reload(self):
        return render_template('reload.html')
    
    # Services
    def services(self):
        return render_template('services.html', list=self.__accounts)
    
    def steam(self):
        return render_template('steam.html')
    
    def newSteam(self):
        self.__accounts['steam'] = str(request.form['userID'])
        self.__games['steam'] = checkSteam(self.__accounts['steam'])
        #print(self.__games['steam'])
        return redirect(url_for('services'))
    
    def epic(self):
        return render_template('epic.html')
    
    def newEpic(self):
        self.__accounts['epic'] = str(request.form['userID'])
        checkEpic(self.__accounts['epic'])
        return redirect(url_for('services'))
    
    def battleNet(self):
        return render_template('battleNet.html')
    
    def newBattleNet(self):
        self.__accounts['battleNet'] = str(request.form['userID'])
        checkBattleNet(self.__accounts['battleNet'])
        return redirect(url_for('services'))
    
    def gog(self):
        return render_template('gog.html')
    
    def newGog(self):
        self.__accounts['gog'] = str(request.form['userID'])
        checkGog(self.__accounts['gog'])
        return redirect(url_for('services'))
    
    def ea(self):
        return render_template('ea.html')
    
    def newEa(self):
        self.__accounts['ea'] = str(request.form['userID'])
        checkEa(self.__accounts['ea'])
        return redirect(url_for('services'))
    
    def uplay(self):
        return render_template('uplay.html')
    
    def newUplay(self):
        self.__accounts['uplay'] = str(request.form['userID'])
        checkUplay(self.__accounts['uplay'])
        return redirect(url_for('services'))
    
    def xboxLive(self):
        return render_template('xboxLive.html')
    
    def newXboxLive(self):
        self.__accounts['xboxLive'] = str(request.form['userID'])
        checkXboxLive(self.__accounts['xboxLive'])
        return redirect(url_for('services'))
    
    def playstation(self):
        return render_template('playstation.html')
    
    def newPlaystation(self):
        self.__accounts['playstation'] = str(request.form['userID'])
        checkPlaystation(self.__accounts['playstation'])
        return redirect(url_for('services'))
    
    def nintendo(self):
        return render_template('nintendo.html')
    
    def newNintendo(self):
        self.__accounts['nintendo'] = str(request.form['userID'])
        checkNintendo(self.__accounts['nintendo'])
        return redirect(url_for('services'))
# end Interface
    
if __name__ == '__main__':
    newFlask = Interface()
    newFlask.run()