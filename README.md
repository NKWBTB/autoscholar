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

Open terminal and move to your workspace

Type `git init` followed by `git clone https://github.com/Xunius/Menotexport.git`

For more information about the installation of menotexport please follow this link: https://github.com/Xunius/Menotexport

### Update files

Open Menotexport folder and remove file `menotexport.py` 

Copy the following files into `Menotexport` folder and replace with the original files

- `extract.py`
- `word_count.py` 

Copy the folowing files from `autoscholar/lib` into the sub folder `Menotexport/lib` and replace with the original files

- `exportannotation.py` 
- `exportpdf.py` 
- `get_highlighted_text.py` 
- `menotexport.py` 

## Usage
You can use autoscholar to extract highlights from Mendeley Desktop and then computer the word frequency

To extract highlighted text from the sqlite database into `ouput_files`

- `python extract.py` `db_file` `output_file`

  (e.g. `python extract.py /path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlighted_text.csv`)

To compute the frequencies of the words in extracted highlighted text and store the result into `output_files`

- `python word_count.py` `highlight_text_file` `output_file`

  (e.g. `python word_count.py highlighted_text.csv word_count.csv`)
