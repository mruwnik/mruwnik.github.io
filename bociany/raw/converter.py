import json
from pathlib import Path
from itertools import groupby


def extract_vals(line):
    diam, h, compr, _, __, avg, bottom, top = line.strip().split()
    return (int(diam), int(h), compr), (float(bottom), float(avg), float(top))


def file_vals(filename):
    with open(filename) as f:
        return dict(map(extract_vals, f))


def add_top_bottom(current, vals):
    if not current:
        return list(vals)

    bottom, avg, top = vals
    return [bottom] + current + [top]


def interval_values(key, intervals_map, model, intervals, m_type):
    current = list(intervals_map[(model, str(intervals[0]), m_type)][key])
    for interval in intervals[1:]:
        bottom, avg, top = intervals_map[(model, str(interval), m_type)][key]
        current = [bottom] + current + [top]
    return current


def all_values(height, diam, models_values, models, m_type):
    weights = [0.478365, 0.353365, 0.168269]
    values = [
        interval_values((diam, height, m_type), models_values, model, intervals, m_type)
        for model, intervals in models.items()
    ]
    avgs = [
        sum(map(lambda v: v[0] * v[1], zip(vals, weights)))
        for vals in zip(*values)
    ]
    return values + [avgs]


def model_vals():
    models_values = {
        tuple(filename.name.replace('_', '.').split('.')[:-1]): file_vals(filename) for filename in Path().glob('*.txt')
    }
    models = {
        model: sorted(int(i[1]) for i in intervals)
        for model, intervals in groupby(sorted(models_values.keys(), key=lambda x: x[0]), key=lambda x: x[0])
    }

    return {
        t: {
            diam: {
                height: all_values(height, diam, models_values, models, m_type)
                for height in range(10, 140)
            } for diam in range(80, 230)
        } for t, m_type in enumerate(['normal', 'dense'], 1)
    }


if __name__ == '__main__':
    with open('../weights.js', 'w') as f:
        f.write('weights = ' + json.dumps(model_vals()) + ';')
