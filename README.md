
# autoscholar
A computer program that automatically read scientific papers for you

## dependencies

### 1. requires python2.7. NOT compatible with python3+

### 2. requires the following python packages:

    - PyPDF2
    - sqlite3
    - pandas (0.16 or later)
    - pdftotext (sudo apt-get install poppler-utils)
    - numpy
    - BeautifulSoup4

## setup

### 1. install `menotexport`

For the installation of menotexport https://github.com/Xunius/Menotexport

### 2. replace files to `MenoTexport` folder

1 Copy files `extract.py` and `word_count.py`  into folder `Menotexport-master` 

2 Copy files `lib/exportannotation.py lib/exportpdf.py lib/get_highlighted_text.py lib/menotexport.py` into `Menotexport-master/lib/`
and replace with its original files

## usage

### 1. to extract highlighted text

python extract.py db_file output_file 

(e.g. `python extract.py /path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlighted_text.csv`)

### 2 to count the word frequency

python word_count.py highlight_text_file output_file

(e.g. `python word_count.py highlighted_text.csv word_count.csv`)
