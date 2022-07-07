#coding='utf-8'
import csv
import jieba.posseg as psg
from KEMT import kemt
from IROR import iror

with open('set/dataset.csv', 'r', newline='') as set:
    set_text = list(csv.reader(set))

output_sign = []
count = 1
lens = len(set_text)
for text in set_text:
    keywords = kemt(psg.cut(str(text)))
    output_sign.append(keywords)
    #if count % 50 == 0:
    print('[--------------{0:4d}/{1:d}--------------]'.format(count,lens))
    count += 1

with open('set/output_sign/output_sign.csv', 'w', newline='') as output:
    outputwrite = csv.writer(output)
    outputwrite.writerows(output_sign)
'''
for keyw in keyword_set:
    print(keyw)
'''
#指标
with open('set/output_sign/output_sign.csv', 'r', newline='') as output:
    output_sign = list(csv.reader(output))
with open('set/truth_sign/turth_sign.csv', 'r', newline='') as truth:
    truth_sign = list(csv.reader(truth))

IR, OR = iror(output_sign,truth_sign)
print('IR=',IR)
print('OR=',OR)
