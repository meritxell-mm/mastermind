# Mastermind
API for mastermind game


## Set environment
```bash
docker-compose up
``` 

## APIs

### New game - POST /mastermind/start/:
#####Request:
```bash
curl --request POST  --url http://localhost:8000/mastermind/start/ 
```
#####Answer:
```json
{"pk":1}
```

### Guess code - POST /mastermind/guess/:
#####Request:
Expects an object in the request's body with the following information:

* game_id (int): The game's ID that this guess is for<br>
* code_guess (string list): The user's code guess

```bash
curl --request POST --url http://localhost:8000/mastermind/guess/ \
       --data 'game_id=1&code_guess=RED&code_guess=GREEN&code_guess=RED&code_guess=YELLOW'
```

#####Possible answers:
* "1 black, 1 white"
* "Congratulations! YOU WON!!!"
* "Game already won"
* "GAME OVER"


### See game historic - GET /mastermind/historic/<game_id>/:
#####Request:
```bash
curl --request GET --url http://localhost:8000/mastermind/historic/1/
```

#####Answer:
```
[
    {
        "id": 1,
        "code_guess": [
            "RED",
            "GREEN",
            "RED",
            "YELLOW"
        ],
        "create_date": "2019-04-07T20:09:52.219005Z",
        "black_pegs": 0,
        "white_pegs": 1,
        "game": 2
    }
]
```