
def hashing(password_string):
        hashing_dict = {
                "a":"ADJAKF12",
                "b":"FDAJFKADXZ",
                "c":"DFSKA",
                "d":"ERKASLK",
                "e":"LDKSFLAKFDS",
                "f": "BFAMDSL",
                "g": "ZXIASKD",
                "h": "PRSIKASDM",
                "i": "JSKDFAJAK",
                "j": "ZZZZ",
                "k": "PDSAOFJ",
                "l":"DKFLAKS11",
                "m":"1238ASD",
                "n":"FDSAFMK",
                "o":"JKFMASNKD",
                "p":"MN2319X",
                "q":"123ASHZZJ",
                "r":"RKSLADJ",
                "s":"SDMADNFK",
                "t":"XMMZKADMF555",
                "u":"DKFLAJ123",
                "v":"SMMAFJ",
                "w":"KFDASFJK155",
                "x":"KFJADKFJM11034",
                "y":"MMMHNGHJGHM",
                "z":"FKAJKDFJ!"
            }
        hashed_password = ""
        #This part of the function encrypts the password the user inputs. It uses the keys above to transform the letters below into unreadable text.
        for i in password_string:
                if i in hashing_dict:
                        hashed_password = hashed_password + hashing_dict[i]
                else:
                        if i.lower() in hashing_dict:
                                hashed_password = hashed_password + hashing_dict[i.lower()].lower()
                        else:
                                hashed_password = hashed_password + i
        return hashed_password

