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
    YOUR_HF_TOKEN = ''
    return YOUR_HF_TOKEN


# for adding small numbers (1-6 digits) and large numbers (7 digits), write prompt prefix and prompt suffix separately.
def your_prompt():
    """Returns a prompt to add to "[PREFIX]a+b[SUFFIX]", where a,b are integers
    Returns:
        A string.
    Example: a=1111, b=2222, prefix='Input: ', suffix='\nOutput: '
    """
    prefix = '''
Output only the sum as digits with no explanation.
Answer the question with only the final result followed by newline.
Don't give explanation of the answer.
Rule: If a digit-sum is 10 or more, add 1 to the next digit.
Question: 5365917+6824171
Answer: 12190088
Explanation: 7+1=8, 1+7=8, 9+1=10 write 0 carry 1, 5+4+1=10 write 0 carry 1, 6+2+1=9 write 9, 3+8=11 write 1 carry 1, 5+6+1=12 write 2 carry 1
Question: 1234567+1234567
Answer: 2469134
Question: 7266426+4758649
Answer: 12025075
Question: 1849658+9146618
Answer: 10996276
Question: 3875741+6338672
Answer: 10214413
Question: 9753833+7241623
Answer: 16995456
Question: 7767518+5928584
Answer: 13696102
Question: 1253531+3835776
Answer: 5089307
Question: 1692838+7331945
Answer: 9024783
Question: 7261695+7241742
Answer: 14503437
Question: 9934556+5998961
Answer: 15933517
Question: 3984499+8223118
Answer: 12207617
Question: 1728224+5137592
Answer: 6865816
Question: 4412487+5946863
Answer: 10359350
Question:
'''

    suffix = '\nAnswer: '

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
        'temperature': 0.09,
        'top_k': 0,
        'top_p': 1,
        'repetition_penalty': 1.09,
        'stop': ["Example", "\n\n"]}
    
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
    longest_num = None
    for ans in all_ans:
        valid_ans = re.sub(r"\D", "", ans)
        if longest_num is None or len(valid_ans) > len(longest_num):
            longest_num = valid_ans
        if len(valid_ans) >= 7 and len(valid_ans) <= 9:
            try:
                value = int(valid_ans)
                if 1000000 <= value <= 999999999:
                    nums.append(value)
            except:
                continue
    if nums:
        return nums[-1]
    if longest_num and 6 <= len(longest_num) <= 9:
        return int(longest_num)
    return 0