import os
import mimetypes
import configparser

def __get_source_location(config):
    return config['source']['location']

def __copy_temp(config, source_file_path):
    source_path = config['source']['location']
    copy_file_path = source_file_path.replace(source_path, '')[1:]
    destination_path = os.path.join(config['temp']['location'], copy_file_path)

    length=16*1024
    copied = 0

    if not os.path.exists(os.path.dirname(destination_path)):
         os.makedirs(os.path.dirname(destination_path))

    fsource = open(source_file_path, 'rb')
    fdestination = open(destination_path, 'wb')
    fsize = os.path.getsize(source_file_path) / 1024

    while True:
        buf = fsource.read(length)
        if not buf:
            break
        fdestination.write(buf)
        copied += len(buf)
        print(copied)
    
    fsource.close()
    fdestination.close()

def scan_source(location):
    file_list = []
    for root, dirs, files in os.walk(location):
        for filename in files:
            file_path = os.path.join(root, filename)
            if(mimetypes.guess_type(filename)[0] is not None and 
                mimetypes.guess_type(filename)[0].split('/')[0] == 'video'):
                file_list.append(file_path)
    return file_list

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get a list of files to convert
    file_list = scan_source(__get_source_location(config))

    # start copying
    for file_path in file_list:
        __copy_temp(config, file_path)

if __name__ == '__main__':
    main()