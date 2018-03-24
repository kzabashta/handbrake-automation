import os
import mimetypes
import subprocess
import configparser

import click

def __get_source_location(config):
    return config['source']['location']

def __copy_temp(config, source_file_path, from_source=True):
    buffer_size=16*1024

    if from_source:
        source_path = config['source']['location']
    else:
        source_path = config['converted_temp']['location']
    copy_file_path = source_file_path.replace(source_path, '')[1:]
    if from_source:
        destination_path = os.path.join(config['temp']['location'], copy_file_path)
    else:
        destination_path = os.path.join(config['destination']['location'], copy_file_path)

    if not os.path.exists(os.path.dirname(destination_path)):
         os.makedirs(os.path.dirname(destination_path))

    try:
        os.remove(destination_path)
    except OSError:
        pass

    fsource = open(source_file_path, 'rb')
    fdestination = open(destination_path, 'wb')
    fsize = os.path.getsize(source_file_path)

    bar_label = 'Copying file %s' % source_file_path

    with click.progressbar(length=fsize, label=bar_label) as bar:
        while True:
            buf = fsource.read(buffer_size)
            if not buf:
                break
            fdestination.write(buf)
            bar.update(len(buf))

    fsource.close()
    fdestination.close()

    return destination_path

def scan_source(location):
    file_list = []
    for root, dirs, files in os.walk(location):
        for filename in files:
            file_path = os.path.join(root, filename)
            if(mimetypes.guess_type(filename)[0] is not None and 
                mimetypes.guess_type(filename)[0].split('/')[0] == 'video'):
                file_list.append(file_path)
    return file_list

def convert(source_path, config):
    handbrake_cli = config['handbrake']['location']
    source_path = __copy_temp(config, source_path)
    filename = os.path.splitext(os.path.basename(source_path))[0]+'.mp4'
    converted_temp_path = os.path.join(config['converted_temp']['location'], filename)

    handbrake_cli += ' -i "' + source_path + '" -o "' + converted_temp_path + '" --preset="Apple 1080p30 Surround"'

    subprocess.call(handbrake_cli)

    try:
        os.remove(source_path)
    except OSError:
        pass

    return converted_temp_path

def save(converted_path, config):

    __copy_temp(config, converted_path, from_source=False)

    try:
        os.remove(converted_path)
    except OSError:
        pass

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get a list of files to convert
    file_list = scan_source(__get_source_location(config))

    # start copying
    for file_path in file_list:
        converted_path = convert(file_path, config)
        save(converted_path, config)

if __name__ == '__main__':
    main()