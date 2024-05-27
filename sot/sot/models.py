import os
import openai
import backoff 
import google.generativeai as palm
import google.generativeai as genai 
api_key = os.getenv("GOOGLE_PALM_API_KEY", "")
genai.configure(api_key=api_key) 
palm.configure(api_key=api_key)	
generation_config = { 
    "temperature": 0.1, 
    "top_p": 1, 
    "top_k": 1, 
    "max_output_tokens": 1000, 
} 
model = genai.GenerativeModel(model_name="gemini-1.0-pro-latest", generation_config=generation_config) 
completion_tokens_gpt_4 = prompt_tokens_gpt_4 = completion_tokens_gpt_3_5 = prompt_tokens_gpt_3_5 = 0

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key != "":
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY is not set")
    
api_base = os.getenv("OPENAI_API_BASE", "")
if api_base != "":
    print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
    openai.api_base = api_base

@backoff.on_exception(backoff.expo, openai.error.OpenAIError)
def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

#def gpt_multi(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    #messages = prompt
    #return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)

def gemini(prompt) -> str:
    response_gemini_init = model.generate_content(prompt)
        #if response_gemini_init.parts:
    try:
        proposals_gemini_raw = response_gemini_init.text
    except ValueError as e:
        if response_gemini_init.parts:
            proposals_gemini_raw = str(response_gemini_init.parts[0]).replace('\\n', '\n')
        else:
            proposals_gemini_raw = 'Failed'

    return proposals_gemini_raw

def palm2(prompt) -> str:
    response_palm_init = palm.generate_text(prompt=prompt)
    if isinstance(response_palm_init.result, str):
        return response_palm_init.result
    else:
        return 'Failed'

def gpt(prompt, model="gpt-4", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    if type(prompt) == list:
        messages = prompt
    else:
        messages = [{"role": "user", "content": prompt}]
    return chatgpt(messages, model=model, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    
def chatgpt(messages, model="gpt-4", temperature=0.1, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens_gpt_4, prompt_tokens_gpt_4, completion_tokens_gpt_3_5, prompt_tokens_gpt_3_5
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        res = completions_with_backoff(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        outputs.extend([choice["message"]["content"] for choice in res["choices"]])
        # log completion tokens
        if model == 'gpt-4':
            completion_tokens_gpt_4 += res["usage"]["completion_tokens"]
            prompt_tokens_gpt_4 += res["usage"]["prompt_tokens"]
        elif model == 'gpt-3.5-turbo':
            completion_tokens_gpt_3_5 += res["usage"]["completion_tokens"]
            prompt_tokens_gpt_3_5 += res["usage"]["prompt_tokens"]
        else:
            raise ValueError(f'model {model} not recognized')
        #print(max_tokens)
        #print(cnt)
        #print(stop)
        #print(temperature)
        #print(messages)
        #print(f"\n\n\n{res}")
    return outputs
    
def gpt_usage(backend="gpt-4", mixed=0):
    global completion_tokens_gpt_4, prompt_tokens_gpt_4, completion_tokens_gpt_3_5, prompt_tokens_gpt_3_5
    if backend == "gpt-4" and mixed == 0:
        cost = completion_tokens_gpt_3_5 / 1000 * 0.002 + prompt_tokens_gpt_3_5 / 1000 * 0.0015 + completion_tokens_gpt_4 / 1000 * 0.06 + prompt_tokens_gpt_4 / 1000 * 0.03
    elif backend == "gpt-3.5-turbo" and mixed == 0:
        cost = completion_tokens_gpt_3_5 / 1000 * 0.002 + prompt_tokens_gpt_3_5 / 1000 * 0.0015 + completion_tokens_gpt_4 / 1000 * 0.06 + prompt_tokens_gpt_4 / 1000 * 0.03
    elif backend == "gpt-4-1106-preview" and mixed == 0:
        cost = completion_tokens_gpt_4 / 1000 * 0.03 + prompt_tokens_gpt_4 / 1000 * 0.01
    elif mixed == 1 and backend == "gpt-4":
        cost = completion_tokens_gpt_3_5 / 1000 * 0.002 + prompt_tokens_gpt_3_5 / 1000 * 0.0015 + completion_tokens_gpt_4 / 1000 * 0.06 + prompt_tokens_gpt_4 / 1000 * 0.03
    elif mixed == 2 and backend == "gpt-3.5-turbo":
        cost = completion_tokens_gpt_3_5 / 1000 * 0.002 + prompt_tokens_gpt_3_5 / 1000 * 0.0015 + completion_tokens_gpt_4 / 1000 * 0.06 + prompt_tokens_gpt_4 / 1000 * 0.03
    else:
        cost = completion_tokens_gpt_3_5 / 1000 * 0.002 + prompt_tokens_gpt_3_5 / 1000 * 0.0015 + completion_tokens_gpt_4 / 1000 * 0.06 + prompt_tokens_gpt_4 / 1000 * 0.03
    return {"completion_tokens_gpt_3_5": completion_tokens_gpt_3_5, "prompt_tokens_gpt_3_5": prompt_tokens_gpt_3_5, "completion_tokens_gpt_4": completion_tokens_gpt_4, "prompt_tokens_gpt_4": prompt_tokens_gpt_4, "cost": cost}
