from Parser import CsvParser
from Email import EmailProcessor
from itertools import groupby

csv_parser = CsvParser.CSV_parser()

print("Total file " + str(len(csv_parser.files)))
print("")

# files = list(filter(lambda f: f.country_short == 'JP' \
#                and f.speed >= 5000000 \
#                and f.uptime >= 86400000, \
#                csv_parser.files))


def name_func(f):
    return f.country_long + " " + f.protocol


g_iter = (groupby(sorted(csv_parser.files, key=name_func), key=name_func))

for k, g in g_iter:
    print(k + ": " + str(len(list(g))))


files_to_save = list(filter(lambda f: f.protocol in ['udp'] and f.country_short in ['JP', 'US'], csv_parser.files))


print("")
print("saved files " + str(len(files_to_save)))

for f in files_to_save:
    f.save_file('test_files')


# if len(files) > 0:
#     EmailProcessor.processMail(files)








