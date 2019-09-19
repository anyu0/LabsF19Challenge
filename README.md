ADI Labs F'19 Technical Challenge
===================

Angela Wang
aw3062

## About 
This flask app will fetch information from [Density](https://density.adicu.com) and display them on a web page.

## Preparation
- obtain a token from this [link](https://density.adicu.com/auth)
- go to `app.py` and change the value of `TOKEN` into your API key
- `flask run`

## Usage
- `localhost:5000/information/<building>` displays how full the building is
- `localhost:5000/information/<rank>` displays the least crowded places upto rank
