
# autoscholar
A computer program that automatically read scientific papers for you

## Dependencies

autoscholar requires python 2.7 and the following python packages:

- PyPDF2
- sqlite3
- pandas (0.16 or later)
- pdftotext (sudo apt-get install poppler-utils)
- numpy
- BeautifulSoup4

## setup

### install `menotexport`

For the installation of menotexport https://github.com/Xunius/Menotexport

### replace files to `MenoTexport` folder

Copy files `extract.py` and `word_count.py`  into folder `Menotexport-master` 

Copy files `lib/exportannotation.py lib/exportpdf.py lib/get_highlighted_text.py lib/menotexport.py` into `Menotexport-master/lib/`
and replace with its original files

## usage

### to extract highlighted text

python extract.py db_file output_file 

(e.g. `python extract.py /path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlighted_text.csv`)

### to count the word frequency

python word_count.py highlight_text_file output_file

(e.g. `python word_count.py highlighted_text.csv word_count.csv`)
