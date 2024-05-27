standard_prompt = '''Write a short and coherent passage about {topic} that incorporates the answers to the following {n} questions: {questions}
Your output should be of the following format:

Passage:
Your passage here.
'''

last_prompt = '''
Write a short and coherent passage about {topic} that incorporates the following: {answers}
Remember each words should be mentioned.
Please rate the reasonability, relevance, accuracy, coherence of your passage on a scale of 0 to 5.
Write the score directly without explanation.
Your output should be of the following format:

Passage:
Your passage here.
Confidence score:
Your score here.
'''

last_prompt_last = '''
Write a short and coherent passage about {topic} that incorporates the following: {answers}
Remember each words should be mentioned.
Your output should be of the following format:

Passage:
Your passage here.
'''

evaluate_prompt_2 ='''Other model has written a short and coherent passage about {topic} that incorporates the following: {answers}
passage:{passage}
Please rate the reasonability, relevance, accuracy, coherence of the passage on a scale of 0 to 5.
Please write a score directly without explanation.
Your output should be of the following format:
Score:
Give a score
'''

evaluate_prompt_ = '''You have answered following questions.
{questions}
Your answers:{self_answers}
Your reasons:{self_reasons}
Your confidence score:{self_confidence_score}
Other answers:{answers}
Other reasons:{reasons}
You need to rate the other answers on a scale of 0 to 5. Find different answers, and if you think Other answer is more correct, give them a higher score, and vice versa.
Score:
'''


evaluate_prompt_1 = '''Other model has answered serveral questions.
You need to determine whether these answers are correct and then give a score on a scale of 0 to 5. If you think all the answers are correct, give them 5 points. If you think some answers are wrong, reduce the score accordingly.
You can't be overconfident, and If you're not sure about the answer, You shouldn't give it a score.
You must format the output as in the example, including analysis and score.
Hera is an example:
questions:1.\"Who was the target of the failed \"\"Bomb Plot\"\" of 1944?\"2.Who had an 80s No 1 hit with Hold On To The Nights?3.Which musical featured the song The Street Where You Live?4.In what year's Olympics were electric timing devices and a public-address system used for the first time?5.Who was the director of the CIA from 1976-81?
Answer: 
1. Adolf Hitler
2. Richard Marx
3. My Fair Lady
4. 1912
5. Stansfield Turner
Analysis:I think the answer to question five is George Bush. I'm not sure answer to question three is correct. So there are three answers that I think are correct. 
Score: 3
------------------New questions------------------------
questions:{questions}
Answers:{answers}
'''

cot_prompt = '''Please answer the following {n} questions: {questions}
Please write the answer directly without explanation.
Your output should be of the following format:
Answer:
1.
2.
'''

check_prompt = '''Please modify the answers to these questions if the possible answer is wrong.
{totals}
Please write your answers to the questions directly without explanation.
Don't repeat the question.
Your output should be of the following format:

Answer:
Your answer here
'''

check_prompt_1 = '''Please modify the answer if you think the possible answer is wrong.
{totals}
Please write your answer to the question directly without explanation.
Your output should be of the following format:

Answer:
Your answer here
'''

check_prompt_2 = '''
'''

'''
propose_prompt = Please answer the following {n} questions: {questions}
Please write the answer directly without explanation.
Your output should be of the following format:

Answer:
1.
2.
'''

propose_prompt = '''
Please answer the following {n} questions.
How confident are you in your answer on a scale of 0 to 5.
You can't be overconfident, and unless you're absolutely sure, you should give a low score.
You must format the output as in the example.
Here are some examples:
questions:1.Who was the man behind The Chipmunks?2.Which Lloyd Webber musical premiered in the US on 10th December 1993?3.Who was the next British Prime Minister after Arthur Balfour?4.Who had a 70s No 1 hit with Kiss You All Over?5.What claimed the life of singer Kathleen Ferrier?
response_gpt_iterate: Answer:
1. Ross Bagdasarian Sr.
2. Sunset Boulevard
3. Henry Campbell-Bannerman
4. Exile
5. Breast cancer
I'm not sure about the answer to question one and two. I'm sure of the other three answers
Confidence score:3

questions:1.\"Who was the target of the failed \"\"Bomb Plot\"\" of 1944?\"2.Who had an 80s No 1 hit with Hold On To The Nights?3.Which musical featured the song The Street Where You Live?4.In what year's Olympics were electric timing devices and a public-address system used for the first time?5.Who was the director of the CIA from 1976-81?
Answer: 
1. Adolf Hitler
2. Richard Marx
3. My Fair Lady
4. 1912
5. Stansfield Turner
I'm not sure about the answers to questions two, four and five.I'm sure of the other two answers
Confidence score:2

questions:{questions}

'''

evaluate_prompt = '''You have answered following questions.
{questions}
Your answers:{self_answers}
Other answers:{answers}
You need to rate the other answers on a scale of 0 to 5.
Score:
'''

propose_prompt_last = '''
Please answer the following {n} questions: {questions}
Please write the answer directly without explanation.
How confident are you in your answer on a scale of 0 to 10.
Your output should be of the following format:
Answer:
1.
2.
Confidence score:
'''

propose_prompt_1 = '''Please answer the following {n} questions: {questions}
Please write the answer directly without explanation.
Your output should be of the following format:

Answer:
Your answer here.
'''

propose_prompt_2 = '''I need to write a short and coherent passage about {topic} that incorporates the following: {answers}
You need to give me an outline.
No more than thirty words.
Your output should be of the following format:

Outline:
Your outline here
'''

vote_prompt = '''Given an instruction and several choices, decide which choice is most promising. Analyze each choice in detail, then conclude in the last line "The best choice is {s}", where s the integer id of the choice.
'''

compare_prompt = '''Briefly analyze the coherency of the following two passages. Conclude in the last line "The more coherent passage is 1", "The more coherent passage is 2", or "The two passages are similarly coherent".
'''

score_prompt = '''Analyze the following passage, then at the last line conclude "Thus the coherency score is {s}", where s is an integer from 1 to 10.
'''
