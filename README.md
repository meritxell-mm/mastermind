# Mastermind
API for mastermind game


## Set environment
```bash
docker-compose up
``` 

## APIs

### New game - POST /game/api/new/:
#####Request:
```bash
curl --request POST  --url http://localhost:8000/game/api/new/ 
```
#####Answer:
```json
{"pk":1}
```

### Guess code - POST /game/api/guess/:
#####Request:
Expects an object in the request's body with the following information:

* game_id (int): The game's ID that this guess is for<br>
* code_guess (string list): The user's code guess

```bash
curl --request POST --url http://localhost:8000/game/api/guess/ \
       --data 'game_id=1&code_guess=RED&code_guess=GREEN&code_guess=RED&code_guess=YELLOW'
```

#####Possible answers:
* "1 black, 1 white"
* "Congratulations! YOU WON!!!"
* "Game already won"
* "GAME OVER"


### See game historic - GET /game/api/historic/<game_id>/:
#####Request:
```bash
curl --request GET --url http://localhost:8000/game/api/historic/1/
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