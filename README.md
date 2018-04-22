# autoscholar
A computer program that automatically reads scientific papers for you

## Dependencies

autoscholar requires python 2.7

The following python packages are required:
 
- sqlite3 (included in the standard library since Python 2.5)
- PyPDF2
- pandas (0.16 or later) 
- numpy
- BeautifulSoup4
- pdftotext
- pdfminer
- [menotexport](https://github.com/Xunius/Menotexport)

On Debian/Ubuntu distributions, you may install pdftotext, git (for pulling autoscholar and Menotexport later), and pip (recommend for installing other Python packages) as follows: 

    $ sudo apt-get install poppler-utils python-pip git

The Python packages may be installed using pip like this: 

    $ pip install PyPDF2 pandas numpy beautifulsoup4 pdfminer
    
For menoexport, simply clone it to your local directory, like this: 

    $ mkdir ~/work_dir       # create a working directory 
    $ cd ~/work_dir          # enter the working directory 
    $ git clone https://github.com/Xunius/Menotexport.git

and then add the root directory of Menotexport to your PYTHONPATH environment variable. The permanent way is to add a line into `~/.bashrc`, such as (assuming the username is forrest on Linux) 

    $ echo "export PYTHONPATH=$PYTHONPATH:/home/forrest/work_dir/Menotexport" >> ~/.bashrc

and then source it: 

    $ source ~/.bashrc 

## Setup
First, clone autoscholar, like this: 

    $ cd ~/work_dir          # enter the working directory
    $ git clone https://github.com/forrestbao/autoscholar.git
    
## Usage
### Extract highlights on PDF files made in Mendeley 
Mendeley uses a sqlite database file to store the highlights in PDF papers. Currently CSV is the only format to dump the highlights into. The usage is:  

`python extract.py sqlite_db_file highlights_file` 

For example, 

    $ python extract.py path/to/your/mendeley/your@email.address@www.mendeley.com.sqlite highlights.csv

On Linux systems, default location of Mendeley database file is `/home/USERNAME/.local/share/data/Mendeley\ Ltd./Mendeley\ Desktop/`. 

### Count word frequencies 
You may further count the frequencies of words in extracted highlighted text, and store the result into another CSV-format file. The usage is: 

`python word_count.py highlights_file word_freq_file`

For example, 

    $ python word_count.py highlights.csv word_count.csv
