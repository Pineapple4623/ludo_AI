# Ludo Mix

A Python-based implementation of the classic Ludo board game with an AI opponent and special power-up features. This enhanced version includes strategic computer players and unique gameplay mechanics like safe square bonuses.

## Features

- Support for 2-4 players
- AI opponents with strategic decision making
- Traditional Ludo rules with power-up enhancements
- Safe squares that grant extra turns
- Token capturing mechanics
- ASCII-based board visualization
- Multiple winning conditions

## Game Rules

### Basic Rules
- Each player has 4 tokens that start in their base
- Roll a die (1-6) to move tokens
- Need a 6 to move a token out of base
- Tokens move clockwise around the board
- Must reach home with an exact roll

### Special Rules and Power-ups
- Rolling a 6 grants an extra turn
- Landing on safe squares (marked with #) grants an extra turn
- Reaching home with a token grants an extra turn
- Tokens can capture opponent's tokens by landing on their square
- Safe squares protect tokens from capture

### Winning Conditions
- First player to get all tokens home wins
- Game continues until all tokens are home
- Final rankings based on completion order

## Computer AI Strategy

The computer opponents use a sophisticated decision-making algorithm with the following priorities:

1. Move tokens out of base when possible (roll of 6)
2. Complete exact moves to home
3. Move to safe squares when possible
4. Advance furthest tokens on the board
5. Make random moves as a fallback

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Pineapple4623/ludo_AI.git
cd ludo_AI
```

2. Ensure you have Python 3.x installed
3. No additional dependencies required!

## How to Play

1. Run the game:
```bash
python ludo_miz.py
```

2. Follow the setup prompts:
   - Choose number of players (2-4)
   - Select player types (Human/Computer)
   - Enter names for human players

3. Game Controls:
   - Press ENTER to roll dice
   - Enter token numbers (1-4) to move
   - Follow on-screen prompts

## Board Layout

The game uses ASCII characters to display the board:
- `#` - Safe squares
- `*` - Regular squares
- `Y1-Y4` - Yellow player tokens
- `B1-B4` - Blue player tokens
- `R1-R4` - Red player tokens
- `G1-G4` - Green player tokens

## Implementation Details

- Written in Python using standard libraries
- Modular design with separate functions for game logic
- Extensive error handling and input validation
- Clean code with detailed comments
- ASCII-based user interface
- Configurable constants for game customization

## Project Structure

```
ludo_AI/
├── README.md
├── ludo_miz.py    # Main game implementation
└── docs/          # Documentation files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Future Enhancements

- Graphical user interface
- Network multiplayer support
- Additional power-ups
- Customizable board layouts
- Statistics tracking
- Different AI difficulty levels
- Save/Load game functionality

## License

This project is open source and available under the MIT License.

## Author

[Your Name]

## Acknowledgments

- Inspired by the classic Ludo board game
- Enhanced with modern gameplay mechanics
- Special thanks to the Python community

---

Feel free to report issues or suggest improvements by creating an issue in the repository.
