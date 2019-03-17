class GetBehavior(object):

    def __init__(self):
        pass

    def predict(self, text):
        pass

    def find_max(self, lst):
        output = [0]*9
        for i in lst:
            output = [a+b for a, b in zip(output, i)]
        sorted(output)[:3:-1]
        return output

    def core(self):
        #preprocessing
        # for file in files:
        #     filename = os.fsdecode(file)
        #     if filename.endswith(".txt"):
        #         fullText=""
        #         text = open(path+"/"+filename,mode="rb")
        #         for line in text:
        #             fullText = str(fullText)+ str(line.decode("utf-8"))
        #         clean_text=re.sub("[^ก-๙]+",'',fullText)
        #         result=word_tokenize(clean_text,engine='newmm')
        #         print(path+"/"+filename,end=" ")

        return self.find_max(lst)
        

