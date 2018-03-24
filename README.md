,# autoscholar
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

First, you need to download menotexport

Open terminal and move to your workspace

Type `git clone https://github.com/Xunius/Menotexport.git` to download menotexport

For more information about the installation of menotexport please follow this link: https://github.com/Xunius/Menotexport

### Install autoscholar

Second, you need to download autoscholar

Type `https://github.com/forrestbao/autoscholar.git` to download autoscholar

Then, copy the `lib` folder from `menotexport` into `autoscholar` and we are now all set 

## Usage
You can use autoscholar to extract highlights from Mendeley Desktop and then computer the word frequency

To extract highlighted text from the sqlite database into `ouput_files`

- `python extract.py` `db_file` `output_file`

  (e.g., `python extract.py /path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlighted_text.csv`)

To compute the frequencies of the words in extracted highlighted text and store the result into `output_files`

- `python word_count.py` `highlight_text_file` `output_file`

  (e.g., `python word_count.py highlighted_text.csv word_count.csv`)
