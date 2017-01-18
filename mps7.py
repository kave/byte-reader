import argparse

parser = argparse.ArgumentParser(description='Parser for the mainframe MPS7')
parser.add_argument('-p', '--path', help='Path of a MPS7 data dump', required=True)
args = vars(parser.parse_args())

dump_file = open(args['path'], 'rb')

print dump_file.read()

DEBIT = 0
CREDIT = 1
StartAutopay = 2
EndAutopay = 3

