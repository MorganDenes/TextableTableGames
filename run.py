from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from LostCities import SetupGame, HandleMove, SwitchPlayer, CheckEndGame, PrintGame, Score, GetCur, GetOth
import os

app = Flask(__name__)

playerDir = \
{
        "RIC":os.environ["RIK_NUM"],
        "MOR":os.environ["MOR_NUM"],
        "SCO":os.environ["SCO_NUM"]
}

adminNumber = os.environ["MOR_NUM"]
playerNumbers = ["", ""]
currentNumber = ""
otherNumber = ""
account_sid = os.environ["TWILIO_ACCOUNT_SID"] 
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilioNumber = os.environ["TWI_NUM"]


def Send(body, current=None):
    if current is None:
        current = currentNumber
    print("Sending board to " + current)
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body= body,
            from_=twilioNumber,
            to= current
        )


def SendGame():
    Send(PrintGame())

def SendScores():
    player0 = Score(0)
    player1 = Score(1)
    format0 = "You scored: %i\nThey scored: %i"%(player0, player1)
    format1 = "You scored: %i\nThey scored: %i"%(player1, player0)
    Send(format0, currentNumber)
    Send(format1, otherNumber)

def ValidateTerms(t):
    return True

def GetPlayerNumbers(t):
    playerNumbers[0] = playerDir[t[1]] if t[1] in playerDir else t[1]
    playerNumbers[1] = playerDir[t[2]] if t[2] in playerDir else t[2]


def SetupNewGame(terms):
    global currentNumber, otherNumber, game
    SetupGame()
    GetPlayerNumbers(terms[:])
    print("Player numbers:", playerNumbers)
    currentNumber = playerNumbers[GetCur()]
    otherNumber = playerNumbers[GetOth()]
    game = True
    SendGame()


def AdminMode(command):
    print("In admin:", command)
    terms = command.upper().split('.')
    if ValidateTerms(terms):
        SetupNewGame(terms)



game = False 

@app.route("/twilio/sms", methods=['GET', 'POST'])
def LostCitiesPlay():  
    global currentNumber, otherNumber, game
    # resp = MessagingResponse()

    receiveNumber = request.values.get('From')
    receiveBody = request.values.get('Body')

    print("Recieved" + receiveNumber)
    print("Body:'%s'"%receiveBody)
    print("Expected number: " + currentNumber)
    if receiveNumber == adminNumber and 'ADMIN' in receiveBody.upper():
        AdminMode(receiveBody)
        return str()

    if not game:
        print('No ongoing game')
        return str()

    if receiveNumber != currentNumber:
        return str()

    if HandleMove(receiveBody):
        SwitchPlayer()
        currentNumber = playerNumbers[GetCur()]
        otherNumber = playerNumbers[GetOth()]
        if CheckEndGame():
            SendScores()
            game = False
            return str()
    else:
        return str()

    SendGame()
    return str()


if __name__ == "__main__":
    print("Server Started")
    app.run(debug=True)
