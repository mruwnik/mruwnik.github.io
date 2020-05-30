import json
from collections import defaultdict
from itertools import groupby

TYPES = {'normal': 1, 'dense': 2}


def dict_keys(*dicts):
    keys = set()
    for d in dicts:
        keys = keys | d.keys()
    return keys


def extract_vals(line):
    d, h, type, _, _, w, low, high = line.split()
    return (int(d), int(h), TYPES[type]), (float(low), float(w), float(high))


def vals_dict(filename):
    with open(filename) as f:
        return dict(extract_vals(line) for line in f)


def size_weights(size, p80, p90, p95):
    p80_low, p80_avg, p80_high = p80.get(size) or (None, None, None)
    p90_low, p90_avg, p90_high = p90.get(size) or (None, None, None)
    p95_low, p95_avg, p95_high = p95.get(size) or (None, None, None)
    avg = p95_avg or p90_avg or p80_avg
    return (p95_low, p90_low, p80_low, avg, p80_high, p90_high, p95_high)


def weights(p80, p90, p95):
    keys = dict_keys(p80, p90, p95)
    return {key: size_weights(key, p80, p90, p95) for key in keys}


def avg_weights(m_weights, keys):
    weights = [0.478365, 0.353365, 0.168269]
    pp1, pp2, pp3 = m_weights
    return {
        key: [
            v1 * weights[0] + v2 * weights[1] + v3 * weights[2]
            for v1, v2, v3 in zip(pp1[key], pp2[key], pp3[key])
        ] for key in keys
    }


def model_weights(model, model_type):
    return weights(*[vals_dict(f'pp{model}.{pp}_{model_type}.txt') for pp in [80, 90, 95]])


def type_weights(models, model_type):
    m_weights = [model_weights(model, model_type) for model in models]
    keys = dict_keys(*m_weights)
    avgs = avg_weights(m_weights, keys)
    return {
        key: [d.get(key) for d in m_weights] + [avgs.get(key)]
        for key in keys
    }


def make_nested(items):
    weights = defaultdict(lambda: defaultdict(lambda: defaultdict()))
    for (d, h, t), values in items.items():
        weights[t][d][h] = values
    return weights


def save(models, output):
    data = type_weights(models, 'normal')
    data.update(type_weights(models, 'dense'))
    with open(output, 'w') as f:
        f.write('weights = ')
        json.dump(make_nested(data), f)
        f.write(';')
        return data


if __name__ == "__main__":
    save([1, 2, 3], '../weights.js')
