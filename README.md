# pdf-grade-analyzer
PDF Grade Analyzer is a Python application designed to read and analyze grade tables from PDF files. It can calculate averages, determine letter grades, and provide various statistics from single or multi column grade layouts.

### Features
**-** Extract grades from PDF files

**-** Supports multi column PDF layouts

**-** Calculates averages, letter grade ranges, and other statistics

**-** Simple and fast to use

**-** Modular structure for easy customization and extension

### INSTALLATION
**1.** Clone the repository
```bash
git clone https://github.com/husnabosun/pdf-grade-analyzer.git
cd pdf-grade-analyzer
```

**2.** Install dependencies from requirements.txt
```bash
pip install -r requirements.txt
```

### USAGE
**1.** Instead of given pdf in the repo , add your own pdf file. Change the line 126 in husna.py.
```bash
doc = pymupdf.open("grades_multiple_col.pdf")
```
For cleaner results, please provide files which has similar structures as grades_multiple_col.pdf.

**2.** Run the main script. The program will analyze the provided PDF file and output the results to the terminal by using given inputs.<br><br>


_Shout out to all the driven girls ready to make their academic comeback 🤩 this one is for you_


