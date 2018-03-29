from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
import os

from source.encrypt_decrypt import encrypt_cesar, decrypt_cesar, encrypt_vigenere, decrypt_vigenere
from source.define_space import define_space
from source.attacks_cesar import bruteforce_attack_cesar, frequency_attack_cesar
from source.coincidence import coincidence
from source.kasiski import kasiski
from source.mutual_f_analysis import mutual, analysis
from source.dico import *

WIDTH = 900
HEIGHT = 350

LEVEL_ZERO_VERBOSE = 0
LEVEL_ONE_VERBOSE = 1
LEVEL_TWO_VERBOSE = 2
DEFAULT_LEVEL_VERBOSE = LEVEL_ZERO_VERBOSE

VALUE_CHOICE_CESAR = 'c'
VALUE_CHOICE_VIGENERE = 'v'

VALUE_CHOICE_COINCIDENCE = 'c'
VALUE_CHOICE_KASISKI = 'k'

DEFAULT_KEY_CESAR = "0"
DEFAULT_KEY_VIGENERE = "key"
DEFAULT_MATCHING_PERCENT = "50.0"
DEFAULT_BENCHMARK = "0.065"

FRENCH = 0
ENGLISH = 1
DEFAULT_LANGUAGE = FRENCH

DIR_TESTS_FILES = "/tests"

DEFAULT_STR_AUTHORIZED = "abcdefghijklmnopqrstuvwxyz"
DEFAULT_STR_REMOVED = " \\n\\t"
DEFAULT_STR_DICO_FRENCH = "Dictionnaires/French_ascii.txt"
DEFAULT_STR_BOOK_FRENCH = "Books/Fr-Jules_Verne-20000_Lieues_sous_les_mers.txt"
DEFAULT_STR_DICO_ENGLISH = "Dictionnaires/English.txt"
DEFAULT_STR_BOOK_ENGLISH = "Books/En-Jules_Verne-Around_the_world_in_eighty_days.txt"
str_c = "éèêë|àâä|ç|ùüû|ïî|ôö"
str_t = "eacuio"

class Frame_vigenere(Frame):
    def __init__(self, father):
        Frame.__init__(self, father)
        self.father = father
        self.verbose = StringVar()
        self.verbose.set(DEFAULT_LEVEL_VERBOSE)
        self.language = IntVar()
        self.language.set(DEFAULT_LANGUAGE)
        self.defineLanguage()
        self.GUI()

    def defineLanguage(self):
        if (self.language.get() == FRENCH):
            self.dico = dico(DEFAULT_STR_DICO_FRENCH, DEFAULT_STR_BOOK_FRENCH, int(self.verbose.get()))
        elif (self.language.get() == ENGLISH):
            self.dico = dico(DEFAULT_STR_DICO_ENGLISH, DEFAULT_STR_BOOK_ENGLISH, int(self.verbose.get()))

    def importFile(self):
        filename = askopenfilename(title="Open a file", initialdir=os.getcwd() + DIR_TESTS_FILES)
        try:
            f = open(filename)
            read_file = f.read()
            self.text_file_imported.delete("1.0","end-1c")
            for i in read_file:
                self.text_file_imported.insert("end-1c", i)
            path = filename.split("/")
            self.state_import_file.config(text=path[len(path) - 1])
        except:
            self.state_import_file.config(text="No file imported")

    def saveFile(self):
        try:
            save = asksaveasfile(title="Save a file", initialdir=os.getcwd() + DIR_TESTS_FILES)
            save.write(self.text_file_imported.get("1.0","end-1c"))
            save.close()
            self.state_save_file.config(text="File save")
        except:
            self.state_save_file.config(text="File not saved")

    def encrypt(self):
        if (self.key.get() != "" and self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get()).replace("\\n", "\n").replace("\\t", "\t")
            str_r = str(self.str_removed.get()).replace("\\n", "\n").replace("\\t", "\t")
            if (self.choice_encrypt.get() == VALUE_CHOICE_CESAR):
                try:
                    int(self.key.get())
                except:
                    print("Error in key")
                    return
                result = encrypt_cesar(s, int(self.key.get()), str_a, str_r, str_c, str_t, int(self.verbose.get()))
            elif (self.choice_encrypt.get() == VALUE_CHOICE_VIGENERE):
                result = encrypt_vigenere(s, str(self.key.get()), str_a, str_r, str_c, str_t, int(self.verbose.get()))
            self.text_file_imported.delete("1.0","end-1c")
            self.text_file_imported.insert("end-1c", result)
            self.state_save_file.config(text="File not saved")

    def decrypt(self):
        if (self.key.get() != "" and self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get())
            if (self.choice_encrypt.get() == VALUE_CHOICE_CESAR):
                try:
                    int(self.key.get())
                except:
                    print("Error in key")
                    return
                result = decrypt_cesar(s, int(self.key.get()), str_a, int(self.verbose.get()))
                if (self.define_space.get()):
                    result = define_space(result, self.dico, str_a, int(self.verbose.get()))
            elif (self.choice_encrypt.get() == VALUE_CHOICE_VIGENERE):
                result = decrypt_vigenere(s, str(self.key.get()), str_a, int(self.verbose.get()))
                if (self.define_space.get()):
                    result = define_space(result, self.dico, str_a, int(self.verbose.get()))
        self.text_file_imported.delete("1.0","end-1c")
        self.text_file_imported.insert("end-1c", result)
        self.state_save_file.config(text="File not saved")

    def bruteforce_attack(self):
        if (self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get())
            (result, key) = bruteforce_attack_cesar(s, self.dico, str_a, float(self.percent.get()), int(self.verbose.get()))
            self.key.set(int(key))
            self.text_file_imported.delete("1.0","end-1c")
            self.text_file_imported.insert("end-1c", result)
            self.state_save_file.config(text="File not saved")

    def frequency_attack(self):
        if (self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get())
            (result, key) = frequency_attack_cesar(s, self.dico, str_a, float(self.percent.get()), int(self.verbose.get()))
            self.key.set(key)
            self.text_file_imported.delete("1.0","end-1c")
            self.text_file_imported.insert("end-1c", result)
            self.state_save_file.config(text="File not saved")

    def mutual_attack(self):
        if (self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get())
            if self.choice_length.get() == VALUE_CHOICE_COINCIDENCE:
                (key_len, text_wo, punc) = coincidence(s, float(self.benchmark.get()), int(self.verbose.get()))
                possi_len = []
            else:
                (key_len, possi_len, text_wo, punc) = kasiski(s, int(self.verbose.get()))
            (k, result) = mutual(text_wo, possi_len, punc, key_len, str_a, self.dico, float(self.percent.get()), int(self.verbose.get()))
            self.text_file_imported.delete("1.0","end-1c")
            self.text_file_imported.insert("end-1c", result)
            self.key.set(k)
            self.state_save_file.config(text="File not saved")

    def analysis_attack(self):
        if (self.str_authorized.get() != ""):
            s = self.text_file_imported.get("1.0","end-1c")
            result = ""
            str_a = str(self.str_authorized.get())
            if self.choice_length.get() == VALUE_CHOICE_COINCIDENCE:
                (key_len, text_wo, punc) = coincidence(s, float(self.benchmark.get()), int(self.verbose.get()))
            else:
                (key_len, len_possi, text_wo, punc) = kasiski(s, int(self.verbose.get()))
            (k, result) = analysis(text_wo, punc, key_len, str_a, self.dico, float(self.percent.get()), int(self.verbose.get()))
            self.text_file_imported.delete("1.0","end-1c")
            self.text_file_imported.insert("end-1c", result)
            self.key.set(k)
            self.state_save_file.config(text="File not saved")

    def GUI(self):
        #Frame Left
        frame_left = Frame(self)
        frame_left.grid(row=1, column=1, sticky='ns', padx=3, pady=3)

        #Frame File
        frame_file = LabelFrame(frame_left, text="File")
        frame_file.grid(row=1, column=1)

        button_import = Button(frame_file,text='Import', command=self.importFile)
        button_import.grid(row=1, column=1)

        self.state_import_file = Label(frame_file,text='No file imported', width=20, wraplength=140)
        self.state_import_file.grid(row=1, column=2, columnspan=2)

        self.button_save = Button(frame_file,text='Save', command=self.saveFile)
        self.button_save.grid(row=2, column=1)

        self.state_save_file = Label(frame_file,text='File not save', width=20, wraplength=140)
        self.state_save_file.grid(row=2, column=2, columnspan=2)

        #~ self.button_english = Button(frame_file,text='English', command=self.defineEnglish)
        #~ self.button_english.grid(row=3, column=1)

        #~ self.button_french = Button(frame_file,text='French', command=self.defineFrench)
        #~ self.button_french.grid(row=3, column=2, columnspan=2)        
        
        label_language = Label(frame_file,text='Language :')
        label_language.grid(row=3, column=1)
        self.language = IntVar()
        self.language.set(DEFAULT_LANGUAGE)
        radioButton_french = Radiobutton(frame_file, text="French", variable=self.language, value=FRENCH, command=self.defineLanguage)
        radioButton_french.grid(row=3, column=2)
        radioButton_english = Radiobutton(frame_file, text="English", variable=self.language, value=ENGLISH, command=self.defineLanguage)
        radioButton_english.grid(row=3, column=3)

        #Frame Configurations
        frame_configurations = LabelFrame(frame_left, text="Settings")
        frame_configurations.grid(row=2, column=1, padx=3, pady=3)

        def define_key():
            if (self.choice_encrypt.get() == VALUE_CHOICE_CESAR):
                self.key.set(DEFAULT_KEY_CESAR)
            elif (self.choice_encrypt.get() == VALUE_CHOICE_VIGENERE):
                self.key.set(DEFAULT_KEY_VIGENERE)

        self.choice_encrypt = StringVar()
        self.choice_encrypt.set(VALUE_CHOICE_VIGENERE)
        b_vigenere = Radiobutton(frame_configurations, text="Vigenere", variable=self.choice_encrypt, value=VALUE_CHOICE_VIGENERE, command=define_key)
        b_vigenere.grid(row=1, column=1, columnspan=2)
        b_cesar = Radiobutton(frame_configurations, text="Cesar", variable=self.choice_encrypt, value=VALUE_CHOICE_CESAR, command=define_key)
        b_cesar.grid(row=1, column=3, columnspan=2)

        label_str_authorized = Label(frame_configurations,text='Characters authorized :')
        label_str_authorized.grid(row=2, column=1, columnspan=3)

        self.str_authorized = StringVar()
        self.str_authorized.set(DEFAULT_STR_AUTHORIZED)
        entry_str_authorized = Entry(frame_configurations, textvariable=self.str_authorized, width=25)
        entry_str_authorized.grid(row=3, column=1, columnspan=4)

        label_removed = Label(frame_configurations,text='Characters removed :')
        label_removed.grid(row=4, column=1, columnspan=3)

        self.str_removed = StringVar()
        self.str_removed.set(DEFAULT_STR_REMOVED)
        entry_removed = Entry(frame_configurations, textvariable=self.str_removed, width=25)
        entry_removed.grid(row=5, column=1, columnspan=4)

        label_key = Label(frame_configurations, text='Key : ')
        label_key.grid(row=6, column=1, columnspan=2)
        label_percent = Label(frame_configurations, text='Matching percent : ')
        label_percent.grid(row=7, column=1, columnspan=2)
        label_benchmark = Label(frame_configurations, text='Benchmark : ')
        label_benchmark.grid(row=8, column=1, columnspan=2)

        self.key = StringVar()
        self.key.set(DEFAULT_KEY_VIGENERE)
        entry_key = Entry(frame_configurations, textvariable=self.key, width=10)
        entry_key.grid(row=6, column=3)
        self.percent = StringVar()
        self.percent.set(DEFAULT_MATCHING_PERCENT)
        entry_percent = Entry(frame_configurations, textvariable=self.percent, width=10)
        entry_percent.grid(row=7, column=3)
        self.benchmark = StringVar()
        self.benchmark.set(DEFAULT_BENCHMARK)
        entry_benchmark = Entry(frame_configurations, textvariable=self.benchmark, width=10)
        entry_benchmark.grid(row=8, column=3)

        #Center
        self.text_file_imported = Text(self,width=50, height=20)
        self.text_file_imported.grid(row=1, column=2)

        self.scrollbar_file_imported=Scrollbar(self, orient=VERTICAL)
        self.scrollbar_file_imported.config(command=self.text_file_imported.yview)
        self.scrollbar_file_imported.grid(row=1, column=3, sticky='ns')
        self.text_file_imported.config(yscrollcommand=self.scrollbar_file_imported.set)

        #Frame right
        frame_right = Frame(self)
        frame_right.grid(row=1, column=4, sticky='ns', padx=3, pady=3)

        #Frame attacks_cesar
        frame_attacks_cesar = LabelFrame(frame_right, text="Cryptanalyze of Cesar")
        frame_attacks_cesar.grid(row=1, column=1, padx=3, pady=3)

        button_attack1 = Button(frame_attacks_cesar,text='Bruteforce attack', command=self.bruteforce_attack)
        button_attack1.grid(row=1, column=1, columnspan=3)

        button_attack2 = Button(frame_attacks_cesar,text='Frequency attack', command=self.frequency_attack)
        button_attack2.grid(row=2, column=1, columnspan=3)

        #Frame attacks_vigenere
        frame_attacks_vigenere = LabelFrame(frame_right, text="Cryptanalyze of Vigenere")
        frame_attacks_vigenere.grid(row=2, column=1, padx=3, pady=3)

        def define_length():
            if (self.choice_length.get() == VALUE_CHOICE_COINCIDENCE):
                self.benchmark.set(DEFAULT_BENCHMARK)
                self.percent.set(DEFAULT_MATCHING_PERCENT)

        label_len_key = Label(frame_attacks_vigenere, text="Len of key :")
        label_len_key.grid(row=1, column=1)

        self.choice_length = StringVar()
        self.choice_length.set(VALUE_CHOICE_COINCIDENCE)
        b_vigenere = Radiobutton(frame_attacks_vigenere, text="Coïncidence", variable=self.choice_length, value=VALUE_CHOICE_COINCIDENCE, command=define_length)
        b_vigenere.grid(row=1, column=2)
        b_cesar = Radiobutton(frame_attacks_vigenere, text="Kasiski", variable=self.choice_length, value=VALUE_CHOICE_KASISKI, command=define_length)
        b_cesar.grid(row=1, column=3)

        button_attack3 = Button(frame_attacks_vigenere,text='Mutual index of coïncidence attack', command=self.mutual_attack)
        button_attack3.grid(row=2, column=1, columnspan=3)

        button_attack4 = Button(frame_attacks_vigenere,text='Frequency analysis attack', command=self.analysis_attack)
        button_attack4.grid(row=3, column=1, columnspan=3)

        #Frame encrypt decrypt
        frame_encrypt_decrypt = LabelFrame(frame_right, text="Encrypt / Decrypt")
        frame_encrypt_decrypt.grid(row=3, column=1, padx=3, pady=5)

        label_verbose = Label(frame_encrypt_decrypt,text='Level Verbosity :')
        label_verbose.grid(row=1, column=1, columnspan=3)

        b_level_0 = Radiobutton(frame_encrypt_decrypt, text="Level 0", variable=self.verbose, value=LEVEL_ZERO_VERBOSE)
        b_level_0.grid(row=2, column=1)
        b_level_1 = Radiobutton(frame_encrypt_decrypt, text="Level 1", variable=self.verbose, value=LEVEL_ONE_VERBOSE)
        b_level_1.grid(row=2, column=2)
        b_level_2 = Radiobutton(frame_encrypt_decrypt, text="Level 2", variable=self.verbose, value=LEVEL_TWO_VERBOSE)
        b_level_2.grid(row=2, column=3)

        button_encrypt = Button(frame_encrypt_decrypt,text='Encrypt', command=self.encrypt)
        button_encrypt.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        button_decrypt = Button(frame_encrypt_decrypt,text='Decrypt', command=self.decrypt)
        button_decrypt.grid(row=3, column=2, columnspan=3, padx=5, pady=5)

        self.define_space = IntVar()
        self.define_space.set(0)
        check_space = Checkbutton(frame_encrypt_decrypt, text="Define space", variable=self.define_space)
        check_space.grid(row=4, column=1, columnspan=3)

def main():
    window = Tk()
    window.title("Vigenère")

    x = (window.winfo_screenwidth() / 2) - (WIDTH / 2)
    y = (window.winfo_screenheight() / 2) - (HEIGHT / 2)
    window.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

    mainframe = Frame_vigenere(window)
    mainframe.pack()

    window.mainloop()

main()
