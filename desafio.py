#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import sha1
import requests
import json
import string


class Decifrador:

    alfabeto = list(string.ascii_lowercase)
    data = {}

    def __init__(self, token=''):

        self.token = token
        self.url = f'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={token}'
        self.get_data()

    def get_data(self):
        r = requests.get(url=(self.url))
        self.data = json.loads(r.text)

    def decodifica(self):

        for letra in self.data.get('cifrado'):
            if letra not in Decifrador.alfabeto:
                self.data['decifrado'] += letra
            else:
                chave = Decifrador.alfabeto.index(letra)
                i = chave - self.data.get('numero_casas')
                self.data['decifrado'] += self.alfabeto[i]

        hash = sha1(self.data['decifrado'].encode('utf-8'))
        self.data['resumo_criptografico'] = hash.hexdigest()

        return self.data['decifrado']

    def save(self):
        f = open("answer.json", "a+")
        f.write(json.dumps(self.data, indent=4))
        f.close()

        file = {'answer': open('answer.json', 'rb')}

        r = requests.post(f'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={self.token}',
                          files=file)
        print(r.headers)
        print(r.status_code)


if __name__ == "__main__":
    decifrador = Decifrador(token='4bd1f2bffee0d2d663c0c238ebd19257caed4a06')
    print(decifrador.decodifica())
    decifrador.save()
