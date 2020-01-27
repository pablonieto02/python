
import hashlib
import hmac
import csv

csv_file = open('01_06_2019_a_26_01_2020.csv', encoding='utf-8')
export_file = open('export_01_06_2019_a_26_01_2020.csv','w')
csv_reader = csv.reader(csv_file)

secret = bytes('rQt8FyPbHiVAKok2Phkqf8rTzuDDkIfyU8VlUdFo6vJXVU06188rXZTXMkePG8oxBb4zgMYnvYju8cEa8giujeBeyGuyjRcbhmIhtFtJ4eyyH8J0H1j4ujgedwsr7kl2IXafVpfCrXZp8066GiZJnpouSFpK1pNietbBjbbF1di4wtphPgeZZRJwXkAiHArso64wCkmvXz5WAbCaHe5ZS5RkKCxy1fGa03WzdahIQSO1zlpPGrRygPtY8snb0PsJ', 'utf-8')

count = 1
for row in csv_reader:
    count = count + 1

    message = bytes(row[0], 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    user_key = hash.hexdigest()

    export_file.write(row[0] + ',' + user_key)
    export_file.write('\n')