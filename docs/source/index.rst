Welcome to XEFR4Py's documentation!
===================================

XEFR4Py is a Python implementation of the algorithm EFR designed by Vitor. This algorithm implements a Ensemble Feature
Ranking for big data.  This implementation is based in the original algorithm but adds some functionalities like
class selection and black list of features.

It also have a dashboard to provide explainability to the algorithm. The dashboard can be used after the execution of
the algorithm with the logs enable. The logs are used to generate the diagrams and tables in the dashboard.

The algorithm itself is present in the module xefr4py in the class EEFR.
The following code snippet shows how to use the algorithm:

.. code-block:: Python

    import pandas as pd
    from xefr4py.knowledge_viewer import launch_dashboard
    from xefr4py import Metric, EEFR

    if __name__ == '__main__':
        dataset: DataFrame = pd.read_csv(
            'https://raw.githubusercontent.com/matpato/XEFR4Py/main/data/allDataArceneTrain.txt',
            sep=' ')  # update this link
        features: list[str] = EEFR(dataset).ensemble_features_ranking(metrics=[Metric.CHI_SQUARED])
        print(features)     # output should be like: ['F.7888', 'F.7564', 'F.3986', 'F.8051', 'F.158', 'F.1455', ...]

        launch_dashboard()  # launch the dashboard

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
