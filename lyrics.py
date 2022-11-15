import requests, json, os
from bs4 import BeautifulSoup
from tabulate import tabulate
import mutagen
from mutagen import id3, mp3
import argparse

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

parser = argparse.ArgumentParser()
parser.add_argument('--titleMode', type=str, help=f"Mode for getting the title of the song you're getting lyrics for. Pass 'manual' if you want to choose the title from the filename, 'file' if the title is already in the mp3 metadata, or 'entry' if you want to type in the song names. DEFAULT: 'manual'")
parser.add_argument('--dir', type=str, required=True, help=f"The directory where the mp3 files you wish to add lyrics to are located.")
parser.add_argument('--src', type=str, help=f"The site to get lyrics from. 'azlyrics' for azlyrics.com or 'genius' for genius.com")

AZ_url = "https://search.azlyrics.com/suggest.php"

AZ_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://www.azlyrics.com",
    "Pragma": "no-cache",
    "Referer": "https://www.azlyrics.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

G_url = "https://genius.com/api/search/multi"

G_headers = {
    "cookie": "_genius_ab_test_cohort=70; _genius_ab_test_desktop_song_primis=inread",
    "authority": "genius.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "pragma": "no-cache",
    "referer": "https://genius.com/search/embed",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}


def insertTitle(f, newtitle):
    addTitle = input(f"\nWould you like to add the title you selected to the track metadata? {c.BOLD}{c.UNDERLINE}y/n{c.END}\n")
    if addTitle == 'y':
        mp3 = id3.ID3(f)
        mp3.add(id3.TIT2(encoding=3, text=u"{}".format(newtitle['q'])))
        mp3.save()
    else:
        return


def getTitle(f, mode=None):
    if mode == "manual":    
        # makes number row and makes it purple
        nums = [f"{i+1}{c.END}" for i in range(len(file.split(' ')))]

        # makes word row
        words = [char for char in file.split(' ')]

        # removes the file extension from the last word
        words[-1] = words[-1].split('.')[0]

        # adds the Number and Word headers to the left
        nums.insert(0, f"{c.BOLD}{c.HEADER}Number:{c.END}")
        words.insert(0, f"{c.BOLD}{c.HEADER}Word:{c.END}")
        print('\n')

        # makes a horizontal table and splits the filename into words, so the user can manually select the title
        print(tabulate([nums, words], tablefmt="rounded_grid"))
        wordRange = input(f"{c.UNDERLINE}{c.BOLD}Select the title by entering a number range{c.END} (e.g. 1-3, 4, 5-7): ")
        ranges = wordRange.split(',')
        selectedWords = []

        # parses the number range and selects the words that the user picked for the title
        for rng in ranges:
            if '-' in rng:
                lower = int(rng.split('-')[0])
                upper = int(rng.split('-')[1]) + 1
                for i in range(lower, upper):
                    selectedWords.append(words[i])
            else:
                selectedWords.append(words[int(rng)])

        return {'q': " ".join(selectedWords)}

    if mode == "file":
        try:
            title = mutagen.id3.ID3(f)['TIT2']
            return {'q': f'{title}'}
        except KeyError:
            newtitle = ""
            choice = int(input(f'\nThe file for "{c.HEADER}{c.BOLD}{f}{c.END}" does not contain any title metadata. Enter title \033[4m{c.BOLD}manually (1){c.END} or by \033[4m{c.BOLD}filename (2)?{c.END}\n{c.BOLD}Choose: {c.END}'))
            if choice == 1:
                newtitle = getTitle(f, mode='entry')
                insertTitle(f, newtitle)
                return newtitle
            elif choice == 2:
                newtitle = getTitle(f, mode='manual')
                insertTitle(f, newtitle)
                return newtitle
            else:
                print("Choose 1 or 2.")
                getTitle(f, mode='file')


    if mode == "entry":
        title = input("Enter title of song: ")
        return {'q': f'{title}'}


def getSongs(title, source=None):
    if source == 'azlyrics':
        response = requests.request("GET", AZ_url, headers=AZ_headers, params=title)
        if not len(json.loads(response.text)['songs']):
            print(f"\nNo results found for {c.HEADER}{c.BOLD}{title['q']}{c.END}\n")
            retry = input(f"Would you like to try another search with a different title? {c.BOLD}{c.UNDERLINE}y/n{c.END}\n")
            if retry == 'y':
                mode = int(input(f"Would you like to enter the title {c.UNDERLINE}{c.BOLD}manually (1){c.END} or by using the {c.UNDERLINE}{c.BOLD}filename (2){c.END}?"))
                print(mode)
                if mode != 1 or mode != 2:
                    print("Enter 1 or 2")
                    getSongs(title, source='azlyrics')
                else:
                    title = getTitle(f, mode='entry') if mode == 1 else getTitle(f, mode='manual')
                return getSongs(title, source='azlyrics')
            elif retry == 'n':
                return
            else:
                print("Enter y or n")
                getSongs(title, source='azlyrics')
        else:
            return json.loads(response.text)
    else:
        response = requests.request("GET", G_url, headers=G_headers, params=title)
        if not len(json.loads(response.text)['response']['sections'][0]['hits']):
            print(f"\nNo results found for {c.HEADER}{c.BOLD}{title['q']}{c.END}\n")
            retry = input(f"Would you like to try another search with a different title? {c.BOLD}{c.UNDERLINE}y/n{c.END}\n")
            if retry == 'y':
                mode = int(input(f"Would you like to enter the title {c.UNDERLINE}{c.BOLD}manually (1){c.END} or by using the {c.UNDERLINE}{c.BOLD}filename (2){c.END}?"))
                if mode != 1 or mode != 2:
                    print("Enter 1 or 2")
                    getSongs(title, source='genius')
                else:
                    title = getTitle(f, mode='entry') if mode == 1 else getTitle(f, mode='manual')
                return getSongs(title, source='genius')
            elif retry == 'n':
                return
            else:
                print("Enter y or n")
                getSongs(title, source='genius')
        else:
            return json.loads(response.text)

args = parser.parse_args()
os.system('cls')

for file in os.listdir(args.dir):
    f = os.path.join(args.dir, file)
    if not os.path.isfile(f) and f.endswith('.mp3'):
        print(f"\n{c.FAIL}{f} is not a mp3 file!{c.END}")
        continue

    
    title = getTitle(f, mode=(args.titleMode if args.titleMode else 'manual'))

    header = f'{c.BOLD}{c.HEADER}Songs matching "{title["q"]}"{c.END}'
    results = [[header]]

    if args.src == 'azlyrics':
        res = getSongs(title, source="azlyrics")
        try:
            for i, result in enumerate(res['songs']):
                results.append([result['autocomplete']])
        except TypeError:
            print(f"\n{c.FAIL}Skipped: {title['q']}{c.END}")
            continue
    else:
        res = getSongs(title, source="genius")
        try:
            for i, result in enumerate(res['response']['sections'][1]['hits']):
                results.append([result['result']['full_title']])
        except TypeError:
            print(f"\n{c.FAIL}Skipped: {title['q']}{c.END}")
            continue



    print('\n')

    print(tabulate(results, showindex="always", tablefmt="rounded_grid"))
    song = int(input(f"{c.BOLD}{c.UNDERLINE}Select index of correct song:{c.END} "))

    if args.src == 'azlyrics':
        lyricsUrl = res['songs'][song - 1]['url']
        songName = res['songs'][song-1]['autocomplete']

        r = requests.get(lyricsUrl)
        soup = BeautifulSoup(r.text, 'html.parser')

        lyrics = soup.select('.ringtone ~ div:not([class])')[0].get_text()
    else:
        lyricsUrl = res['response']['sections'][1]['hits'][song-1]['result']['url']
        songName = res['response']['sections'][1]['hits'][song-1]['result']['full_title']

        r = requests.get(lyricsUrl)
        soup = BeautifulSoup(r.text, 'html.parser')

        lyrics = str(soup.select('div[data-lyrics-container]')[0].decode_contents()).replace('<br/>', '\n')

    mp3 = mutagen.id3.ID3(f)
    mp3.add(mutagen.id3.USLT(encoding=3, lang="eng", text=lyrics))
    mp3.save()

    print(f"\nFinished {c.HEADER}{c.BOLD}{songName}!{c.END}")

print(f"\n\n{c.OKGREEN}All Done!{c.END}")

# lyrics.py --titleMode file --dir "C:\Users\turtl\OneDrive\Desktop\Ben Howard - 2018 - Noonday Dream" --src genius