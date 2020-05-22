import json
import time

with open("dep_probs_lemm_filtered.json") as file:
    PROB_TABLE = json.load(file)

sequences = [("plan", "attack"), ("make", "travel", "bomb"), ("plan", "bomb")]
max_d = 4 # max separation between events

def ps(sequence, max_distance):
    curr = sequence[0]
    return ps_helper(curr, sequence[1:], max_distance, ([curr], 1.))

def ps_helper(curr, rest, max_distance, acc):
    ps_helper.counter += 1
    
    if not rest:
        return acc
    
    if max_distance == 0:
        return []

    target = rest[0]
    
    # next_steps = PROB_TABLE.get(curr)
    # for n in next_steps:
    #     nn_steps = PROB_TABLE.get(n)

        



    next_steps = PROB_TABLE.get(curr, [])
    for test in next_steps:
        temp = (acc[0]+[test], acc[1]*PROB_TABLE[curr][test])
        best = temp
        if test == target:
            return ps_helper(test, rest[1:], max_distance, best)
        if not ps_helper(test, rest, max_distance-1, best):
            continue

    return acc

ps_helper.counter = 0
# def stop_criteria(test, target):
#     if test == target:
#         return True
#     return False

start = time.time()
print(ps(sequences[0], max_d))
print(f"Function called {ps_helper.counter} times.")
print(time.time() - start)
  
# print(ps(sequences[2], max_d))

# print(PROB_TABLE["plan"])
# best_prob = 0.0
# best = ""
# for event in PROB_TABLE["plan"]:
#     if event in PROB_TABLE:
#         for ee in PROB_TABLE[event]:
#             if ee == "bomb":
#                 if PROB_TABLE["plan"][event]*PROB_TABLE[event]["bomb"] > best_prob:
#                     best_prob = PROB_TABLE["plan"][event]*PROB_TABLE[event]["bomb"]
#                     best = (event, ee)
# print(best, best_prob)
    # print(PROB_TABLE["plan"][""])