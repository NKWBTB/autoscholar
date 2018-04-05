import sys,os
import utility

if __name__ == "__main__":
    
    """
    "/home/todd/.local/share/data/Mendeley Ltd./Mendeley Desktop/junteng@iastate.edu@www.mendeley.com.sqlite" extracted_highlight.csv
    
    db=str(sys.argv[1])
    output=str(sys.argv[2])
    print("db:",db)
    print("output:",output)
    utility.main(db,output)
    """
    
    
    
    db=str(sys.argv[1])
    hl_output=str(sys.argv[2])
    pdf_output=str(sys.argv[3])
    print("db:",db)
    print("hl_output:",hl_output)
    print("pdf_output:",pdf_output)  
    utility.main(db,hl_output,pdf_output)
    
    
    