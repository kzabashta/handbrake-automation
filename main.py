import os
import mimetypes
import configparser

def __get_source_location(config):
    return config['source']['location']

def scan_source(location):
    for root, dirs, files in os.walk(location):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(file_path)
            if(mimetypes.guess_type(filename)[0] is not None and 
                mimetypes.guess_type(filename)[0].split('/')[0] == 'video'):
                print(filename)
                print

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    scan_source(__get_source_location(config))

if __name__ == '__main__':
    main()