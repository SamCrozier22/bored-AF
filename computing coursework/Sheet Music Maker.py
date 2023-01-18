import sounddevice as sd
import numpy as np
import scipy.fftpack
import pygame
import sys
import math
import os
import copy

'''
display portion
'''
#pygame setup
pygame.init()
res = (1080, 540)
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Sheet Music Maker")
white = (255,255,255)
color2 = (0, 0, 0)
color3 = (169, 169, 169)
red = (180, 0, 0)
dark_grey = (148, 148, 148)
light_grey = (204, 204, 204)
current_colour = dark_grey
Font = pygame.font.Font(None, 32)
errorFont = pygame.font.Font(None, 20)
start_y = 90
width = screen.get_width()
height = screen.get_height()
font = pygame.font.Font('freesansbold.ttf', 32)
titleFont = pygame.font.Font(None, 80)
location = (200, 100)
clef = pygame.image.load("clef.jpg")
clef = pygame.transform.scale(clef, (70, 80))
note = ["A", "B", "C", "D", "E", "F", "G"]

class box(object):
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = dark_grey
        self.text = text
        self.txt_surface = Font.render(text, True, self.colour)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.colour = dark_grey if self.active else light_grey
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    global songName
                    songName = self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.txt_surface = Font.render(self.text, True, self.colour)
                else:
                    self.text += event.unicode
                    self.txt_surface = Font.render(self.text, True, self.colour)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

class inputBox(box):
    def __init__(self, x, y, w, h, title, inputType, errorMessage, text='',):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = dark_grey
        self.text = text
        self.txt_surface = Font.render(text, True, self.colour)
        self.active = False
        self.inputType = inputType
        self.correct = False
        self.displayError = False
        self.errorMessage = errorFont.render(errorMessage, True, red)
        self.title = Font.render(title, True, white)
    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    
    def check(self):
        self.correct = False
        if self.inputType == "string":
            if len(self.text) > 0 and len(self.text) < 20:
                self.correct = True
            else:
                self.correct = False
        elif self.inputType == "integer":
            try:
                num = int(self.text)
                if num >= 30 and num <= 240:
                    self.correct = True
            except:
                self.correct = False
    
    def displayErrorMessage(self):
        screen.blit(self.errorMessage, (self.rect.x+5, self.rect.y + self.rect.h + 5))
    
    def titleDisplay(self):
        screen.blit(self.title, (self.rect.x+5, self.rect.y-30))

class button(box):
    def __init__(self, x, y, w, h, text, checkList):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = dark_grey
        self.text = text
        self.txt_surface = Font.render(text, True, self.colour)
        self.active = False
        self.finished = False
        self.checkList = checkList
        self.tempCheck = 0
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.finished = False
                self.tempCheck = 0
                for box in self.checkList:
                    box.displayError = False
                    if box.correct == False:
                        box.displayError = True
                        self.tempCheck += 1
                if self.tempCheck == 0:
                    self.finished = True
            else:
                self.active = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.active = False

clock = pygame.time.Clock()
SongNameBox = inputBox(150, 150, 400, 50, "Song name: ", "string", "Please enter a valid string between 1 and 20 characters")
BPMBox = inputBox(150, 350, 200, 75, "BPM:", "integer", "Please enter a valid integer number between 30 and 240")
inputBoxes = [SongNameBox, BPMBox]
enterButton = button(600, 150, 250, 250, "click to enter values", inputBoxes)
boxes = [SongNameBox, BPMBox, enterButton]
done = False
while not done:
        for event in pygame.event.get():
            if enterButton.finished == True:
                done = True
            for box in boxes:
                box.handle_event(event)

        for box in inputBoxes:
            box.check()
            box.update()

        screen.fill((30, 30, 30))
        
        titleText = titleFont.render("Sheet Music Maker", True, white)
        screen.blit(titleText, (250, 20))

        for box in inputBoxes:
            box.titleDisplay()
            if box.displayError == True:
                box.displayErrorMessage()

        for box in boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)
songName = SongNameBox.text
BPM = int(BPMBox.text)
BPM_uhh = str(BPM)
BPM_words = ("BPM = " + BPM_uhh)
BPMText = font.render(BPM_words, True, color2, white)
nameText = font.render(songName, True, color2, white)


#background music sheet
def base_screen():
    screen.fill(white)
    screen.blit(BPMText, (100, 30))
    screen.blit(nameText, (420, 30))
    screen.blit(clef, (100, 100))
    screen.blit(clef, (100, 250))
    screen.blit(clef, (100, 400))
    
    for i in range(0, 5):
        pygame.draw.line(screen, color2, (100, i*22 + start_y), (1000, i*22 + start_y), 5)
        pygame.draw.line(screen, color2, (100, (i+7)*22 + start_y), (1000, (i+7)*22 + start_y), 5)
        pygame.draw.line(screen, color2, (100, (i+14)*22 + start_y), (1000, (i+14)*22 + start_y), 5)
    for i in range(0, 2):
        pygame.draw.line(screen, color3, (100, (i*22)+200), (1000, (i*22)+200), 1)
        pygame.draw.line(screen, color3, (100, (i*22)+354), (1000, (i*22)+354), 1)
    pygame.display.flip()

def sharp(x, y):
    pygame.draw.line(screen, color2, (x+26, y-11), (x+32, y-30), 3)
    pygame.draw.line(screen, color2, (x+18, y-11), (x+24, y-30), 3)
    pygame.draw.line(screen, color2, (x+18, y-26), (x+35, y-26), 3)
    pygame.draw.line(screen, color2, (x+15, y-15), (x+32, y-15), 3)
    
#draw the note in position 
def noted(thingy, k):
    if thingy[0] != "REST":
        center_y = 431 - (thingy[0] * 11)
        center_x = (k*65) + 200
        center = (center_x, center_y)
        pygame.draw.circle(screen, color2, center, 10)
        pygame.draw.line(screen, color2, (center_x+8, center_y), (center_x+9, center_y-40), 4)
        if thingy[1] == True:
            sharp(center_x, center_y)
    else:
        pygame.draw.circle(screen, color2, ((k*65)+200, 145), 10, 4)
        pygame.draw.circle(screen, color2, ((k*65)+200, 299), 10, 4)
        pygame.draw.circle(screen, color2, ((k*65)+200, 453), 10, 4)

#use the prior procedures to display the current list of notes
def display(current_list):
    base_screen()
    song_formatted = []
    for i in range(0, len(current_list)):
        sharp = False
        current_note = current_list[i]
        if current_note != "REST":
            index = note.index(current_note[0])
            octave = int(current_note[len(current_note)-1]) -1
            octave_add = 7 * octave
            position = index + octave_add - 9
            if current_note[1] == "#":
                sharp = True
            if position < 2:
                song_formatted.append(["REST", False])
            else:
                song_formatted.append([position, sharp])
        else: song_formatted.append(["REST", False])
        
    for k in range(0, len(song_formatted)):
        noted(song_formatted[k], k)
    pygame.display.flip()

'''
note detection
'''
#variables we'll need for calcs and input stream
samp_freq = 44100
window_size = int(44100 * 60 / BPM)
window_step = window_size
samp_len_sec = 1 / samp_freq
window_len_sec = window_size / samp_freq
windowSamples = [0 for _ in range(window_size)]
power_threshhold = 1e-6

#maffs for finding closest note from a pitch
CONCERT_PITCH = 440
ALL_NOTES = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"]
def find_closest_note(pitch):
  i = int(np.round(np.log2(pitch/CONCERT_PITCH)*12))
  closest_note = ALL_NOTES[i%12] + str(4 + (i + 9) // 12)
  closest_pitch = CONCERT_PITCH*2**(i/12)
  return closest_note, closest_pitch

#here comes the sciencey stuff
currentSong = []
def callback(indata, frames, time, status):
    global windowSamples
    if status:
        print(status)
    if any(indata):
        windowSamples = np.concatenate((windowSamples,indata[:, 0]))
        windowSamples = windowSamples[len(indata[:, 0]):]
        magnitudeSpec = abs(scipy.fftpack.fft(windowSamples)[:len(windowSamples)//2])

        for i in range(int(62/(samp_freq/window_size))):
            magnitudeSpec[i] = 0

        #harmonic product spectrum
        hps_spec = copy.deepcopy(magnitudeSpec)
        for i in range(5):
            tmp_hps_spec = np.multiply(hps_spec[:int(np.ceil(len(magnitudeSpec)/(i+1)))], magnitudeSpec[::(i+1)])
            if not any(tmp_hps_spec):
                break
        hps_spec = tmp_hps_spec

        maxInd = np.argmax(hps_spec)    
        maxFreq = maxInd * (samp_freq/window_size)
        closestNote, closestPitch = find_closest_note(maxFreq)
        signal_power = (np.linalg.norm(windowSamples, ord=2)**2) / len(windowSamples)
        if signal_power < power_threshhold:
            closestNote = ("REST")
        currentSong.append(closestNote)
        displayNotes = []
        for i in range(12, 1, -1):
            try:
                displayNotes.append(currentSong[-i])
            except:
                pass
        display(displayNotes)
    else:
        print('no input')
        
        



#runs a single channel input till it has blocksize amount of data
#then it runs callback with the data it has received
try:
    with sd.InputStream(channels=1, callback=callback,
                        blocksize=window_step,
                        samplerate=samp_freq):
        #makes it run infinitely
        while True:
            #ending and saving
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    passes = int(math.ceil(len(currentSong)/12))
                    os.makedirs("songs/" + songName)
                    for i in range(0, passes):
                        saveNotes = []
                        for k in range(0, 12):
                            try:
                                saveNotes.append(currentSong[(i*12)+k])
                            except:
                                pass
                        base_screen()
                        display(saveNotes)
                        name = (songName + "_" + str(i+1) + ".jpg")
                        directory = ("songs/" + songName + "/" + name)
                        pygame.image.save(screen, directory)
                    pygame.quit() ; sys.exit()
            pass
except Exception as e:
    print(str(e))
    print("Your make might not be plugged in. give it another go")
