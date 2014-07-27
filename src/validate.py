import argparse

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(
            description='Script recognition predictor.')
    parser.add_argument('-p', '--prediction_file', type=str, default='.', help='predictions file')
    args = parser.parse_args()

    with open(args.prediction_file, 'r') as f:
        for line in f:
            parts = line.split(',')
            actual = parts[0].split('-')[1].split('.')[0]
            prediction = parts[1].strip()
            if actual != prediction:
                print '%s,%s' % (parts[0], parts[1].strip())
