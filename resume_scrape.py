from PIL import Image
import pytesseract
import argparse
import os
import nltk
import operator

resumes_dir = "./Resumes"
keywords = [("machine learning", 5), ("python", 4), ("tensorflow", 3), ("pytorch", 3), ("programming", 2), ("development", 2)]
resumes = []
num_resumes = 5
total_score = sum(j for i, j in keywords)

class Resume:
    def __init__(self,tokens,filename,score=0, matched_tokens=[]):
        self.tokens = tokens
        self.filename = filename
        self.score = score
        self.matched_tokens = matched_tokens

    def calculate_score(self):
        for (keyword, weight) in keywords:
            keyword_matched = False
            for token in tokens:
                if keyword_matched:
                    break
                l_distance = nltk.edit_distance(token, keyword)
                if l_distance <= 3:
                    self.score += weight
                    self.matched_tokens.append(keyword)
                    keyword_matched = True

        return self.score



if __name__ == '__main__':
    for file in os.listdir(resumes_dir):
        if file == ".DS_Store":
            continue

        print("Currently reading " + file)
        filepath = resumes_dir + "/" + file
        img = Image.open(filepath).convert('L')
        resume_text = pytesseract.image_to_string(img, lang = "eng")
        resume_text = resume_text.lower()
        print(resume_text)
        tokens = nltk.word_tokenize(resume_text)
        new_resume = Resume(tokens,file)
        new_resume.calculate_score()
        resumes.append(new_resume)


    resumes = sorted(resumes, key=operator.attrgetter('score'), reverse=True)
    with open("top_{}_resumes.txt".format(num_resumes), "w") as text_file:
        print("Top {} Resumes".format(num_resumes))
        for i in range(num_resumes):
            text_file.write(resumes[i].filename + "match: {}% \n".format(resumes[i].score/total_score*100))
            print("Rank {}: {} \n".format(i+1, resumes[i].filename))
            print("Score: {} \n".format(resumes[i].score))
            print("Tokens: {} \n".format(resumes[i].tokens))
            print("Matched Tokens: {}".format(resumes[i].matched_tokens))

