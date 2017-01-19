import struct
import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Parser for the mainframe MPS7')
parser.add_argument('-p', '--path', help='Path of a MPS7 data dump', required=True)
args = vars(parser.parse_args())

# Reads file in binary mode
dump_file = open(args['path'], 'rb')

# Record Types
DEBIT = 0
CREDIT = 1
StartAutopay = 2
EndAutopay = 3

# Skips magic number & version
dump_file.read(5)

num_records = struct.unpack('>i', dump_file.read(4))[0]

# Ordered dictionary since record memory is in a fixed order
record_desc = OrderedDict([
    ("type", [1, ">b"]),
    ("timestamp", [4, "!i"]),
    ("uid", [8, "!q"])
])

# Questions to solve
usr_credit = 0
usr_debit = 0
total_debits = 0
total_credits = 0
total_autopay_started = 0
total_autopay_ended = 0


# Convert byte to readable format
def get_byte_val(byte_format, read_size):
    data = dump_file.read(read_size)
    if data:
        return struct.unpack(byte_format, data)[0]
    else:
        return None


records = []
for x in range(0, num_records):
    record = OrderedDict()

    for key, value in record_desc.iteritems():
        record[key] = get_byte_val(value[1], value[0])

        # Credit/Debit Record Case
        if record.keys() == ['type', 'timestamp', 'uid']:
            if record['type'] == DEBIT:
                record['amt'] = get_byte_val("!d", 8)
                total_debits += record['amt']

            elif record['type'] == CREDIT:
                record['amt'] = get_byte_val("!d", 8)
                total_credits += record['amt']

    if record:
        # Question Solution Logic
        if record['uid'] == 2456938384156277127:
            if record['type'] == DEBIT:
                debit = record['amt']
            elif record['type'] == CREDIT:
                credit = record['amt']
        elif record['type'] == StartAutopay:
            total_autopay_started += 1
        elif record['type'] == EndAutopay:
            total_autopay_ended += 1

        records.append(record)

print "What is the total amount in dollars of debits? -- %s" % total_debits
print "What is the total amount in dollars of credits? -- %s" % total_credits
print "How many autopays were started? -- %d" % total_autopay_started
print "How many autopays were ended? -- %d" % total_autopay_ended
print "What is balance of user ID 2456938384156277127? -- %d" % (usr_credit - usr_debit)
