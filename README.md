# 🐍 Huffman coding project
The well-known method for lossless compression of texts as an exercise for Python.
## 📁 Expected file structure of the project
```
huffman_coding/
├── README.md
├──
├── io_helpers.py           # Auxiliary functions for file I/O
├── main.py                 # Huffman CLI main program
├── huffman/                # Main package
│   ├── __init__.py
│   ├── tree.py             # Building a Huffman tree
│   ├── encoder.py          # Encoding of texts
│   ├── decoder.py          # Decoding bit sequences
│   └── utils.py            # Help functions (e.g., frequency analysis)
├── data/                   # Sample texts or input files
│   └── sample_input.txt
├── tests/                  # Unittests
│   ├── __init__.py
│   └── test_encoder.py
├── scripts/                # Executable scripts
│   └── run_huffman.py
└── docs/                   # Documentation
    └── usage.md
```
## 🧰 Expected system requirements
This project requires the following environment:
- Python version 3.9 or higher (uses simplified type annotations like `list[str], dict[str, int]`, etc.)
- Operating Systems:
    - ✅ Windows (tested on Windows 10)
    - ✅ Linux (tested on Ubuntu/Debian-based systems)
    - ⚠️ macOS is likely compatible – not tested
- Optional: Virtual environment recommended (venv or poetry) for clean package management
