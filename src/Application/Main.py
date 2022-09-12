from datetime import datetime  

from Config import *
from Styles import UI
from Common import Inspect  
from Common import Select  
from Common import Execute  

def main():

    UI.print_console() 

    features = Inspect.inspect_features()

    selection = Select.inquire_selection(features)

    execution = Execute.execute(selection) 

    selection = input("\nContinue (Y/N): ")
    if selection == "Y":
        main()
    else:
        return

if __name__ == '__main__':
    beg = datetime.now()
    main()
    end = datetime.now()
    duration = end - beg
    duration = duration.total_seconds()
    
    print(f"\nProgram finished in {duration:.2f} sec")
