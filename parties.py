import mysql.connector



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="blockchainVoting"
)



mycursor = mydb.cursor()


class Party:
    def __init__(self, partyID,partyName,symbol,password):
        self.partyID=partyID
        self.partyName=partyName
        self.symbol=symbol
        self.password=password

    @classmethod
    def getParties(cls):
        parties = []
        mycursor.execute("SELECT * FROM Parties")
        data = mycursor.fetchall()

        for party in data:
            p = Party(party[0], party[1], party[2], party[3])
            parties.append(p)

        return parties


party=Party.getParties()
print(party)