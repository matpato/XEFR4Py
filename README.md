<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div style="display: flex; align-items: center;">
    <div style="flex: 1;">
        <a href="https://isel.pt" target="_blank">
            <img src="https://www.isel.pt/sites/default/files/SCI/Identidade/logo_ISEL_simplificado_cor.png" alt="ISEL logo" style="width: 240px; height: auto;">
        </a>
    </div>
    <div style="flex: 3; text-align: left; padding-left: 20px;">
        <h3>eXplainable Ensemble Feature Ranking</h3>
    </div>
</div>



<!-- TABLE OF CONTENTS -->
<details>
    <summary>Table of Contents</summary>
    <ol>
    <li>
        <a href="#about-the-project">About The Project</a>
        <ul>
            <li><a href="#built-with">Built With</a></li>
        </ul>
    </li>
    <li>
        <a href="#getting-started">Getting Started</a>
        <ul>
            <li><a href="#Prerequisites">Prerequisites</a></li>
            <li><a href="#Installation">Installation</a></li>
        </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact-and-acknowledgements">Contact and Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[//]: # (<img src="images/screenshot.png" alt="Logo">)

This project presents an enhanced version of the Ensemble Feature Ranking algorithm, Enhanced Ensemble Feature Ranking
(EEFR) , tailored to optimize feature selection in machine learning models. It proposes the use of an interactive 
dashboard application, as part of learning environment, designed to provide users with a visually intuitive platform 
for exploring the algorithm’s internal metrics and rankings.

The algorithm is based on the monte Carlo and the ensemble of multiple feature selection metrics, which are combined to 
produce a feature ranking that is more robust and reliable than any individual metrics. The algorithm is designed to be 
flexible and configurable, allowing users to select the desired feature selection  metrics to be used in the ensemble. 
Being based on the Monte Carlo means that it uses a random sampling of the data to apply the metrics. As it uses subsets,
we can configure the number of sets and the size of each set, which allows the user to control the computational cost of
the algorithm. The EEFR let users choose the class and blacklist of features (by labels) and the number of features to 
be selected, or iven to auto select the number of features of the final ranking.

The dashboard facilitates a deeper understanding of feature importance and algorithm behaviour, bridging the gap between
complex algorithms and user comprehension. By combining advanced algorithmic techniques with a user-centric interface, 
our approach promotes transparency, accountability and increased user engagement in the explanation of machine learning 
models. To be able to use the dashboard, the algorithm must be run with the logs enabled.

<!-- TODO insert project description here -->
<p >(<a href="#top">back to top</a>)</p>



### Built With

This app was developed using these frameworks:

* [Python 3.10](https://www.python.org/)
* [Pandas](https://pandas.pydata.org/)
* [Numpy](https://numpy.org/)
* [Scipy](https://scipy.org/)
* [Scikit learn](https://www.rabbitmq.com/)

The dashboard was developed using these frameworks:
* [Py QT 5](https://www.qt.io/)
* [MatplotLib](https://matplotlib.org/)

<p>(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

The library was developed for the Python 3.10 (it is not guaranteed that it works with other versions).
The dashboard can only be used if the algorithm was the logs enabled, otherwise it doesn't start.

#### Prerequisites

* Install Python 3.10 (Compatibility with other versions is not guaranteed)
* Install Pandas (The library uses Pandas DataFrame as input)

#### Installation # TODO to be done

After having installed Python 3.10 you can install the library. It's recommended to use virtual environments to ensure 
that there are no compatibility problems with the library. If you don't want to generate the virtual environment or your 
IDE manage that, you can jump to step 3.  

1. Generate virtual environment:
```shell
python3 -m venv path\to\env
```
2. To activate the virtual environment on Windows, execute the command given below:
```shell
path\to\env\Scripts\activate.bat
```
To activate the virtual environment on Unix or macOS, execute the command given below:
```shell
source path/to/env/bin/activate
```

3. Install the library and pandas via pip:
```shell
pip install eefr pandas
```


<p>(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Code snippet to test the library and dashboard:

```python
from pandas import DataFrame
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
```

<p>(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p>(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact and Acknowledgements

This project was developed as a master thesis of Lisbon School of Engineering (ISEL)

Diogo Amorim - A47248@alunos.isel.pt</br>
Matilde Pós-de-Mina Pato - matilde.pato@isel.pt</br>
Nuno Datia - nuno.datia@isel.pt</br>

Project Link: [https://github.com/matpato/XEFR4Py](https://github.com/matpato/XEFR4Py)

</br>To cite the work, please use the following text:</br>
Amorim, D.; Pato, M. & Datia, N.</br>
XEFR: eXplainable Ensemble Feature Ranking </br>


<p>(<a href="#top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew

[//]: # ([product-screenshot]: images/screenshot.png)