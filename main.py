import mysql.connector
from blocks import Blockchain, Block
from collections import deque
from parties import Party
# importing pandas as pd
import pandas as pd
ts = pd.Timestamp(year = 2011, month = 11, day = 21, hour = 10, second = 49, tz = 'US/Central')



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database=""
)


mycursor = mydb.cursor()

class Voters:
  def __init__(self,db):
    self.db=mycursor


  def check_voter(self,voterId):
    check=False
    mycursor.execute("SELECT * FROM Voters where voterId=%s", (voterId,))
    data = mycursor.fetchall()
    if data:
      check=True
      return check
    else:
      check=False
      return check



  def insert_voter(self,voterId,voterName,voterAge,voterCity):
    check_present_voter=Voters.check_voter(voterId)
    if check_present_voter==True:
      return "Voter already present in the system!"
    else:
      sql = "INSERT INTO Voters (voterId, voterName, voterAge, voterCity) VALUES (%s, %s,%s,%s)"
      val = (voterId,voterName,voterAge,voterCity)
      mycursor.execute(sql, val)
      mydb.commit()
      return "New Voter Details inserted in the system!"



class Parties:
  def __init__(self,db):
    self.db=mycursor

  def insert_parties(self,partyId, partyName,symbol):
    check_present_voter = Parties.check_parties(partyId)
    if check_present_voter == True:
      return "Party already present in the system!"
    else:
      sql = "INSERT INTO Parties (partyID, partyName, symbol) VALUES (%s, %s,%s)"
      val = (partyId,partyName,symbol)
      mycursor.execute(sql, val)
      mydb.commit()
      return "New Voter Details inserted in the system!"


  def check_parties(self,partyId):
    check = False
    mycursor.execute("SELECT * FROM Parties where partyID=%s", (partyId,))
    data = mycursor.fetchall()
    if data:
      check = True
      return check
    else:
      check = False
      return check




class Votings:

  def __init__(self,db):
    self.db=mycursor


  def check_voted_by_voter(self,voterID):
    check = False
    mycursor.execute("SELECT * FROM votings where VoterID=%s", (voterID,))
    data = mycursor.fetchall()
    if data:
      check = True
      return check
    else:
      check = False
      return check


  def votings_details(self,voterID):
    sql="INSERT INTO Votings(VoterID, Voted) VALUES (%s, %s)"
    val = (voterID,ts.now())
    mycursor.execute(sql, val)
    mydb.commit()
    return "Voting Successfull !"




print("Login Into the system and Vote for your favourite Party !")

voters = Voters(mycursor)
party=Parties(mycursor)
votings=Votings(mycursor)

mempool={}
party_details=Party.getParties()

n=1

winner={'TinguSarkar':0,'NOTA':0,'ShreyuSarkar':0,'SidEkNamuna':0,'SankiSarkar':0}

# while n<=6:
#   i = int(input("Enter the number 1 to login and vote your candidate:"))
#   if i==1:
#     ID=int(input("Enter your Voter ID:"))
#     if voters.check_voter(ID):
#       pass
#       if votings.check_voted_by_voter(ID):
#         print("You have already casted your vote !")
#       else:
#         print("Vote accordingly!")
#         for index, party in enumerate(party_details):
#           print(f"{index}. {party.symbol} {party.partyName}\n")
#         v=int(input("Enter your vote:"))
#         for index, party in enumerate(party_details):
#           if v==index:
#             mempool[str(ID)]=party.partyName
#
#
#     else:
#       print("No such voter in the constituency !")
#
#   else:
#     exit()
#
#   n+=1

blockchain = Blockchain(Blockchain.curr_hash)

for ID, partyID in {
  "994968317349": 1,
  "292916015840": 1,
  "259326718916": 0,
  "719889320346": 2,
  "912779882179": 3,
  "994968317347": 1,
  "771458061273": 1,
  "149277622179": 1,
  "252135586177": 0,
  "594914337308": 2,
  "725618484618": 3,
  "771718507971": 1,

}.items():
  if len(mempool) == 6:
    print(mempool)
    blockchain.insert_block(mempool.copy())
    mempool.clear()

  if voters.check_voter(ID):
    pass
    if votings.check_voted_by_voter(ID):
      print("You have already casted your vote !")
    else:
      for index, party in enumerate(party_details):
          if partyID==index:
            mempool[str(ID)]=party.partyName
            votings.votings_details(ID)

  else:
    print("No such voter in the constituency !")

d = {party.partyName:0 for party in party_details}
for block in blockchain.blockchain[1:]:
  pass
  for voterID, partyName in block.data.items():
      d[partyName] += 1

for block in blockchain.blockchain:
  print(block)
  print("\n")

d = sorted(d.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
print("The Winner is:", d[0][0])



