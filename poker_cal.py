import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import pickle

class TexasHoldemCalculator:
    def __init__(self):
        self.history = []

    def calculate_pot_odds(self, pot_size, bet_amount):
        return bet_amount / (pot_size + bet_amount)

    def calculate_outs(self, hand, board):
        suits = {'hearts': 0, 'diamonds': 0, 'clubs': 0, 'spades': 0}
        ranks = {'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'T': 0, 'J': 0, 'Q': 0, 'K': 0, 'A': 0}
        
        all_cards = hand + board
        for card in all_cards:
            ranks[card[0]] += 1
            suits[card[1]] += 1

        flush_outs = 0
        for suit in suits.values():
            if suit == 4:
                flush_outs = 9

        straight_outs = self.calculate_straight_outs(ranks)

        triple_outs = sum(1 for count in ranks.values() if count == 3) * 2

        return flush_outs + straight_outs + triple_outs

    def calculate_straight_outs(self, ranks):
        rank_keys = list(ranks.keys())
        straight_outs = 0
        
        for i in range(len(rank_keys) - 4):
            if all(ranks[rank_keys[j]] >= 1 for j in range(i, i + 4)):
                straight_outs += 4

        return straight_outs

    def calculate_win_probability(self, outs, cards_remaining):
        return outs / cards_remaining

    def calculate_ev(self, pot_size, bet_amount, win_probability):
        lose_probability = 1 - win_probability
        ev = (win_probability * pot_size) - (lose_probability * bet_amount)
        return ev

    def simulate_game(self, player_hand, opponent_range, board):
        win_count = 0
        simulation_count = 1000

        for _ in range(simulation_count):
            opponent_hand = random.choice(opponent_range)
            # 심플하게 임의의 상대 핸드를 선택하고 결과를 시뮬레이션
            if self.hand_strength(player_hand, board) > self.hand_strength(opponent_hand, board):
                win_count += 1

        return win_count / simulation_count

    def hand_strength(self, hand, board):
        # 핸드 강도 평가 함수 (단순 버전)
        return random.random()  # 임시로 랜덤한 강도를 반환

    def evaluate_hand_strength(self, hand, board):
        return self.hand_strength(hand, board)

    def save_history(self, data):
        with open('hand_history.pkl', 'wb') as f:
            pickle.dump(data, f)

    def load_history(self):
        try:
            with open('hand_history.pkl', 'rb') as f:
                self.history = pickle.load(f)
        except FileNotFoundError:
            self.history = []

def run_calculator(calculator):
    try:
        pot_size = float(entry_pot.get())
        bet_amount = float(entry_bet.get())
        player_hand = entry_hand.get().split(',')
        board = entry_board.get().split(',')
        opponent_range = entry_opponent_range.get().split(',')

        pot_odds = calculator.calculate_pot_odds(pot_size, bet_amount)
        outs = calculator.calculate_outs(player_hand, board)
        cards_remaining = 52 - len(player_hand) - len(board)
        win_probability = calculator.calculate_win_probability(outs, cards_remaining)
        ev = calculator.calculate_ev(pot_size, bet_amount, win_probability)
        sim_win_probability = calculator.simulate_game(player_hand, opponent_range, board)

        result_text.set(f"포트 오즈: {pot_odds:.2f}\n아웃 수: {outs}\n승리 확률: {win_probability * 100:.2f}%\n"
                        f"EV: {ev:.2f}\n시뮬레이션 승리 확률: {sim_win_probability * 100:.2f}%")

        calculator.history.append({
            'pot_size': pot_size,
            'bet_amount': bet_amount,
            'player_hand': player_hand,
            'board': board,
            'opponent_range': opponent_range,
            'result': result_text.get()
        })
        calculator.save_history(calculator.history)

    except ValueError:
        messagebox.showerror("입력 오류", "숫자를 올바르게 입력해주세요.")

def visualize_data(calculator):
    win_probs = [entry['result'].split('\n')[2].split(': ')[1].strip('%') for entry in calculator.history]
    win_probs = list(map(float, win_probs))
    
    plt.hist(win_probs, bins=10, color='blue', alpha=0.7)
    plt.title('승리 확률 히스토그램')
    plt.xlabel('승리 확률 (%)')
    plt.ylabel('빈도')
    plt.show()

def create_gui(calculator):
    global entry_pot, entry_bet, entry_hand, entry_board, entry_opponent_range, result_text
    
    calculator.load_history()
    
    window = tk.Tk()
    window.title("텍사스 홀덤 확률 계산기")

    tk.Label(window, text="현재 포트 크기:").grid(row=0, column=0)
    entry_pot = tk.Entry(window)
    entry_pot.grid(row=0, column=1)

    tk.Label(window, text="상대의 베팅 금액:").grid(row=1, column=0)
    entry_bet = tk.Entry(window)
    entry_bet.grid(row=1, column=1)

    tk.Label(window, text="플레이어 핸드 (예: 2H,3H):").grid(row=2, column=0)
    entry_hand = tk.Entry(window)
    entry_hand.grid(row=2, column=1)

    tk.Label(window, text="보드 카드 (예: 5H,9H,KD):").grid(row=3, column=0)
    entry_board = tk.Entry(window)
    entry_board.grid(row=3, column=1)

    tk.Label(window, text="상대 핸드 범위 (예: AH,KH,QS,JS,TD):").grid(row=4, column=0)
    entry_opponent_range = tk.Entry(window)
    entry_opponent_range.grid(row=4, column=1)

    tk.Button(window, text="계산하기", command=lambda: run_calculator(calculator)).grid(row=5, columnspan=2)

    tk.Button(window, text="시각화", command=lambda: visualize_data(calculator)).grid(row=6, columnspan=2)

    result_text = tk.StringVar()
    tk.Label(window, textvariable=result_text).grid(row=7, columnspan=2)

    window.mainloop()

if __name__ == "__main__":
    calculator = TexasHoldemCalculator()
    create_gui(calculator)
