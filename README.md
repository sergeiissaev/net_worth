<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
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
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Net Worth Calculator and Tracking Tool</h3>

  <p align="center">
    A free, open source tool to track your live net worth by multiplying your assets by their respective market values.
    <br />
    <a href="https://github.com/sergeiissaev/net_worth/issues">Report Bug</a>
    ·
    <a href="https://github.com/sergeiissaev/net_worth/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

A free, open-source tool to track your net worth at any moment and across time. No more signing in separately and checking various brokerages,
exchanges, etc. Now, you can easily and reliably track and visualize your complete net worth at any moment.

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started

To get a copy of the tool follow these steps.


### Installation

1. Install Anaconda from  [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution) if you do not have a Python installed already.
2. Clone the repo
   ```sh
   git clone https://github.com/sergeiissaev/net_worth.git
   ```
3. Navigate to the project root using a shell (terminal on Mac or command prompt on Windows). Create a virtual environment using
   ```sh
   conda env create --name net_worth --file envs/environment.yml
   ```
4. Activate your environment with
   ```sh
   conda activate net_worth
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After you have navigated to the root directory, run the following command:

```sh
python src/scripts/find_net_worth.py
```

The asset data is read from the ```data/money``` folder. For demonstration purposes, there are three .csv files to start.
1. ```data/money/tfsa.csv```, which contains 10 shares of MSFT stock, 10 shares of AAPL, and 100 shares of XIU.TO.


2. ```data/money/chequing_account.csv```, which contains $2000 in cash.


3. ```data/money/rrsp.csv```, which contains 10 shares of GSY stock, 10 shares of HXQ.TO, and 100 shares of BRK-B.
When you run the program initially, these data files will be used to calculate a net worth.

If you open those files, you will notice the first column contains a column name "type". This is used to determine whether to multiply
this asset by its live price, or whether the price is static:

* Type 1 = live values. These numbers will be multiplied by the live price using the Yahoo Finance API. Examples include stocks, crypto, etc.


* Type 2 = static value. These numbers are constants and will not be multiplied by the live price. Examples include cash, car value, collectibles, etc.

Once you are ready to add your own assets, delete these data files, along with the file at ```data/net_worth_history/net_worth_history.csv``` (this file will only be there if you ran the code).

To input your own assets, create a new .csv file in the ```data/money``` folder. The name of the file will be used as the name of the asset for graphing purposes.

There should be two rows in each .csv file. The first row should contain the column names, and the second should contain the values.

The first column should be "type" (with a value of 1 or 2, as explained above), and the columns to the right should have a column name of the asset. If this file is type 1, the name should be the ticker for that asset as it appears on [Yahoo Finance](https://ca.finance.yahoo.com/).
If the asset is of type 2, the name does not matter, other than that it will appear in the report with that name. The value column should contain the number of shares (or crypto coins) for type 1, or the cash value of the asset for type 2.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



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

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE.md -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sergei Issaev - sergei740@gmail.com

Project Link: [https://github.com/sergeiissaev/net_worth](https://github.com/sergeiissaev/net_worth)

<p align="right">(<a href="#readme-top">back to top</a>)</p>







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sergeiissaev/net_worth.svg?style=for-the-badge
[contributors-url]: https://github.com/sergeiissaev/net_worth/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sergeiissaev/net_worth.svg?style=for-the-badge
[forks-url]: https://github.com/sergeiissaev/net_worth/network/members
[stars-shield]: https://img.shields.io/github/stars/sergeiissaev/net_worth.svg?style=for-the-badge
[stars-url]: https://github.com/sergeiissaev/net_worth/stargazers
[issues-shield]: https://img.shields.io/github/issues/sergeiissaev/net_worth.svg?style=for-the-badge
[issues-url]: https://github.com/sergeiissaev/net_worth/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/sergeiissaev/net_worth/blob/master/LICENSE.md
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sergei-issaev
[product-screenshot]: data/processed/net_worth_line_graph.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
