import sys,os
import utility

if __name__ == "__main__":
    db=str(sys.argv[1])
    output=str(sys.argv[2])
    print("db:",db)
    print("output:",output)
    utility.main(db,output)
