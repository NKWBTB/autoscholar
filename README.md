# autoscholar
A computer program that automatically read scientific papers for you

## Dependencies

autoscholar requires python 2.7

    Recommend using pip as package manager

    To insall pip, open your terminal and copy the following commands

    ~$ sudo apt-get update

    ~$ sudo apt-get install python-pip
    
    ~$ pip install --upgrade pip

The following python packages are required:
 
- `sqlite3` (included in the standard library (since Python 2.5))
 
 
- `PyPDF2`

     ~$ pip install PyPDF2
  

- `pandas (0.16 or later)`

    ~$ pip install pandas
 
- `numpy`

    ~$ pip install numpy

- `BeautifulSoup4`

    ~$ pip install beautifulsoup4

- `pdftotext` 

    ~$ sudo apt-get install poppler-utils

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
