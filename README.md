<div align="center">
  <h1>♠️♥️ Streamlit Blackjack 21 ♣️♦️</h1>
  
  <p>
    <b>A fully playable Blackjack (21) web application built using Pygame and Streamlit!</b>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />
    <img src="https://img.shields.io/badge/Pygame-F5ED00?style=for-the-badge&logo=pygame&logoColor=000000" alt="Pygame" />
  </p>
</div>

<br/>

> **Experience the thrill of the casino from your browser!** The game renders high-quality Pygame graphics headlessly and streams them directly to your browser for a smooth, interactive casino experience.

---

## ✨ Features

*   🃏 **Classic Rules**: Hit, Stand, Double Down, and Split functionality.
*   💰 **Dynamic Betting**: Place custom bets with a slider. Balance and bets persist across rounds.
*   🎬 **Slick Animations**: Realistic, sequential card-dealing animations slide right out of the deck.
*   📱 **Responsive UI**: Built natively into Streamlit with an intuitive, side-by-side wide layout.
*   🖥️ **Headless Engine**: Uses a virtual SDL video driver to run Pygame on any server without needing a physical display.

---

## 🛠️ Installation & Setup

Make sure you have **Python 3.8+** installed on your system.

**1. Clone the repository:**
```bash
git clone https://github.com/ImAust1n/BlackJack.git
cd BlackJack
```

**2. Create a virtual environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Game

Launch the web interface using Streamlit:

```bash
streamlit run blackjack.py
```
*The game will automatically open in your default web browser at `http://localhost:8501`.*

---

## 🎮 How to Play

### The Setup
Slide to select your bet amount and click **Deal**.

### Player Actions
| Action | Description |
| :--- | :--- |
| **Hit** 🎯 | Draw another card. |
| **Stand** 🛑 | End your turn and let the dealer play. |
| **Double Down** 💸 | Double your bet, receive exactly one more card, and stand. |
| **Split** ✌️ | If you have two cards of the exact same value, you can split them into two separate hands (requires an additional bet equal to your original bet). |

### Payouts & Rules
*   The dealer reveals their hidden card and automatically hits until they reach **17 or higher**.
*   **Normal Win:** Pays 1:1.
*   **Blackjack! (Ace + 10-value):** Pays 3:2.
*   **Push:** Ties result in your bet being returned.
*   **Bankrupt:** If you run out of chips, it's game over. You'll need to restart!

---

## 💡 Pro Tip
For the ultimate immersive experience, press **`F11`** to make your web browser completely full screen!

---

<div align="center">
  <i>Built with Pillow, Pygame, and Streamlit.</i>
</div>
