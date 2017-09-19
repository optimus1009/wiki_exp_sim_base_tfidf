# coding=utf-8
class KeywordExtractor(object):
    #默认的停用词
    STOP_WORDS = set((
        "the", "of", "is", "and", "to", "in", "that", "we", "for", "an", "are",
        "by", "be", "as", "on", "with", "can", "if", "from", "which", "you", "it",
        "this", "then", "at", "have", "all", "not", "one", "has", "or", "that"
    ))
    #加载用户自定义停用词文件
    def set_stop_words(self, stop_words_path):
        abs_path = _get_abs_path(stop_words_path)
        if not os.path.isfile(abs_path):
            raise Exception("jieba: file does not exist: " + abs_path)
        content = open(abs_path, 'rb').read().decode('utf-8')
        #保存到stop_words中
        for line in content.splitlines():
            self.stop_words.add(line)

    def extract_tags(self, *args, **kwargs):
        raise NotImplementedError

#idf文件加载类
class IDFLoader(object):

    def __init__(self, idf_path=None):
        self.path = ""
        self.idf_freq = {}
        self.median_idf = 0.0
        if idf_path:
            self.set_new_path(idf_path)
    
    #从idf文件中读取词的idf值，保存到idf_freq字典中，用median_idf记录中位数
    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            self.path = new_idf_path
            content = open(new_idf_path, 'rb').read().decode('utf-8')
            self.idf_freq = {}
            for line in content.splitlines():
                word, freq = line.strip().split(' ')
                #保存词的idf值
                self.idf_freq[word] = float(freq)
            #中位数
            self.median_idf = sorted(
                self.idf_freq.values())[len(self.idf_freq) // 2]
    #获取idf值，median值
    def get_idf(self):
        return self.idf_freq, self.median_idf


class TFIDF(KeywordExtractor):

    def __init__(self, idf_path=None):
        self.tokenizer = jieba.dt #分词器
        self.postokenizer = jieba.posseg.dt
        self.stop_words = self.STOP_WORDS.copy() #停用词
        self.idf_loader = IDFLoader(idf_path or DEFAULT_IDF) #idf加载器
        self.idf_freq, self.median_idf = self.idf_loader.get_idf() #idf值字典
    #设置自定义路径
    def set_idf_path(self, idf_path):
        new_abs_path = _get_abs_path(idf_path)
        if not os.path.isfile(new_abs_path):
            raise Exception("jieba: file does not exist: " + new_abs_path)
        self.idf_loader.set_new_path(new_abs_path)
        self.idf_freq, self.median_idf = self.idf_loader.get_idf()

    def extract_tags(self, sentence, topK=20, withWeight=False, allowPOS=(), withFlag=False):
        """
        Extract keywords from sentence using TF-IDF algorithm.
        Parameter:
            - topK: 关键词数目. `None`代表全部
            - withWeight: 为真返回(word,weight)，为假只返回word
            - allowPOS: 关键词的词性列表，不在此列表的将被过滤
            - withFlag: 
        """
        #开始切词
        if allowPOS:
            allowPOS = frozenset(allowPOS)
            words = self.postokenizer.cut(sentence)
        else:
            words = self.tokenizer.cut(sentence)
        freq = {}
        for w in words:
            if allowPOS:
                if w.flag not in allowPOS:
                    continue
                elif not withFlag:
                    w = w.word
            wc = w.word if allowPOS and withFlag else w
            #停用词过滤
            if len(wc.strip()) < 2 or wc.lower() in self.stop_words:
                continue
            #计算tf值
            freq[w] = freq.get(w, 0.0) + 1.0
        total = sum(freq.values())
        for k in freq:
            kw = k.word if allowPOS and withFlag else k
            #计算tf_idf值
            freq[k] *= self.idf_freq.get(kw, self.median_idf) / total
        #返回tf-idf值最高的k个，作为关键词
        if withWeight:
            tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(freq, key=freq.__getitem__, reverse=True)
        if topK:
            return tags[:topK]
        else:
            return tags