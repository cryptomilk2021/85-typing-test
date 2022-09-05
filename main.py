from tkinter import *
# import random
import datetime
time_to_go = 0
words = "A princess is cursed by a vindictive elder with weightlessness, and a prince is prepared to die to rescue " \
        "her. A summer installment of our series on fairy tale architecture is less a love-and-marriage story than a " \
        "deceptively simple psychological thriller with excellent special effects and a non-conformist heroine "
words = words.replace('.', '').replace(',', '').replace('-', ' ').lower()
split = words.split()
split_list = []
for i in split:
    if len(i) > 1:
        split_list.append(i)
# random.shuffle(split_list)
START_TIME = 60
word_list = []  # word, length, nbr of letters mispelled
for i in split_list:
    word_list.append([i, len(i), 0, 0])
offset = 0
for i in word_list:
    print(i[1])
for i in range(len(word_list) - 1):
    word_list[i][3] = offset
    offset = offset + word_list[i][1] + 1


pointer_list = [0, 0, 0, 'mask', 0]  # curr_pos(Enter), curr word, curr letter, masknamebase, mask counter

## Creating a new window and configurations
window = Tk()
window.title("Typing test")
window.minsize(width=800, height=600)
window.config(padx=50, pady=50)

# Labels
padx = 50
pady = 20
label_corrected_CPM = Label(text="Corrected CPM: 0")
label_corrected_CPM.grid(row=0, column=0)
label_corrected_CPM.config(padx=padx, pady=pady)

##
label_WPM = Label(text="WPM: 0")
label_WPM.grid(row=0, column=1)
label_WPM.config(padx=padx, pady=pady)

label_time_left = Label(text="time left: 0")
label_time_left.grid(row=0, column=2)
label_time_left.config(padx=padx, pady=pady)

type_text = Text(width=50, height=10, wrap='word', font=("Arial", 20))
type_text.insert('1.0', split_list)
type_text['state'] = 'disabled'
type_text.grid(row=1, column=1)


def timer():
    global time_to_go
    time_to_go -= 1
    if time_to_go < 0:
        time_to_go = 0
    label_time_left.config(text=f"time left: {str(time_to_go)}")
    if time_to_go < 1:
        print('end of test')
    window.after(1000, timer)


def select_next_word():
    global time_to_go
    if time_to_go == 0:
        #we are starting
        time_to_go = START_TIME
        label_time_left.config(text="time left: 60")

    type_text.tag_delete('cd')
    current_word = pointer_list[1]
    current_pos = pointer_list[0]
    type_text.tag_add('cd', f'1.{word_list[current_word][3]}',
                      f'1.{word_list[current_word][3] + word_list[current_word][1]}')
    type_text.tag_configure('cd', background='green')
    pointer_list[2] = 0
    pointer_list[0] = word_list[current_word][3]
    # pointer_list[1] += 1


def letter_pressed(event):
    global time_to_go
    if event.keycode == 8:  # ignore backspace
        return ()
    #display CPM
    label_corrected_CPM.config(text=f"Corrected CPM: {pointer_list[0]*(60-time_to_go)/60}")
    # check if past end of word, if space add to score, else get next word
    # compare if same
    # change col
    # else change col
    # increment current pos pointer_list[0]

    if pointer_list[2] == word_list[pointer_list[1]][1]:
        pointer_list[1] += 1
        select_next_word()
        return None

    if event.char == word_list[pointer_list[1]][0][pointer_list[2]]:
        # print('match')
        apply_letter_tag(pointer_list[0], "Y")
    else:
        # print('mismatch')
        apply_letter_tag(pointer_list[0], "N")
        # if pointer_list[2] == word_list[pointer_list[1]][1] - 1:
        #     print('last letter')

    pointer_list[2] += 1
    pointer_list[0] += 1


def apply_letter_tag(offset, type):
    if type == "Y":
        type_text.tag_add('highlightletter', f'1.{offset}', f'1.{offset + 1}')
        type_text.tag_configure('highlightletter', foreground="blue")
    else:
        type_text.tag_add('highlightletter1', f'1.{offset}', f'1.{offset + 1}')
        type_text.tag_configure('highlightletter1', foreground="red")


# Buttons
button = Button(text="Start", command=select_next_word)
button.grid(row=3, column=1)

# user input text box
user_input = Entry(textvariable="start typing here", width=50, font="si")

user_input.bind('<Key>', letter_pressed)
user_input.grid(row=2, column=1)
user_input.focus()

window.after(1000, timer)
window.mainloop()
