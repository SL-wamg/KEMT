#coding='utf-8'
#import csv
def iror(output_sign,truth_sign):
    def longest_common_subsequence( word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_len = 0
        row = 0
        col = 0
        # dp[i][j]表示word1以i结尾,word2以j结尾的最大公共子串的长度
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    if max_len < dp[i][j]:
                        max_len = dp[i][j]
                        row = i
                        col = j
        max_str = ''
        i = row
        j = col
        while i > 0 and j > 0:
            if dp[i][j] == 0:
                break
            i -= 1
            j -= 1
            max_str += word1[i]

        lcstr = max_str[::-1]
        #print(lcstr)    # 回溯的得到的最长公共子串
        return max_len
    '''
    with open('set/output_sign/output_sign.csv', 'r', newline='') as output:
        output_sign = list(csv.reader(output))
    with open('set/truth_sign/turth_sign.csv', 'r', newline='') as truth:
        truth_sign = list(csv.reader(truth))
    '''
    count = 0
    iror_vlaue = []
    print('指标评估开始')
    while count < (len(output_sign) or len(truth_sign)):  # 1层循环取每个文本的关键词集
        keyword_set1 = output_sign[count]  # 取出的每条数据的5个关键词
        keyword_set2 = truth_sign[count]
        now_set1_id = 0
        max_set1_id = 0
        while now_set1_id < len(keyword_set1):  # 2层循环读取该文本提取的单个关键词
            word1 = keyword_set1[now_set1_id]
            max_long = 0
            now_set2_id = 0
            max_set2_id = 0
            while now_set2_id < len(keyword_set2):  # 3层循环读取真实标记比较
                word2 = keyword_set2[now_set2_id]
                new_long = longest_common_subsequence(word1, word2)
                if new_long > max_long:  # 寻找最大的最长子序列，并标记
                    max_long = new_long  # 记录子串和位置ID
                    max_set1_id = now_set1_id  # output集 ID
                    max_set2_id = now_set2_id
                now_set2_id += 1
            IR = max_long / len(keyword_set2[max_set2_id])  # 完整度 = 最长子序列长度/真实标记的长度
            OR = max_long / len(keyword_set1[max_set1_id])  # 溢出度 = 最长子序列长度/抽取的长度
            #print(count, now_set1_id, max_set1_id, now_set2_id, max_set2_id, IR, OR)
            iror_vlaue.append([count + 1, IR, OR])
            now_set1_id += 1
        count += 1
    '''
    for number in iror_vlaue:
        print(number)
    '''
    i = 1
    ir_all = 0
    or_all = 0
    while i <= len(iror_vlaue):
        ir_all += iror_vlaue[i-1][1]
        or_all += iror_vlaue[i-1][2]
        i += 1
    IR = ir_all/(i-1)
    OR = or_all/(i-1)
    return IR, OR
