from Parser import CsvParser
from Email import EmailProcessor

csv_parser = CsvParser.CSV_parser()

print("total file " + str(len(csv_parser.files)))

# files = list(filter(lambda f: f.country_short == 'JP' \
#                and f.speed >= 5000000 \
#                and f.uptime >= 86400000, \
#                csv_parser.files))

files = list(filter(lambda f: f.protocol == 'udp' and f.country_short in ['JP', 'US'], csv_parser.files))

print("files " + str(len(files)))

for f in files:
    f.save_file('test_files')


# if len(files) > 0:
#     EmailProcessor.processMail(files)








