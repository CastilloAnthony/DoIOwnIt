from flask import Flask, render_template, request, redirect, url_for
import bcrypt
import uuid
import time
import webbrowser
from processManager import ProcessManager
from serviceLib import checkSteam, checkEpic, checkBattleNet, checkGog, checkEa, checkUplay

class Interface():
    def __init__(self):
        self.__interface = Flask(__name__, template_folder='./templates', static_folder='./static')
        self.__interface.secret_key = str(uuid.uuid4())
        self._configure_routes()
        self.__processManager = ProcessManager()
        self.__accounts = {'steam':None, 'epic':None, 'battleNet':None, 'gog':None, 'ea':None, 'uplay':None}
        self.__games = {'steam':None, 'epic':None, 'battleNet':None, 'gog':None, 'ea':None, 'uplay':None}
        webbrowser.open("http://127.0.0.1:7777/home")

    def __del__(self):
        del self.__interface, self.__processManager

    def run(self):
        self.__interface.run(host="0.0.0.0", port=7777)

    def _configure_routes(self):
        rulesList = [
            {'route':'/home', 'page':'home', 'function':self.home, 'methods':None},
            {'route':'/about', 'page':'about', 'function':self.about, 'methods':None},
            {'route':'/help', 'page':'help', 'function':self.help, 'methods':None},
            
            {'route':'/games', 'page':'games', 'function':self.games, 'methods':None},
            {'route':'/games/search', 'page':'search', 'function':self.search, 'methods':None},
            {'route':'/games/listGames', 'page':'listGames', 'function':self.listGames, 'methods':None},
            {'route':'/games/reload', 'page':'reload', 'function':self.reload, 'methods':None},

            {'route':'/services', 'page':'services', 'function':self.services, 'methods':None},
            {'route':'/services/steam', 'page':'steam', 'function':self.steam, 'methods':None},
            {'route':'/services/steam/newSteam', 'page':'newSteam', 'function':self.newSteam, 'methods':['POST']},
            {'route':'/services/epic', 'page':'epic', 'function':self.epic, 'methods':None},
            {'route':'/services/steam/newEpic', 'page':'newEpic', 'function':self.newEpic, 'methods':['POST']},
            {'route':'/services/battleNet', 'page':'battleNet', 'function':self.battleNet, 'methods':None},
            {'route':'/services/steam/newBattleNet', 'page':'newBattleNet', 'function':self.newBattleNet, 'methods':['POST']},
            {'route':'/services/gog', 'page':'gog', 'function':self.gog, 'methods':None},
            {'route':'/services/steam/newGog', 'page':'newGog', 'function':self.newGog, 'methods':['POST']},
            {'route':'/services/ea', 'page':'ea', 'function':self.ea, 'methods':None},
            {'route':'/services/steam/newEa', 'page':'newEa', 'function':self.newEa, 'methods':['POST']},
            {'route':'/services/uplay', 'page':'uplay', 'function':self.uplay, 'methods':None},
            {'route':'/services/steam/newUplay', 'page':'newUplay', 'function':self.newUplay, 'methods':['POST']},
            {'route':'/services/xboxLive', 'page':'xboxLive', 'function':self.xboxLive, 'methods':None},
            {'route':'/services/steam/newXboxLive', 'page':'newXboxLive', 'function':self.newXboxLive, 'methods':['POST']},
            {'route':'/services/playstation', 'page':'playstation', 'function':self.playstation, 'methods':None},
            {'route':'/services/steam/newPlaystation', 'page':'newPlaystation', 'function':self.newPlaystation, 'methods':['POST']},
            {'route':'/services/nintendo', 'page':'nintendo', 'function':self.nintendo, 'methods':None},
            {'route':'/services/steam/newNintendo', 'page':'newNintendo', 'function':self.newNintendo, 'methods':['POST']},
            ]
        for i in rulesList:
            self.__interface.add_url_rule(i['route'], i['page'], i['function'], methods=i['methods'])
        del rulesList

    def home(self):
        return render_template('home.html', timestamp=time.ctime())
    
    def about(self):
        return render_template('about.html')
    
    def help(self):
        return render_template('help.html')
    
    # Games
    def games(self):
        return render_template('games.html')

    def search(self):
        return render_template('search.html')
    
    def listGames(self):
        return render_template('listGames.html', list=self.__games)
    
    def reload(self):
        return render_template('reload.html')
    
    # Services
    def services(self):
        return render_template('services.html')
    
    def steam(self):
        return render_template('steam.html')
    
    def newSteam(self):
        self.__accounts['steam'] = str(request.form['userID'])
        self.__games['steam'] = checkSteam(self.__accounts['steam'])
        print(self.__games['steam'])
        return redirect(url_for('steam'))
    
    def epic(self):
        return render_template('epic.html')
    
    def newEpic(self):
        return redirect(url_for('epic'))
    
    def battleNet(self):
        return render_template('battleNet.html')
    
    def newBattleNet(self):
        return redirect(url_for('battleNet'))
    
    def gog(self):
        return render_template('gog.html')
    
    def newGog(self):
        return redirect(url_for('gog'))
    
    def ea(self):
        return render_template('ea.html')
    
    def newEa(self):
        return redirect(url_for('ea'))
    
    def uplay(self):
        return render_template('uplay.html')
    
    def newUplay(self):
        return redirect(url_for('uplay'))
    
    def xboxLive(self):
        return render_template('xboxLive.html')
    
    def newXboxLive(self):
        return redirect(url_for('xboxLive'))
    
    def playstation(self):
        return render_template('playstation.html')
    
    def newPlaystation(self):
        return redirect(url_for('playstation'))
    
    def nintendo(self):
        return render_template('nintendo.html')
    
    def newNintendo(self):
        return redirect(url_for('nintendo'))
# end Interface
    
if __name__ == '__main__':
    newFlask = Interface()
    newFlask.run()