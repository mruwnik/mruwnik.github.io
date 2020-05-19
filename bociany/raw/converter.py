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


def interval_values(key, intervals_map, model, intervals):
    current = list(intervals_map[(model, str(intervals[0]))][key])
    for interval in intervals[1:]:
        bottom, avg, top = intervals_map[(model, str(interval))][key]
        current = [bottom] + current + [top]
    return current


def all_values(height, diam, models_values, models):
    return [
        interval_values((diam, height, 'normal'), models_values, model, intervals)
        for model, intervals in models.items()
    ]


def model_vals():
    models_values = {
        tuple(filename.name.split('.')[:-1]): file_vals(filename) for filename in Path().glob('*.txt')
    }
    models = {
        model: sorted(int(i[1]) for i in intervals)
        for model, intervals in groupby(sorted(models_values.keys(), key=lambda x: x[0]), key=lambda x: x[0])
    }

    return {
        1: {
            diam: {
                height: all_values(height, diam, models_values, models)
                for height in range(10, 140)
            } for diam in range(80, 230)
        }
    }


if __name__ == '__main__':
    with open('../weights.js', 'w') as f:
        f.write('weights = ' + json.dumps(model_vals()) + ';')
