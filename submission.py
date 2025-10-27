import json
import collections
import argparse
import random
import numpy as np
import requests
import re

def your_netid():
    YOUR_NET_ID = 'xs2682'
    return YOUR_NET_ID

def your_hf_token():
    YOUR_HF_TOKEN = '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'
    return YOUR_HF_TOKEN


# for adding small numbers (1-6 digits) and large numbers (7 digits), write prompt prefix and prompt suffix separately.
def your_prompt():
    """Returns a prompt to add to "[PREFIX]a+b[SUFFIX]", where a,b are integers
    Returns:
        A string.
    Example: a=1111, b=2222, prefix='Input: ', suffix='\nOutput: '
    """
    prefix = '''You're a calculator.
Answer the question with final result only followed by a new line.
Output the sum with digits only, no spaces, commas, or text.
Give no explanation of the answer.
Follow these rules strictly: Add digits from right to left. If a digit-sum is 10 or more, add 1 to the next digit.
Question: what is 5365917+4824171
Explanation: Right to left: 7+1=8, 1+7=8, 9+1=10 write 0 carry 1, 5+4+1=10 write 0 carry 1, 6+2+1=9 write 9, 3+8=11 write, 5+4+1=10 write 0 carry 1
Answer: 10190088
Question: what is 1234567+1234567?
Answer: 2469134
Question: what is 8716638+1302271?
Answer: 10018909
Question: what is 3697407+4804185?
Answer: 8501592
Question: what is 3726518+2184739?
Answer: 5911257
Question: what is 9451203+7082416?
Answer: 16533619
Question: what is 6041295+3786427?
Answer: 9827722
Question: what is 1035947+8962178?
Answer: 9998125
Question: what is '''

    suffix = '?\nAnswer: '

    return prefix, suffix


def your_config():
    """Returns a config for prompting api
    Returns:
        For both short/medium, long: a dictionary with fixed string keys.
    Note:
        do not add additional keys. 
        The autograder will check whether additional keys are present.
        Adding additional keys will result in error.
    """
    config = {
        'max_tokens': 90, # max_tokens must be >= 50 because we don't always have prior on output length 
        'temperature': 0.01,
        'top_k': 20,
        'top_p': 0.5,
        'repetition_penalty': 1,
        'stop': ["Example", "\n\n\n"]}
    
    return config


def your_pre_processing(s):
    return s

def your_post_processing(output_string):
    """Returns the post processing function to extract the answer for addition
    Returns:
        For: the function returns extracted result
    Note:
        do not attempt to "hack" the post processing function
        by extracting the two given numbers and adding them.
        the autograder will check whether the post processing function contains arithmetic additiona and the graders might also manually check.
    """

    s = output_string.strip()
    all_ans = re.findall(r'\b[0-9,]+\b', s)
    nums = []
    for ans in all_ans:
        valid_ans = re.sub(r"\D", "", ans)
        if 7 <= len(valid_ans) <= 8:
            try:
                value = int(valid_ans)
                if 1_000_000 <= value <= 19_999_999:
                    nums.append(value)
            except:
                continue
    if nums:
        return nums[-1]
    return 0