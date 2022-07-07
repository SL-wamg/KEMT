#coding='utf-8'
import csv

def kemt(seg_initial):

    #------------------------------------------------------------------------------------------------------数据读取及初始化阶段
    wordid = 1                  #词序标
    with open('read/stopwords.txt', 'r', encoding='utf-8', newline='\n') as stopword:
        stopwords = stopword.read()
    #------------------------------------------------------------------------------------------------CWE阶段
    temp_compoundwords = []
    CWE = []
    pass            #发表后公开
    #------------------------------------------------------------------------------------------------STE阶段
    sentenceid = 1
    shortsentenceid = 1
    temp_STE = []               #STE的临时输出
    STE = []                    #STE的最终输出
    with open('read/point_sentence.txt', 'r', newline='\n', encoding='utf-8') as point_sentence:
        point_sentence = point_sentence.read()
    with open('read/point_shortsentence.txt', 'r', newline='\n', encoding='utf-8') as point_shortsentence:
        point_shortsentence = point_shortsentence.read()
    with open('read/parallel_set.txt', 'r', newline='\n', encoding='utf-8') as parallel_set:
        parallel_set = parallel_set.read()
    with open('read/pretrigger_word.txt', 'r', newline='\n', encoding='utf-8') as pretrigger_word:
        pretrigger = pretrigger_word.read()
    with open('read/post_trigger_word.txt', 'r', newline='\n', encoding='utf-8') as post_trigger:
        post_trigger = post_trigger.read()
    #------------------------------------------------------------------------------定义预处理的基础列表
    basalwords = list()             #基本词汇集
    BWE = []                   #停用后的基础词汇
    #------------------------------------------------------------------------------------------------------数据处理阶段
    wordtemp = '*********'
    for word,flag in seg_initial:
        # -------------------------------------------------------------------------CWE无效区间判断
        pass
        # -------------------------------------------------------------------------CWE第一二阶段结果
        pass
        # -------------------------------------------------------------------------STE标志区间判断
        if wordtemp in point_sentence:                       #句子计数
            point_sentence_tag = '~'    #~号代表句子断句           #测试语句
            sentenceid += 1
            shortsentenceid = 1         #重置短句计数号
        else: point_sentence_tag = '@'  #@号代表同一个句子              #测试语句
        if wordtemp in point_shortsentence:                 #短句计数
            point_shortsentence_tag = '^'   #^号代表短句断句           #测试语句
            shortsentenceid += 1
        else: point_shortsentence_tag = '&'#&号代表同一个短句              #测试语句
        if word in parallel_set:                            #词关系集标志
            relation_tag = '='
        elif word in pretrigger:
            relation_tag = '←'
        elif word in post_trigger:
            relation_tag = '→'
        else: relation_tag = 'no'        #!代表非关系词
        wordtemp = word
        # -------------------------------------------------------------------------STE结果
        temp = [wordid, word, point_sentence_tag, sentenceid, point_shortsentence_tag, shortsentenceid, relation_tag]    #测试语句
        temp_STE.append(temp)   #测试语句
        STE.append([word, wordid, sentenceid, shortsentenceid, relation_tag])     #-----------------------STE最终输出
        # -------------------------------------------------------------------------基础无效词判断
        if (word in stopwords) or (flag in posfilter and len(word) < 3):          #这个地方要改
            basalwords_tag = '-'        #-号表示停用
        else: basalwords_tag = '+'      #+号表示非停用，即基础词集
        # -------------------------------------------------------------------------基础词序写入
        basalwords.append([wordid, word, basalwords_tag])
        # -------------------------------------------------------------------------词序计数
        wordid += 1
    # -----------------------------------------------------------------------------CWE输出阶段结果写入
    link_compoundwords_tag = 0          #复合词首词标签
    first_id = 0                        #复合词首词词位
    last_id =  0                        #复合词尾词词位
    count = 0                           #复合词计数器
    for wordid, word, flag, delete_tags in temp_compoundwords:  #-----------------------------------------------------CWE最终输出
        pass
    for wordid, word, basalwords_tag in basalwords:    #基础词集写入
        if basalwords_tag == '+':
            BWE.append([word,wordid])
    #------------------------------------------------------------------------------------------------------数据测试阶段
    '''
    # 配合测试CWE12阶段的输出
    with open('复合词中间结果.csv', 'w', newline='') as cfile:
        cwrite = csv.writer(cfile)
        cwrite.writerows(temp_compoundwords)
    # 配合测试CWE最终的输出
    with open('CWE输出.csv', 'w',newline='') as cwefile:
        cwewrite = csv.writer(cwefile)
        cwewrite.writerows(CWE)
    # 配合测试STE中间的输出
    with open('语法树中间结果.csv', 'w', newline='\n') as stefile:
        swrite = csv.writer(stefile)
        swrite.writerows(temp_STE)
    # 配合测试STE最终输出
    with open('STE输出.csv', 'w', newline='\n') as stefile:
        swrite = csv.writer(stefile)
        swrite.writerows(STE)
    # 配合测试基础词的输出
    with open('基础词集中间结果.csv', 'w', newline='') as bfile:
        bwrite = csv.writer(bfile)
        bwrite.writerows(basalwords)
    # 配合测试基础词的最终输出
    with open('BWE输出.csv', 'w', newline='') as Bfile:
        Bwrite = csv.writer(Bfile)
        Bwrite.writerows(BWE)
    '''
    for i in range(len(CWE)-1,-1,-1):             #过滤字长小于3的非复合词
        if CWE[i][1] == CWE[i][2] and len(CWE[i][0])< 3:
            CWE.remove(CWE[i])
    for i in range(len(BWE)-1,-1,-1):             #过滤到小于字长小于2的基础词
        if len(BWE[i][0]) <2:
            BWE.remove(BWE[i])
    bwe = BWE
    cwe = CWE
    ste = STE
    # ---------------------------------------------------------------------------------------------建立特征迁移------树
    # --------------------------------------------------------------------第1.1部分，建立复合词的特征迁移树
    count = 0
    end = len(cwe) - 1
    CWE_calculate_pro = []
    for word, word_begin, word_end in cwe:
        # 获取复合词的句子、短句ID
        word_sentenceid = ste[int(word_begin)][2]
        word_shortsentenceid = ste[int(word_begin)][3]
        # 获取复合词的语境
        rela_tag = 'no'
        if count == 0:  # 首词只有后置词
            next_word_begin = cwe[count + 1][1]
            for ele in ste[int(word_end) - 1:int(word_end) +3]:
                if ele[4] == '←':
                    rela_tag = '+'
                    break
        elif count == end:  # 尾词只有前置词
            pro_word_end = cwe[count - 1][2]
            for ele in ste[int(word_begin)-3:int(word_begin):1]:
                if ele[4] == '→':
                    rela_tag = '+'
                    break
        else:
            pro_word_end = cwe[count - 1][2]
            next_word_begin = cwe[count + 1][1]
            for ele in ste[int(word_begin)-3:int(word_begin):1]:  # 前置词
                if ele[4] == '→':
                    rela_tag = '+'
            for ele in ste[int(word_end) - 1:int(word_end) + 3]:  # 后置词
                if ele[4] == '←':
                    rela_tag = '+'
        CWE_calculate_pro.append([word, word_sentenceid, word_shortsentenceid, rela_tag])
        count += 1
    # --------------------------------------------------------------------第1.2部分，建立基础词的特征迁移树
    count = 0
    end = len(bwe) - 1
    BWE_calculate_pro = []
    for word, word_id in bwe:
        # 获取基础词的句子、短句ID
        word_sentenceid = ste[int(word_id)][2]
        word_shortsentenceid = ste[int(word_id)][3]
        # 获取基础词的语境
        rela_tag = 'no'
        if count == 0:  # 首词只有后置词
            next_word_id = bwe[count + 1][1]
            for ele in ste[int(word_id) - 1:int(word_id) + 3]:
                if ele[4] == '←':
                    rela_tag = '+'
                    break
        elif count == end:  # 尾词只有前置词
            pro_word_id = bwe[count - 1][1]
            for ele in ste[int(word_id)-3:int(word_id):1]:
                if ele[4] == '→':
                    rela_tag = '+'
                    break
        else:
            pro_word_id = bwe[count - 1][1]
            next_word_id = bwe[count + 1][1]
            for ele in ste[int(word_id)-3:int(word_id):1]:  # 前置词
                if ele[4] == '→':
                    rela_tag = '+'
            for ele in ste[int(word_id) - 1:int(word_id)+3]:  # 后置词
                if ele[4] == '←':
                    rela_tag = '+'
        BWE_calculate_pro.append([word, word_sentenceid, word_shortsentenceid, rela_tag])
        count += 1
    '''
    #--------------------------------------------------------------------测试
    with open('层-特征迁移CWE.csv', 'w',newline='') as TCWE:
        cwrite = csv.writer(TCWE)
        cwrite.writerows(CWE_calculate_pro)
    with open('层-特征迁移BWE.csv', 'w',newline='') as TBWE:
        bwrite = csv.writer(TBWE)
        bwrite.writerows(BWE_calculate_pro)
    '''
    # ---------------------------------------------------------------------------------------------建立词汇的特征迁移---图
    # --------------------------------------------------------------------词的特征迁移图函数
    def combine(words_set):
        set = words_set
        begen_a = 0
        temp_combine = []
        while len(set) != 0:
            word_a, sflag_a, ssflag_a, rflag_a = set[0]
            temp_combine.append([[word_a], [sflag_a, ssflag_a, rflag_a]])
            del set[0]
            set_copy = set
            begen_b = 0
            while begen_b < len(set_copy):
                word_b, sflag_b, ssflag_b, rflag_b = set_copy[begen_b]
                if word_b == word_a:
                    temp_combine[begen_a].append([sflag_b, ssflag_b, rflag_b])
                    del set_copy[begen_b]  # 删除一个已读取的重复值
                    begen_b -= 1
                begen_b += 1
            set = set_copy
            begen_a += 1
        return temp_combine
    CWE_calculate = combine(CWE_calculate_pro)  # 特征迁移后的复合词---------最终输出
    BWE_calculate = combine(BWE_calculate_pro)  # 特征迁移后的基础词---------最终输出
    '''
    with open('图-特征迁移CWE.csv', 'w', newline='') as TCWE:
        ccwrite = csv.writer(TCWE)
        ccwrite.writerows(CWE_calculate)  
    with open('图-特征迁移BWE.csv', 'w', newline='') as TBWE:
        bbwrite = csv.writer(TBWE)
        bbwrite.writerows(BWE_calculate)
    '''
    # ---------------------------------------------------------------------------------------------异构贡献度计算
    # --------------------------------------------------------------------定义异构计算函数
    def diff_calculate_ave(graph_set):  # 异构平均式计算
        count = 1
        temp_vlaue = 0
        vlaue = 0
        long = len(graph_set)
        while count < len(graph_set):
            sflag, ssflag, relaflag = graph_set[count]
            pass
            vlaue += temp_vlaue
            count += 1
        vlaue /= (long - 1)
        return vlaue
    def diff_calculate_no_ave(graph_set):  # 异构总值计算
        count = 1
        temp_vlaue = 0
        vlaue = 0
        long = len(graph_set)
        while count < long:
            sflag, ssflag, relaflag = graph_set[count]
            pass
            vlaue += temp_vlaue
            count += 1
        return vlaue
    # --------------------------------------------------复合词异构贡献值输出
    c_diff_vlaue = []
    for words in CWE_calculate:
        c_diff_vlaue1 = diff_calculate_ave(words)
        c_diff_vlaue2 = diff_calculate_no_ave(words)
        c_diff_vlaue.append([words[0][0], c_diff_vlaue1, c_diff_vlaue2])
    # --------------------------------------------------基础词异构贡献值输出
    b_diff_vlaue = []
    for words in BWE_calculate:
        b_diff_vlaue1 = diff_calculate_ave(words)
        b_diff_vlaue2 = diff_calculate_no_ave(words)
        b_diff_vlaue.append([words[0][0], b_diff_vlaue1, b_diff_vlaue2])
    '''
    # --------------------------------------------------词汇异构贡献度测试输出
    with open('异构贡献度-CWE.csv', 'w', newline='') as DIFFCWE:
        dcwrite = csv.writer(DIFFCWE)
        dcwrite.writerows(c_diff_vlaue)
    with open('异构贡献度-BWE.csv', 'w', newline='') as DIFFBWE:
        dbwrite = csv.writer(DIFFBWE)
        dbwrite.writerows(b_diff_vlaue)
    '''
    # ---------------------------------------------------------------------------------------------同构贡献度计算
    # --------------------------------------------------------------------函数，前七
    def ahead_seven_avg(diff_vlaue):  # 第一通道，找到平均值前7
        temp_ahead_seven = []
        temp_set = diff_vlaue
        times = 0
        while times < 7 :
            count = 0
            max = 0
            max_id = 0
            for word, avg, total in temp_set:
                if float(avg) > max :
                    max = float(avg)
                    max_id = count
                count += 1
            temp_ahead_seven.append([temp_set[max_id][0], temp_set[max_id][1], temp_set[max_id][2]])
            del temp_set[max_id]
            times += 1
        return temp_ahead_seven
    def ahead_seven_no_avg(diff_vlaue):  # 第二通道，找到总值前10
        temp_ahead_seven = []
        temp_set = diff_vlaue
        times = 0
        while times < 10 :
            count = 0
            max = 0
            max_id = 0
            for word, avg, total in temp_set:
                if float(total) > max:
                    max = float(total)
                    max_id = count
                count += 1
            temp_ahead_seven.append([temp_set[max_id][0], temp_set[max_id][1], temp_set[max_id][2]])
            del temp_set[max_id]
            times += 1
        return temp_ahead_seven
    # --------------------------------------------------------------------函数，同构
    def alike_calculate_avg(ahead_seven_avg):  # 第一通道，对均值前7同构化
        temp_alike_calculate = []
        max = float(ahead_seven_avg[0][1])
        min = float(ahead_seven_avg[len(ahead_seven_avg)-1][1])
        baseline = max - min
        for word, avg, total in ahead_seven_avg:
            vlaue = (float(avg) - min) / baseline
            temp_alike_calculate.append([word, vlaue])
        return temp_alike_calculate
    def alike_calculate_no_avg(ahead_seven_no_avg):  # 第二通道，对总值前7同构化
        temp_alike_no_calculate = []
        max = float(ahead_seven_no_avg[0][2])
        min = float(ahead_seven_no_avg[6][2])
        baseline = max - min
        for word, avg, total in ahead_seven_no_avg:
            vlaue = (float(total) - min) / baseline
            temp_alike_no_calculate.append([word, vlaue])
        return temp_alike_no_calculate
    # --------------------------------------------------------------------调函数，取前7
    c_ahead_seven_avg = ahead_seven_avg(c_diff_vlaue)
    #c_ahead_seven_no_avg = ahead_seven_no_avg(c_diff_vlaue)
    #b_ahead_seven_avg = ahead_seven_avg(b_diff_vlaue)
    b_ahead_seven_no_avg = ahead_seven_no_avg(b_diff_vlaue)
    # --------------------------------------------------------------------调函数，同构贡献度
    c_ahead_seven_alike_calculate_avg = alike_calculate_avg(c_ahead_seven_avg)
    #c_ahead_seven_alike_calculate_no_avg = alike_calculate_no_avg(c_ahead_seven_no_avg)
    #b_ahead_seven_alike_calculate_avg = alike_calculate_avg(b_ahead_seven_avg)
    b_ahead_seven_alike_calculate_no_avg = alike_calculate_no_avg(b_ahead_seven_no_avg)
    # ---------------------------------------------------------------------------------------------第一候选词集-返回同构贡献度
    # 第一候选词集1
    c_ahead_seven_alike_calculate_avg += b_ahead_seven_alike_calculate_no_avg
    candidate_wordset1 = c_ahead_seven_alike_calculate_avg
    #print(candidate_wordset1)
    '''
    #第一候选词集2
    c_ahead_seven_alike_calculate_avg += b_ahead_seven_alike_calculate_avg
    candidate_wordset2 = c_ahead_seven_alike_calculate_avg
    print(candidate_wordset2)
    #第一候选词集
    c_ahead_seven_alike_calculate_no_avg += b_ahead_seven_alike_calculate_no_avg
    candidate_wordset3 = c_ahead_seven_alike_calculate_no_avg
    print(candidate_wordset3)
    #第一候选词集
    c_ahead_seven_alike_calculate_no_avg += b_ahead_seven_alike_calculate_avg
    candidate_wordset4 = c_ahead_seven_alike_calculate_no_avg
    print(candidate_wordset4)
    with open('候选词集-未消融.csv', 'w', newline='') as candidate:
        candwrite = csv.writer(candidate)
        candwrite.writerows(candidate_wordset1)
    '''
    # ---------------------------------------------------------------------------------------------消融规则
    condidate = candidate_wordset1
    melt_conditate = []
    while len(condidate) != 0:
        word1 = condidate[0][0]
        vlaue1 = condidate[0][1]
        melt_conditate.append([word1, vlaue1])
        del condidate[0]
        condidate_copy = condidate
        count = 0
        while count < len(condidate_copy):
            word2 = condidate_copy[count][0]
            vlaue2 = condidate_copy[count][1]
            lista = str(word1)
            listb = str(word2)
            if (lista.find(listb) != -1) or (listb.find(lista) != -1):
                del condidate_copy[count]
                count -= 1
            count += 1
        condidate = condidate_copy
    '''
    with open('候选词集-消融.csv', 'w', newline='') as candidate_late:
        candwrite = csv.writer(candidate_late)
        candwrite.writerows(melt_conditate)
    '''
    # --------------------------------------------------------------------函数Top-N，融合词集前五
    def ahead_five(melt_conditate):
        temp_ahead_five = []
        temp_set = melt_conditate
        times = 0
        while times < 5:
            count = 0
            max = 0
            max_id = 0
            for word, vlaue in temp_set:
                if float(vlaue) > max:
                    max = float(vlaue)
                    max_id = count
                count += 1
            temp_ahead_five.append([temp_set[max_id][0]])
            del temp_set[max_id]
            times += 1
        return temp_ahead_five
    keywords = ahead_five(melt_conditate)
    return keywords