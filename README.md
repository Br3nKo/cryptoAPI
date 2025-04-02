# A simple app to track your crypto portfolio
## install & run 
- `docker-compose up -d`

- backend URL:
  - `localhost:8000/docs`
- frontend URL:
  - `localhost:3000`

## Description
### Add coin:
- Use coin symbol and name and the application retrieves all the data from COinGecko
- example, `symbol: btc` & `name: bitcoin`
### Update Coin: 
- Use coin id to update specific coin
- this was not thought through in the frontend as you can´t see ID in the table - will fix later
### Delete Coin:
- same as above
### Disclaimer
The frontend is yet to be fully implemented, therefore use backend Openapi to call the API requests

## What to improve / implement
### Backend:
- error handling (add error codes and messages)
- auth
### Frontend:
- everything :)
- had no time to implement, will certainly do later
