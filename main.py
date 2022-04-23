import argparse
import requests
import csv
import pathlib
import json

from airplane import get_star as gs
import pandas as pd

from bs4 import BeautifulSoup

csv_file = str(pathlib.Path.cwd() / 'ratings.csv')


def safeCheck():
    try:
        obj = json.load(open('airlines.json', 'r+', encoding='utf-8'))
    except:
        obj = {}

    if not obj.get('airlines'):
        obj['airlines'] = []
    if not obj.get('mode'):
        obj['mode'] = False

    json.dump(obj, open('airlines.json', 'w+', encoding='utf-8'))


safeCheck()


def get(): return list(csv.reader(open(csv_file, 'w+', encoding='utf-8'), delimiter=':'))
def fetch(): return json.load(
    open('airlines.json', 'r+', encoding='utf-8'))


def acc(b): return b if type(b) == list else [b]


def dump(airlines, mode): json.dump(
    {"airlines": airlines, "mode": mode}, open('airlines.json', 'w+', encoding='utf-8'))


class Ratings():
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="get airline ratings")
        self.parser.add_argument('-c', '--command', type=str, required=False)
        self.parser.add_argument(
            '-a', '--airline', type=str, required=False, nargs='+')

        self.args = self.parser.parse_args()
        self.command = self.args.command

        self.airline = self.args.airline

        if not self.command:
            print(self.update())
            return

        if self.command == 'list':
            self.list()
            return

        if self.command == 'get':
            self.get()
            return

        if self.command == 'mode':
            self.mode()
            return

        if not hasattr(self, self.command):
            print("Invalid command")
            return

        if self.airline is None:
            print("You must have at least a parameter to use this command")
            return

        if hasattr(self, self.command):
            getattr(self, self.command)(self.airline)

    def list(self):
        safeCheck()
        airlines = fetch()['airlines']
        if len(airlines) == 0:
            print("No airlines in list.")
            print("Use 'add' to add an airline.")
            return

        for i, v in enumerate(airlines):
            print("Airline %s: %s" % (i + 1, v))

    def add(self, airlines):
        safeCheck()
        al = set(fetch()['airlines'])
        airlines = [i.replace('_', ' ').replace('-', ' ').title()
                    for i in airlines]
        for i in airlines:
            try:
                gs(i)
            except:
                print("Airline '%s' is invalid." % i)
                continue

            stars = gs(i)
            if type(stars) == list:
                print("There were multiple airplanes that fitted your criteria: \n")
                for m, v in enumerate(stars):
                    print("Airline %s: %s" % (m + 1, v['name']))

                print(
                    "\nPick a number to choose the airplane you meant. (Ctrl-C to exit)")
                try:
                    it = int(input("\nEnter a number: "))
                    stars = stars[it - 1]
                except Exception as e:
                    print("Invalid number.")
                    return

                name = stars['name']
            else:
                name = i

            if name in al:
                print("Airline '%s' already in list." % name)
                return

            al.add(name)
            
        dump(list(al), fetch()['mode'])
        self.update()

    def remove(self, airlines):
        safeCheck()
        al = set(fetch()['airlines'])
        airlines = [i.replace('_', ' ').replace('-', ' ').title()
                    for i in airlines]
        for i in airlines:
            if i not in al:
                print("Airline '%s' not in list." % i)

            al.discard(i)

        dump(list(al), fetch()['mode'])
        self.update()

    def update(self):
        al = fetch()['airlines']
        if not al:
            print("No airlines in list.")
            print("Use 'add' to add an airline.")
            return ""

        headers = ["Airline Ticker", "Rating"]

        lists = [[i, self.convert(
            next(n for n in acc(gs(i)) if n['name'] == i)['stars'])] for i in al]

        writer = csv.writer(open(csv_file, 'w+', newline='',
                            encoding='utf-8'), delimiter=':', lineterminator='\n')

        for i in [headers] + sorted(lists):
            writer.writerow(i)

        return True

    def get(self):
        df = pd.DataFrame(get())
        print(df)

    def ratings(self, airlines):
        airlines = [i.replace('_', ' ').replace('-', ' ').title()
                    for i in airlines]
        for i in airlines:
            try:
                gs(i)
            except:
                print("Invalid airline %s" % i)
                continue

            stars = gs(i)
            if type(stars) == list:
                print("There were multiple airplanes that fitted your criteria: \n")
                for m, v in enumerate(stars):
                    print("Airline %s: %s" % (m + 1, v['name']))

                print(
                    "\nPick a number to choose the airplane you meant. (Ctrl-C to exit)")
                try:
                    it = int(input("\nEnter a number: "))
                    stars = stars[it - 1]
                except Exception as e:
                    print("Invalid number.")
                    return

                print("%s: %s" % (stars['name'], self.convert(
                    gs(stars['name'])['stars'])))
                return
            else:
                print("%s: %s" % (i, self.convert(gs(i)['stars'])))

    def mode(self):
        safeCheck()
        current_mode = fetch()['mode']
        print("Current mode is %s" % ('emoji' if current_mode else 'text'))
        enter = input("Press <enter> to toggle between modes: ")
        if enter == '':
            dump(fetch()['airlines'], not current_mode)
            print("Mode toggled.")
            self.update()

    @staticmethod
    def convert(stars):
        safeCheck()
        if fetch()['mode']:
            return '★' * stars + '✰' * (10 - stars)
        else:
            return '%s/10' % stars


if __name__ == '__main__':
    Ratings()
