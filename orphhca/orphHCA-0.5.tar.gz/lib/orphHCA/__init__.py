__version__ = "0.5"
__release__ = __version__  + '-dev' # comment out '-dev' before a release

import traceback, inspect
import sys
import OrphHCA

def orphHCA_main():
    params = OrphHCA.process_parameters()
    ret = OrphHCA.orphHCA_main(params.inputmsa, params.workdir, params.output,
        hmmdb=params.hmmdatabase, keepfasta=params.keepfasta,
        verbose=params.verbose, seqdb=params.seqdb, cores=params.cores,
        cut_hca=params.cut_hca, nbover_hca=params.nbover_hca, 
        cut_dom=params.cut_dom, nbover_dom=params.nbover_dom, 
        hca_size=params.hca_size, cut_hmm=params.cut_hmm,
        nbover_hmm=params.nbover_hmm)
    return ret

if __name__ == "__main__":
    """
    Catching malfunctionning behavior
    """
    try:
        ext = orphHCA_main()
    except SystemExit as e :
        ext = e.code
    except:
        print "Unexpected error:", sys.exc_info()[0]
        traceback.print_exc()
        ext = 1
    finally:
        sys.exit(ext)


