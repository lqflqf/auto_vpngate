from Parser import CsvParser
from Email import EmailProcessor
from collections import Counter

csv_parser = CsvParser.CSV_parser()

print("Total file " + str(len(csv_parser.files)))
print("")

# files = list(filter(lambda f: f.country_short == 'JP' \
#                and f.speed >= 5000000 \
#                and f.uptime >= 86400000, \
#                csv_parser.files))

cnt = Counter()

for f in csv_parser.files:
    cnt[f.country_long + ' ' + f.protocol] += 1

for k, v in sorted(cnt.items()):
    print(k + ": " + str(v))

files_to_save = list(filter(lambda f: f.protocol in ['udp'] and f.country_short in ['JP', 'US'], csv_parser.files))

print("")
print("saved files " + str(len(files_to_save)))

for f in files_to_save:
    f.save_file('test_files')

# if len(files) > 0:
#     EmailProcessor.processMail(files)








