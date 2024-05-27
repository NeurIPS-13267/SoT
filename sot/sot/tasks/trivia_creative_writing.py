import os
import re
from sot.tasks.base import Task, DATA_PATH
from sot.prompts.trivia_creative_writing import *
from sot.models import gpt
import json

class TriviaCreativeWritingTask(Task):
    """
    Input (x)   : a text instruction
    Output (y)  : a text generation
    Reward (r)  : # TODO
    Input Example: 
    Output Example: 
    """
    def __init__(self, file='trivia_creative_writing_100_n_5.jsonl'):
        """
        file: a text file, each line is some sentences
        """
        super().__init__()
        path = os.path.join(DATA_PATH, 'trivia_creative_writing', file)
        with open(path, "r") as f:
            self.data = [json.loads(line) for line in f]
        self.steps = 2
        #self.bug = []
        self.stops = ['\nPassage:\n', None]

    def __len__(self) -> int:
        return len(self.data)
    
    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def test_output(self, idx: int, output: str):
        output = output.split('Passage:\n')[-1]
        #prompt = score_prompt + output
        #score_outputs = gpt(prompt, n=5, model='gpt-4')
        scores = []
        correct_count = 0
        instance = self.data[idx]
        question_count = len(instance["answers"])
        for ans_to_question in instance["answers"]:
            for ans in ans_to_question:
                # compare all to lower
                if ans.lower() in output.lower():
                    correct_count += 1
                    print(ans)
                    break
        scores.append(correct_count)
        info = {'rs': scores, 'r': sum(scores) / question_count if scores else 0}
        return info
    
    @staticmethod
    def propose_prompt_wrap_writing(x: str, step: int, y: str='') -> str:
        datapoint = x 
        questions = datapoint["questions"]
        n = len(questions)
        topic = datapoint["topic"]
        if step == 0:
            questions_string = ''
            for index, value in enumerate(questions, 1):
                questions_string = questions_string + f"{index}.{value}"
            prompt = propose_prompt.format(n=n, questions=questions_string)
            #print(prompt)
            #prin
        elif step == 1:
            answers = y
            prompt = last_prompt.format(topic=topic, answers=answers)
        return prompt

    @staticmethod
    def propose_prompt_wrap_writing_other1(x: str, step: int, y: str='', self_answer='', self_reason='', answer='', reason='', confidence=0) -> str:
        datapoint = x 
        questions = datapoint["questions"]
        n = len(questions)
        topic = datapoint["topic"]
        if step == 0:
            questions_string = ''
            for index, value in enumerate(questions, 1):
                questions_string = questions_string + f"{index}.{value}"
            prompt = evaluate_prompt_.format(questions=questions_string,self_answers=self_answer, self_reasons=self_reason, answers=answer, reasons=reason, self_confidence_score=confidence)
            #print(prompt)
            #prin
        elif step == 1:
            answers = y
            prompt = last_prompt.format(topic=topic, answers=answers)
        return prompt

    @staticmethod
    def propose_prompt_wrap_writing_other(x: str, step: int, y: str='', answer='', reason='', passage='') -> str:
        datapoint = x 
        questions = datapoint["questions"]
        n = len(questions)
        topic = datapoint["topic"]
        if step == 0:
            questions_string = ''
            for index, value in enumerate(questions, 1):
                questions_string = questions_string + f"{index}.{value}"
            prompt = evaluate_prompt_1.format(questions=questions_string, answers=answer)
            #print(prompt)
            #prin
        elif step == 1:
            answers = y
            prompt = evaluate_prompt_2.format(topic=topic, answers=answers, passage=passage)
        return prompt

    def propose_prompt_wrap_writing_other2(x: str, step: int, y: str='', answer='', reason='') -> str:
        datapoint = x 
        questions = datapoint["questions"]
        n = len(questions)
        topic = datapoint["topic"]
        if step == 0:
            questions_string = ''
            for index, value in enumerate(questions, 1):
                questions_string = questions_string + f"{index}.{value}"
            prompt = evaluate_prompt_1.format(questions=questions_string, answers=answer, reasons=reason)
            #print(prompt)
            #prin
        elif step == 1:
            answers = y
            prompt = evaluate_prompt_2.format(topic=topic)
        return prompt

    @staticmethod
    def value_prompt_wrap(x: str, step: int, y: str='') -> str:
        if step == 0:
            answers = y.split('\n')
            while len(answers) < 5:
                answers.append('')
            datapoint = x 
            questions = datapoint["questions"]
            n = len(questions)
            topic = datapoint["topic"]
            print(y)
            print(len(questions))
            print(len(answers))
            #totals = [questions[i] + 'possible answer:' + answers[i] for i in range(n)]
            totals = [questions[i] + 'possible answer:' + answers[i].split(f'{i+1}.')[1] for i in range(n)]
            prompt = [check_prompt_1.format(totals=totals[i]) for i in range(n)]
            #prompt = check_prompt.format(totals=totals)
        elif step == 1:
            datapoint = x 
            topic = datapoint["topic"]
            answers = y
            prompt = last_prompt_last.format(topic=topic, answers=answers)
        return prompt

    @staticmethod
    def standard_prompt_wrap(x: str, y:str='') -> str:
        datapoint = x
        questions = datapoint["questions"]
        topic = datapoint["topic"]
        n = len(questions)
        questions_str = " ".join(questions)
        return standard_prompt.format(n=n, questions=questions_str, topic=topic) + y

    @staticmethod
    def cot_prompt_wrap(x: str, y:str='') -> str:
        datapoint = x
        questions = datapoint["questions"]
        topic = datapoint["topic"]
        n = len(questions)
        questions_str = " ".join(questions)
        return cot_prompt.format(n=n, questions=questions_str, topic=topic) + y

    @staticmethod
    def vote_prompt_wrap(x: str, ys: list) -> str:
        prompt = vote_prompt
        for i, y in enumerate(ys, 1):
            # y = y.replace('Plan:\n', '')
            # TODO: truncate the plan part?
            prompt += f'Choice {i}:\n{y}\n'
        return prompt
    
    @staticmethod
    def vote_outputs_unwrap(vote_outputs: list, n_candidates: int) -> list:
        vote_results = [0] * n_candidates
        for vote_output in vote_outputs:
            pattern = r".*best choice is .*(\d+).*"
            match = re.match(pattern, vote_output, re.DOTALL)
            if match:
                vote = int(match.groups()[0]) - 1
                if vote in range(n_candidates):
                    vote_results[vote] += 1
            else:
                print(f'vote no match: {[vote_output]}')
        return vote_results

    @staticmethod
    def compare_prompt_wrap(x: str, ys: list) -> str:
        assert len(ys) == 2, 'compare prompt only supports 2 candidates'
        ys = [y.split('Passage:\n')[-1] for y in ys]
        prompt = compare_prompt + f'Passage 1:\n{ys[0]}\n\nPassage 2:\n{ys[1]}\n'
        return prompt
    
    @staticmethod
    def compare_output_unwrap(compare_output: str):
        if 'more coherent passage is 1' in compare_output:
            return 0
        elif 'more coherent passage is 2' in compare_output:
            return 1
        elif 'two passages are similarly coherent' in compare_output:
            return 0.5
        else:
            print(f'-----------------compare no match: {[compare_output]}')
            return -1
