# Huffman coding project
The well-known method for lossless compression of texts as an exercise for Python.

## Expected file structure of the project
```
huffman_coding/
    ├── README.md
    ├── requirements.txt
    ├── io_helpers.py
    ├── setup.py
    ├── huffman/                # Hauptmodul 
    │       ├── __init__.py 
    │       ├── tree.py         # Aufbau des Huffman-Baums 
    │       ├── encoder.py      # Kodierung von Texten 
    │       ├── decoder.py      # Dekodierung von Bitfolgen 
    │       └── utils.py        # Hilfsfunktionen (z. B. Frequenzanalyse)
    ├── data/                   # Beispieltexte oder Eingabedateien
    │       └── sample_input.txt
    ├── tests/                  # Unit-Tests
    │       ├── init.py
    │       └── test_encoder.py
    ├── scripts/                # Ausführbare Skripte
    │       └── run_huffman.py
    └── docs/                   # Dokumentation
            └── usage.md
```
