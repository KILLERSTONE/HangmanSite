from flask import Flask, request, jsonify,render_template
from hangman import getRandomWords

app=Flask(__name__)

def initGame():
    word = getRandomWords("wordbank.csv").strip()
    wordLen = len(word)
    found = ['_']*wordLen

    return {
        "word": word,
        "found_till_now": found,
        "attempts_left": wordLen,
        "game_over": False
    }


gameStarted = None

@app.route('/hangman')
def index():
    return render_template('hangman.html')

@app.route('/hangman/new', methods=['POST'])
def newGame():
    global gameStarted
    gameStarted = initGame()

    if gameStarted:
        # Successful start of game posted
        print(gameStarted["word"])
        return jsonify({"Message": "New game started"}), 200
    else:
        # Couldn't post the request
        return jsonify({"Message": "Couldn't start new game ERROR"}), 500


@app.route('/hangman/guess', methods=['POST'])
def guessChar():
    global gameStarted

    if gameStarted['game_over']==True:
        return jsonify({"Message": "Please start a new game"}), 200
    if not gameStarted:
        return jsonify({"Message": "No active game found"}), 400

    data = request.get_json()
    print(data)

    if not data or 'guess' not in data:
        return jsonify({"Message": "Invalid request, Check the url"}), 400

    guess = data['guess']
    word = gameStarted['word']
    found = gameStarted['found_till_now']
    attempts = gameStarted['attempts_left']

    if guess in word:
        for i, letter in enumerate(word):
            if guess == letter:
                found[i] = guess

        gameStarted['found_till_now'] = found

        if '_' not in found:
            gameStarted['game_over'] = True
            return jsonify({"Message": "Congratulations you found the word", "found_till_now: ": found}), 200

        return jsonify({"Message": "Go on", "found_till_now": ''.join(found)}), 200

    else:
        attempts -= 1
        gameStarted['attempts_left'] = attempts
        if attempts == 0:
            gameStarted['game_over'] = True
            return jsonify({"Message": "You failed to find the word", "word: ": word}), 200

        return jsonify({"Message": "Try again", "found_till_now": found, "attempts_left": attempts}), 200


@app.route('/hangman/status',methods=['GET'])
def getStatus():
    global gameStarted
    if not gameStarted:
        return jsonify({"Message": "No active game found"}), 400

    return jsonify({
        "found_till_now": gameStarted['found_till_now'],
        "attempts_left": gameStarted['attempts_left'],
        "game_over": gameStarted['game_over']
    }),200
    

if __name__=='__main__':
    app.run(debug=True)