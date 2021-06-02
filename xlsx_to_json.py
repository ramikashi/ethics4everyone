# -*- encoding: utf-8 -*-
import pandas as pd
import csv
import os

#this program actually just converts the ethics benchmark (in format JP | EN) to two separate jsons
#it's not designed as a general purpose converter, but rather a one-step converter to plug into the pipeline...
#so you don't need argparse either...

def xlsx_to_json(filename_no_ext, extension, Ja_jsonFileName, Eng_jsonFileName):
    #file_to_convert = 'C:\Users\...\master-benchmark_updated_translated_v0.85.xlsx'
    #filename_no_ext = os.path.splitext(filename)[0]
    if extension == ".xlsx":
        df = pd.read_excel(filename_no_ext + '.xlsx', header=0, encoding='UTF-8') #, sheetname='<your sheet>'
        df.to_csv(filename_no_ext + '.csv', index=False, quotechar='"', encoding='UTF-8')

    with open(filename_no_ext + '.csv', "r", encoding='UTF-8') as master_benchmark:
        with open(Ja_jsonFileName, "w", encoding='shiftjis') as jp_json:
            with open(Eng_jsonFileName, "w", encoding='shiftjis') as eng_json:
                jp_json.write('{\n')
                eng_json.write('{\n')
                reader = csv.reader(master_benchmark)
                next(reader)
                [ (jp_json.write("".join(row[0])+'\n'), eng_json.write("".join(row[1])+'\n')) for row in reader]
        jp_json.close()
        eng_json.close()
        
    return True
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="enter the full path of the file you want to convert")
    args = parser.parse_args()
    filename = args.filename
    filename_no_ext, extension = os.path.splitext(filename)
    #filename_no_ext = os.path.splitext(filename)[0]
    Ja_jsonFileName = filename_no_ext + '_jp.json'
    Eng_jsonFileName = filename_no_ext + '_eng.json'
    
    print(xlsx_to_json(filename_no_ext, extension, Ja_jsonFileName, Eng_jsonFileName))
    
if __name__ == '__main__':
    main()