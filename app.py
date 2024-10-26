from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

current_player = 'X'
game_board = ['', '', '', '', '', '', '', '', '']
game_active = True


@app.route('/game')
# def index():
    # return render_template('index.html')


@app.route('/make-move', methods=['POST'])
def make_move():
    global current_player, game_board, game_active

    if not game_active:
        return jsonify({'message': 'Game over'}), 400

    data = request.get_json()
    index = data.get('index')

    if index is None or not (0 <= index < 9) or game_board[index] != '':
        return jsonify({'message': 'Invalid move'}), 400

    game_board[index] = current_player

    if check_winner():
        return jsonify({'message': f'{current_player} wins!'})

    if all(cell != '' for cell in game_board):
        game_active = False
        return jsonify({'message': 'It\'s a draw!'})

    current_player = 'O' if current_player == 'X' else 'X'
    return jsonify({'message': f'{current_player}\'s turn'})


@app.route('/reset-game', methods=['POST'])
def reset_game():
    global current_player, game_board, game_active
    current_player = 'X'
    game_board = ['', '', '', '', '', '', '', '', '']
    game_active = True
    return jsonify({'message': 'Game reset'})


def check_winner():
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    return any(all(game_board[i] == current_player for i in combo) for combo in winning_combos)


if __name__ == '__main__':
    app.run(debug=True)
