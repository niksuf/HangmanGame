from random import choice


# Проверка новой игры или выхода
def check_start():
    while True:
        user_input = input()
        if user_input == 'N' or user_input == 'n':
            return True
        if user_input == 'E' or user_input == 'e':
            return False
        else:
            print('Нажмите [N] или [E]!')


# Проверка ввода буквы
def check_letter(word, tried_letters):
    while True:
        user_input = input('Введите букву (кириллица): ').lower()
        if user_input in [chr(i) for i in range(1072, 1104)]:
            if user_input in tried_letters:
                print('Вы уже пробовали эту букву! Введите новую!')
            elif user_input in word:
                print('Прекрасно! Вы угадали букву!\n')
                return True, user_input
            else:
                print('Мимо! Не угадали букву!\n')
                return False, user_input
        else:
            print('Некорректный ввод, попробуйте еще раз!')


# Загрузка ассетов (списка слов и картинок виселицы, выбор случайного слова)
def load_assets(words='russian_nouns.txt', pics='hangman.txt', enc='UTF-8'):
    with open(words, encoding=enc) as dictionary, open(pics, encoding=enc) as pictures:
        content = dictionary.readlines()
        word = choice(content).rstrip()
        hangman_pics = pictures.read().split(',')
        assets = (word, hangman_pics)
        return assets


# Отображение игрового процесса (маска слова, картинка)
def show_board(word, guessed_letters, top='_', delimiter='|'):
    wordlist = list(word)
    for i, v in enumerate(wordlist):
        if v in guessed_letters:
            wordlist[i] = v
        else:
            wordlist[i] = '*'
    print(top * len(wordlist) * 2)
    print('\033[1m' + delimiter + delimiter.join(wordlist) + delimiter + '\033[0m')
    print(top * len(wordlist) * 2)


# Основная функция игры
def run_main_game(word, hangman_pics):
    tried_letters = []
    guessed_letters = []
    lives_left = len(hangman_pics) - 1
    session_running = True

    while run_game and session_running:
        print('\033[0;34m' + hangman_pics[len(hangman_pics) - lives_left - 1] + '\n\033[0;30m')
        print(f"Загадано слово из {len(word)} букв. Вы угадали {len(guessed_letters)} букв. "
              f"Осталось {lives_left} жизней\n")

        show_board(word, guessed_letters)

        res = check_letter(word, tried_letters)
        if res[0]:
            guessed_letters.append(res[1])
            tried_letters.append(res[1])
        else:
            tried_letters.append(res[1])
            lives_left -= 1

        if len(set(guessed_letters)) == len(set(word)):
            print(f'\033[1mПоздравляем вы выиграли!\n\033[0m')
            session_running = False
        if lives_left == 0:
            print(f'\033[1mК сожалению, вы проиграли\n\033[0m')
            session_running = False


if __name__ == '__main__':
    print('Добро пожаловать в ВИСЕЛИЦУ!\n[N] - новая игра\n[E] - выход\n[N]ew game\n[E]xit')
    run_game = True
    while run_game:
        if check_start():
            run_main_game(*(load_assets()))
            print('Запустить заново?\n[N] - новая игра\n[E] - выход\n[N]ew game\n[E]xit')
        else:
            run_game = False
    else:
        print('Спасибо за игру!')
