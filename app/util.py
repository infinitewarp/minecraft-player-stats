from collections import defaultdict


# borrowed from https://gist.github.com/hrldcpr/2012250
def tree():
    return defaultdict(tree)
