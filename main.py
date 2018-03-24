import os
import configparser

def __get_source_location(config):
    return config['source']['location']

def scan_source(location):
    print(location)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    scan_source(__get_source_location(config))

if __name__ == '__main__':
    main()