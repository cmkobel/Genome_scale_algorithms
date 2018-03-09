import random

class TestTools:


    @staticmethod
    def String_Random(length, alphabet):

        if alphabet is None:
            alphabet = ["abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "]

        str_rnd = ""

        for i in range(0, length):
            str_rnd += alphabet[random.randint(0, len(alphabet) - 1)]

        return str_rnd

    @staticmethod
    def String_Inject_Random(base, injection, times):

        if times is None or times < 1:
            times = 1

        nbase = base
        ls_pos = []

        for i in range(0, times):
            ls_pos.append( random.randint(0, len(nbase) - 1) )

        ls_pos.sort( reverse = True)

        for i in range(0, times):
            pos = ls_pos[i]
            nbase =  nbase[:pos] + injection + nbase[pos + 1:]

        return nbase