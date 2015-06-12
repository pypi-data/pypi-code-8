from pyhacrf import StringPairFeatureExtractor, Hacrf
import numpy as np


# Run with: python -m cProfile temp_profile.py
# or copy to pyhacrf.py, decorate function of interest with @profile, and run with kernprof
def test_fit_predict_regularized():
    incorrect = ['helloooo', 'freshh', 'ffb', 'h0me', 'wonderin', 'relaionship', 'hubby', 'krazii', 'mite', 'tropic']
    correct = ['hello', 'fresh', 'facebook', 'home', 'wondering', 'relationship', 'husband', 'crazy', 'might', 'topic']
    training = zip(incorrect, correct)

    fe = StringPairFeatureExtractor(match=True, numeric=True)
    xf = fe.fit_transform(training)

    model = Hacrf(l2_regularization=10.0)
    model.fit(xf, [0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    expected_parameters = np.array([[-0.0569188, 0.07413339, 0.],
                                    [0.00187709, -0.06377866, 0.],
                                    [-0.01908823, 0.00586189, 0.],
                                    [0.01721114, -0.00636556, 0.],
                                    [0.01578279, 0.0078614, 0.],
                                    [-0.0139057, -0.00862948, 0.],
                                    [-0.00623241, 0.02937325, 0.],
                                    [0.00810951, -0.01774676, 0.]])

    from numpy.testing import assert_array_almost_equal
    assert_array_almost_equal(model.parameters, expected_parameters)

    expected_probas = np.array([[0.5227226, 0.4772774],
                                [0.52568993, 0.47431007],
                                [0.4547091, 0.5452909],
                                [0.51179222, 0.48820778],
                                [0.46347576, 0.53652424],
                                [0.45710098, 0.54289902],
                                [0.46159657, 0.53840343],
                                [0.42997978, 0.57002022],
                                [0.47419724, 0.52580276],
                                [0.50797852, 0.49202148]])
    actual_predict_probas = model.predict_proba(xf)
    assert_array_almost_equal(actual_predict_probas, expected_probas)

    expected_predictions = np.array([0, 0, 1, 0, 1, 1, 1, 1, 1, 0])
    actual_predictions = model.predict(xf)
    assert_array_almost_equal(actual_predictions, expected_predictions)

test_fit_predict_regularized()
