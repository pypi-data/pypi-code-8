




def runme(tag=1, N=125000):
    import scoring
    s = scoring.HPNScoringPrediction('/home/cokelaer/.config/dreamtools/dream8/D8C1/submissions/sc2a/StuartLab-Prediction.zip')
    res = s.get_null(N=N)
    import pickle
    fh = open('res%s.pkl' % str(tag), 'w')
    pickle.dump(res, fh)
    fh.close()

def aggregate_and_save(filenames):

    results = []
    for filename in filenames:
        import pickle
        l = pickle.load(open(filename, 'r'))
        results.extend(l)


    BT20 = [x['BT20'] for x in results]
    BT549 = [x['B549'] for x in results]
    MCF7 = [x['MCF7'] for x in results]
    UACC812 = [x['UACC812'] for x in results]

    import json

    fh = open('BT20.json', 'w')
    json.dump(fh, BT20)
    fh.close()

    fh = open('UACC812.json', 'w')
    json.dump(fh, UACC812)
    fh.close()

    fh = open('MCF7.json', 'w')
    json.dump(fh,MCF7)
    fh.close()

    fh = open('BT549.json', 'w')
    json.dump(fh, BT549)
    fh.close()

    return results




