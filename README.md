# WordleBot

A Python-based Wordle solver and performance testing tool.

## Features
- **Wordle Solver**: Simulates games of Wordle and selects the optimal guesses.
- **Performance Analysis**: Tests the solver on a dataset and generates performance statistics with histograms.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/wordle-bot.git
    cd wordle-bot
    ```
3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ``` 
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the solver or tester:
    ```bash
    python src/wordle_bot.py  # Runs the Wordle Solver
    python src/test_bot.py    # Runs the performance tester
    ```
## Project Structure
```python
my_project/
├── src/                   # Source code
│   ├── wordle_bot.py      # Wordle Solver
│   └── test_bot.py        # Performance tester
├── data/                  # Input and binary data
│   ├── inputs/            # Input datasets
│   ├── bin/               # Pickled binary data
│   └── outputs/           # Generated output files
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── .gitignore             # Ignored files
```
## Outputs
Results are saved in the `data/outputs/` directory, with each run stored in a timestamped subdirectory.