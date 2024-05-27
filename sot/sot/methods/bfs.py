import itertools
import numpy as np
from functools import partial
from sot.models import gpt, gemini, palm2
import os
import re
import sympy
import time
import re


def extract_confidence(proposals):
    if 'core:' not in proposals:
      return 0
    try:
        match = re.search(r'\d+', proposals.split('core:')[-1])
        if match:
            confidence_value = int(match.group(0))
            if 0 <= confidence_value <= 5:
                return confidence_value
            else:
                return 0
        else:
            return 0
    except ValueError:
        return 0

def get_values_writing(task, x, ys, n_evaluate_sample, mixed, step, correct_number=0, prompt=''):
    global gpt
    if step == 0:
        #return ys, correct_number, prompt
        gpt = partial(gpt, model='gpt-4')
        prompt = task.value_prompt_wrap(x, step, ys)
        if type(prompt) == list:
            output_list = []
            for i in range(len(prompt)):
                gpt_output = gpt(prompt[i], stop=None)[0]  
                answer = gpt_output.split('Answer:')[-1].strip()  
                formatted_output = f'{i+1}.{answer}'
                output_list.append(formatted_output) 
            output = '\n'.join(output_list)
        #output = gpt(prompt, stop=None)[0].split('Answer:')[-1].strip()
        #print(output)
        #answers = output.split('\n')
        #possible_answers = y.split('\n')
        #correct_number = 0
        #for i in range(len(answers)):
        #    if possible_answers[i] == answers[i]:
        #        correct_number += 1 
        ys = output
    elif step == 1:
        prompt = task.value_prompt_wrap(x, step, ys)
        print('PROMPT: ', prompt)
        output = gpt(prompt, stop=None)[0].split('Passage:')[-1].strip()
        ys = output
    return ys

def get_proposals_writing(task, x, y, mixed, step): 
    global gpt
    if step == 0:
        gpt = partial(gpt, model='gpt-3.5-turbo')
        propose_prompt = task.propose_prompt_wrap_writing(x, step, y)
        tem = 0.1
        confidence_gpt = []
        confidence_gemini = []
        confidence_palm = []
        proposals = []
        proposals_gpt_raw = gpt(propose_prompt, n=1, stop=None, temperature = tem)[0].split('Answer:')[-1].strip()
        proposals_gpt_answer = proposals_gpt_raw.split('I\'m')[0].strip()
        #proposals_gpt_reason = proposals_gpt_raw.split('Reason:')[-1].split('I\'m')[0].strip()
        confidence_gpt.append(extract_confidence(proposals_gpt_raw))
        proposals.append(proposals_gpt_answer)
        print('proposals_gpt_raw:', proposals_gpt_raw)
        
        time.sleep(5)
        proposals_gemini_raw = gemini(propose_prompt).split('Answer:')[-1].strip()
        proposals_gemini_answer = proposals_gemini_raw.split('I\'m')[0].strip()
        #proposals_gemini_reason = proposals_gemini_raw.split('Reason')[-1].split('I\'m')[0].strip()
        confidence_gemini.append(extract_confidence(proposals_gemini_raw))
        proposals.append(proposals_gemini_answer)
        print('proposals_gemini_raw:', proposals_gemini_raw)
        #proposals = proposals_raw.split('Score')[0].strip()
        #input('continue')

        time.sleep(5)
        proposals_palm_raw = palm2(propose_prompt).split('Answer:')[-1].strip()
        proposals_palm_answer = proposals_palm_raw.split('I\'m')[0].strip()
        #proposals_palm_reason = proposals_palm_raw.split('Reason')[-1].split('I\'m')[0].strip()
        confidence_palm.append(extract_confidence(proposals_palm_raw))
        proposals.append(proposals_palm_answer)
        print('proposals_palm_raw:', proposals_palm_raw)

        evaluate_prompt_gemini = task.propose_prompt_wrap_writing_other(x, step, y, proposals_gemini_answer, '')
        evaluate_prompt_gpt = task.propose_prompt_wrap_writing_other(x, step, y, proposals_gpt_answer, '')
        evaluate_prompt_palm = task.propose_prompt_wrap_writing_other(x, step, y, proposals_palm_answer, '')
        gpt2gemini = gpt(evaluate_prompt_gemini, n=1, stop=None, temperature = tem)[0]
        confidence_gemini.append(extract_confidence(gpt2gemini))
        gpt2palm = gpt(evaluate_prompt_palm, n=1, stop=None, temperature = tem)[0]
        print('gpt2palm', evaluate_prompt_palm + gpt2palm)
        confidence_palm.append(extract_confidence(gpt2palm))
        time.sleep(5)
        gemini2gpt = gemini(evaluate_prompt_gpt)
        confidence_gpt.append(extract_confidence(gemini2gpt))
        time.sleep(5)
        gemini2palm = gemini(evaluate_prompt_palm)
        confidence_palm.append(extract_confidence(gemini2palm))
        time.sleep(5)
        palm2gpt = palm2(evaluate_prompt_gpt)
        confidence_gpt.append(extract_confidence(palm2gpt))
        time.sleep(5)
        palm2gemini = palm2(evaluate_prompt_gemini)
        confidence_gemini.append(extract_confidence(palm2gemini))
        #prin
        #print(proposals)
        #prin
        
        max_confidence = max(sum(confidence_gemini) / 3, sum(confidence_gpt) / 3, sum(confidence_palm) / 3)
        print('(confidence_gemini)', confidence_gemini)
        print('(confidence_gpt)', confidence_gpt)
        print('(confidence_palm)', confidence_palm)
        print('max_confidence', max_confidence)
        if max_confidence == sum(confidence_gpt) / 3:
            proposal = proposals[0]
        elif max_confidence == sum(confidence_gemini) / 3:
            proposal = proposals[1]
        else:
            proposal = proposals[2]
        if max_confidence <= 3.5:
            flag = 1
        else:
            flag = 0
    elif step == 1:
        tem = 0.1
        gpt = partial(gpt, model='gpt-3.5-turbo')
        propose_prompt = task.propose_prompt_wrap_writing(x, step, y)
        #print(propose_prompt)
        confidence_gpt = []
        confidence_gemini = []
        confidence_palm = []
        proposals = []
        proposals_gpt_raw = gpt(propose_prompt, n=1, stop=None)[0].split('Passage:')[-1].strip()
        proposals_gpt_passage = proposals_gpt_raw.split('Confidence')[0]
        confidence_gpt.append(extract_confidence(proposals_gpt_raw))
        proposals.append(proposals_gpt_passage)    
        print('proposals_gpt_raw:', proposals_gpt_raw)

        time.sleep(5)
        proposals_gemini_raw = gemini(propose_prompt).split('Passage:')[-1].strip()
        proposals_gemini_passage = proposals_gemini_raw.split('Confidence')[0]
        confidence_gemini.append(extract_confidence(proposals_gemini_raw))
        proposals.append(proposals_gemini_passage)
        print('proposals_gemini_raw:', proposals_gemini_raw) 

        time.sleep(5)
        proposals_palm_raw = palm2(propose_prompt).split('Passage:')[-1].strip()
        proposals_palm_passage = proposals_palm_raw.split('Confidence')[0]
        confidence_palm.append(extract_confidence(proposals_palm_raw))
        proposals.append(proposals_palm_passage)
        print('proposals_palm_raw:', proposals_palm_raw)       

        evaluate_prompt_gpt = task.propose_prompt_wrap_writing_other(x, step, y=y, passage=proposals_gpt_passage)
        evaluate_prompt_gemini = task.propose_prompt_wrap_writing_other(x, step, y=y, passage=proposals_gemini_passage)
        evaluate_prompt_palm = task.propose_prompt_wrap_writing_other(x, step, y=y, passage=proposals_palm_passage)
        gpt2gemini = gpt(evaluate_prompt_gemini, n=1, stop=None, temperature = tem)[0]
        confidence_gemini.append(extract_confidence(gpt2gemini))
        gpt2palm = gpt(evaluate_prompt_palm, n=1, stop=None, temperature = tem)[0]
        confidence_palm.append(extract_confidence(gpt2palm))
        time.sleep(5)
        gemini2gpt = gemini(evaluate_prompt_gpt)
        confidence_gpt.append(extract_confidence(gemini2gpt))
        time.sleep(5)
        gemini2palm = gemini(evaluate_prompt_palm)
        confidence_palm.append(extract_confidence(gemini2palm))
        time.sleep(5)
        palm2gpt = palm2(evaluate_prompt_gpt)
        confidence_gpt.append(extract_confidence(palm2gpt))
        time.sleep(5)
        palm2gemini = palm2(evaluate_prompt_gemini)
        confidence_gemini.append(extract_confidence(palm2gemini))

        max_confidence = max(sum(confidence_gemini) / 3, sum(confidence_gpt) / 3, sum(confidence_palm) / 3)
        print('(confidence_gemini)', confidence_gemini)
        print('(confidence_gpt)', confidence_gpt)
        print('(confidence_palm)', confidence_palm)
        print('max_confidence', max_confidence)
        if max_confidence == sum(confidence_gpt) / 3:
            proposal = proposals[0]
        elif max_confidence == sum(confidence_gemini) / 3:
            proposal = proposals[1]
        else:
            proposal = proposals[2]
        if max_confidence <= 3.5:
            flag = 1
        else:
            flag = 0
    return proposal, propose_prompt, flag

def solve(args, task, idx, to_print=True):
    global gpt
    gpt = partial(gpt, model=args.backend, temperature=args.temperature)
    print(gpt)
    x = task.get_input(idx)  # input
    #ys = ['']  # current output candidates
    infos = []
    y = ''
    for step in range(task.steps): 
        if args.method_generate == 'writing':
            new, prompt, flag = get_proposals_writing(task, x, y, mixed=args.mixed, step=step)
            new_ys = new

        new_ys_1 = new_ys
        if flag and step == 0:
            new_ys = get_values_writing(task, x, new_ys, args.n_evaluate_sample, args.mixed, step)
        elif flag and step == 1:
            new_ys = get_values_writing(task, x, ys_1, args.n_evaluate_sample, args.mixed, step)
        print('new_ys', new_ys)

        infos.append({'step': step, 'x': x, 'prompt': prompt, 'new_ys_1':new_ys_1, 'y': y, 'new_ys': new_ys})
        y = new_ys
        if step == 0:
            ys_1 = new_ys
    if to_print:
        pass 
        #print(ys)
    return y, {'steps': infos}, ys_1

