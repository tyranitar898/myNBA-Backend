from flask import Flask, request, jsonify
import os
from nba_api.stats.static import players
player_dict = players.get_players()
print(player_dict)
#init app
app = Flask("MYNBA")

@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Welcome to myNba'})

#Run Server
if __name__ == "__main__":
    app.run(debug=True)