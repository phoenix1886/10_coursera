# Coursera Dump

This script parses information about coursera courses.

## How to use
To use the script one should have python 3.5 installed. All required packages can be found in requirenments.txt. The installation from file is as simple. Just type the following command in terminal:
```
pip install -r requirenments.txt
```

The script takes 2 positional arguments:
* path - the path of file for saving results (.xlsx format)
* num - the number of courses to parse

## Example of work
```
KirillMaslov$ python 10_coursera/coursera.py './results.xlsx' 10
Requesting coursera...
parsing https://www.coursera.org/learn/hotel-management-project
parsing https://www.coursera.org/learn/crypto-info-theory
parsing https://www.coursera.org/learn/educacion-superior
parsing https://www.coursera.org/learn/astrobiology
parsing https://www.coursera.org/learn/marketing-management-two
parsing https://www.coursera.org/learn/3d-cad
parsing https://www.coursera.org/learn/big-bang
parsing https://www.coursera.org/learn/asset-measurement-disclosure
parsing https://www.coursera.org/learn/ingles-empresarial-gestion-liderazgo
parsing https://www.coursera.org/learn/advanced-trading-algorithms
Request completed. Information recorded to ./results.xlsx
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
