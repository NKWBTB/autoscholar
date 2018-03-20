# autoscholar
A computer program that automatically read scientific papers for you

## Dependencies

autoscholar requires python 2.7 and the following python packages:

- `PyPDF2`
- `sqlite3`
- `pandas (0.16 or later)`
- `pdftotext` (sudo apt-get install poppler-utils)
- `numpy`
- `BeautifulSoup4`

## Setup

### Install menotexport

First, you need to get menotexport installed. 

For the installation of menotexport please follow this link: https://github.com/Xunius/Menotexport

### Copy the following files into `Menotexport` folder and replace with the original files

- `extract.py`
- `word_count.py` 

### Copy the folowing files from `autoscholar/lib` into the sub folder `Menotexport/lib` and replace with the original files

- `exportannotation.py` 
- `exportpdf.py` 
- `get_highlighted_text.py` 
- `menotexport.py` 

## Usage

- `python extract.py` `db_file` `output_file`
  
  Extract highlighted text from the sqlite database into `ouput_files`
  
  (e.g. `python extract.py /path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlighted_text.csv`)

### To count the word frequency

- `python word_count.py` `highlight_text_file` `output_file`

  Compute the frequencies of the words in extracted highlighted text and store the result into `output_files`

(e.g. `python word_count.py highlighted_text.csv word_count.csv`)
