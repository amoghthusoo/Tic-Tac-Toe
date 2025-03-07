# Tic Tac Toe App

A simple multiplayer Tic Tac Toe game built with KivyMD for the UI and a backend hosted on PythonAnywhere. This app allows two players to play Tic Tac Toe against each other, with one player being "X" and the other being "O".

## Features

- Multiplayer functionality with synchronization via a backend server.
- Simple and intuitive UI built with KivyMD.
- Dialogs for game results (Win, Lose, Draw).
- Reset and refresh functionality to start new games.
- Windows-specific window sizing for better UI experience.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/repository-name.git
   ```

2. Install the required dependencies:
   ```sh
   pip install kivy kivymd requests
   ```

3. Run the application:
   ```sh
   python main.py
   ```

## Usage

- The game window will open with a 3x3 grid for the Tic Tac Toe board.
- Players take turns to play by clicking on the grid cells.
- The game will automatically synchronize the moves with the backend server.
- A dialog will appear to show the game result (Win, Lose, Draw) and provide options to start a new game or go back.

## Backend

The backend code for this app is hosted in the `Login-System` repository. Ensure that the backend server is running and accessible for the app to work correctly.

### Backend Repository

- [Login-System Repository](https://github.com/yourusername/Login-System)

## Configuration

- The app is configured to run in Windows mode with specific window sizing. You can adjust the window size and position in the code if needed.
- The backend host URL is set in the `self.host` variable. Make sure to update it if your backend server URL changes.

## Troubleshooting

- If the app is not connecting to the backend, ensure that the backend server is running and the URL is correct.
- Check for any network issues that might be preventing the app from communicating with the backend.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/amoghthusoo/Tic-Tac-Toe/blob/master/LICENSE.txt) file for details.

## Acknowledgements

- KivyMD for the UI components.
- PythonAnywhere for hosting the backend server.

Feel free to contribute to this project by submitting issues or pull requests. Happy gaming!