import sys
import argparse
import os
import logging

VERSION = "1.0.0"

#############################
# FUNCTIONS
#############################

def get_commandline_parser():

    version_string = r'%(prog)s ' + VERSION
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), description='Process library.')
    parser.add_argument('-c', '--bytes', action='store_true', default=False, help='print the byte counts')
    parser.add_argument('-m', '--chars', action='store_true', default=False, help='print the character counts')
    parser.add_argument('-l', '--lines', action='store_true', default=False, help='print the newline counts')
    parser.add_argument('-L', '--max-line-length', action='store_true', default=False, help='print the lenght of the longest line')
    parser.add_argument('-w', '--words', action='store_true', default=False, help='print the word counts')
    parser.add_argument('--version', action='version', version=version_string, help='output version information and exit')
    parser.add_argument('file', nargs='*', help='file to be processed')

    return parser

def get_logger():

    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)

    log_file = os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".log"
    ch = logging.FileHandler(log_file, mode='w')
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger

def get_input_file(input_arguments):

    return input_arguments.file[0]

def get_input_settings(input_arguments):

    settings = {}

    settings['bytes'] = input_arguments.bytes
    settings['chars'] = input_arguments.chars
    settings['lines'] = input_arguments.lines
    settings['max-line-length'] = input_arguments.max_line_length
    settings['words'] = input_arguments.words

    return settings

def get_file_content(input_file):

    with open(input_file) as f:
        return f.read()

def get_characters_count(buffer):

    # simplified version; assumes 8 bits for a character
    return len(buffer)

def get_lines_count(buffer):

    if len(buffer) > 0:
        return buffer.count("\n") + 1 # +1 in case of single line without "\n" at the end
    else:
        return 0 # empty buffer

def get_max_line_length(buffer):

    max_len = 0

    buffer_array = buffer.split("\n")

    for line in buffer_array:
        logger.debug("checking line: %s" % line)

        line_len = len(line)

        if line_len > max_len:
            logger.debug("line len %d is greater then current max_len %d. New max_len set" % (line_len, max_len))

            max_len = line_len

    return max_len

def get_words_count(buffer):

    return len(buffer.split())

#############################
# MAIN PROGRAM
#############################

parser = get_commandline_parser()
logger = get_logger()

input_arguments = parser.parse_args()

input_file = get_input_file(input_arguments)
input_file_content = get_file_content(input_file)

settings = get_input_settings(input_arguments)

if settings['bytes']:

    logger.info("get bytes")

    result = os.path.getsize(input_file)

elif settings['chars']:

    result = get_characters_count(input_file_content)

elif settings['lines']:

    result = get_lines_count(input_file_content)

elif settings['max-line-length']:

    result = get_max_line_length(input_file_content)

elif settings['words']:

    result = get_words_count(input_file_content)

else:

    result = "%d %d %d" % (get_lines_count(input_file_content),
                           get_words_count(input_file_content),
                           get_characters_count(input_file_content))


print "%s %s" % (result, input_file)

