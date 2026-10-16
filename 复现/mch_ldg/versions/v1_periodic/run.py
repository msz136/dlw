import argparse,json
from mch.experiment import run
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--output',default='results')
    args=ap.parse_args();run(json.load(open(args.config,encoding='utf-8')),args.output)
