import pygame
from pygame import TEXTINPUT, mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

red1 = (255,106,106)
red2 = (139,58,58)
pink = (255,174,185)
brown = (139,87,66)
mistry = (238,213,210)
bro = (139,119,101)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Drum Machine: Beat Maker')
lable_font = pygame.font.Font('freesansbold.ttf',28)
medium_font = pygame.font.Font('freesansbold.ttf',21)

fps = 60 #framaerate
timer = pygame.time.Clock()
beats = 8
boxes = []
instruments = 6
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] #when nothing selected, it is not active
bpm = 240 #4 beats/sec
playing = True
act_len = 0
active_list = [1 for _ in range(instruments)]
act_beat = 0
beat_changed = True
active_list = [1 for _ in range(instruments)]
save_menu = False
load_menu = False

saved_beats = []
file = open('saved_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False
index = 100
#load_rectangle = True

#load in sounds
hi_hat = mixer.Sound('hi hat.WAV')
clap = mixer.Sound('clap.WAV')
crush = mixer.Sound('cymbal.WAV')
snare = mixer.Sound('snare.WAV')
kick = mixer.Sound('kick.WAV')
floor = mixer.Sound('tom.WAV')
pygame.mixer.set_num_channels(instruments*3)

def play_notes():
    for i in range(len(clicked)): #and active_list[i] == 1:
        if clicked[i][act_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crush.play()
            if i == 4:
                clap.play()
            if i == 5:
                floor.play()


#left and botton bar menu boxes and all the boxes
def draw_grid(clicks,beat, actives): 
    left_box = pygame.draw.rect(screen, red2, [0,0,200,HEIGHT-200])
    left_box_line = pygame.draw.rect(screen, mistry, [0,0,200,HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, red2, [0,HEIGHT-200, WIDTH, 200])
    
    boxes = []
    colors = [mistry,red1,mistry]

    hi_hat_text = lable_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30,30)) #draw on the screen

    snare_text = lable_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30,130)) #draw on the screen

    kick_text = lable_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(kick_text, (30,230)) #draw on the screen

    crash_text = lable_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30,330)) #draw on the screen

    clap_text = lable_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30,430)) #draw on the screen

    floor_text = lable_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_text, (30,530)) #draw on the screen

    for i in range(instruments):
        pygame.draw.line(screen, bro,(0,(i*100)+100), (200,(i*100)+100),3)
    
    #for active_list 
    
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = red1
            else:
                if actives[j] == 1:
                    color = brown
                else:
                    color = red2

            rect = pygame.draw.rect(screen, color, [i*((WIDTH-200)//beats)+200,(j*100), ((WIDTH-200)//beats),100])
            rect = pygame.draw.rect(screen, mistry, [i*((WIDTH-200)//beats)+200,(j*100), ((WIDTH-200)//beats),100],2)

            boxes.append((rect,(i,j))) #tuple for returning which beat it is, using i,j as a axis and y...

    active = pygame.draw.rect(screen, bro, [beat*((WIDTH-200)//beats) + 200, 0,((WIDTH-200)//beats),instruments*100],5,3)
    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, pink, [0,0,WIDTH,HEIGHT])
    menu_text = lable_font.render('SAVE MENU: Enter a name for current beat', True, brown)
    screen.blit(menu_text, (470,40))
    saving_btn = pygame.draw.rect(screen, red1, [WIDTH // 2 - 200, HEIGHT*0.75, 400, 100],0,5)
    saving_text = lable_font.render('Save Beat', True, brown)
    screen.blit(saving_text, (WIDTH//2-70,HEIGHT*0.75 + 30))
    
    exit_btn = pygame.draw.rect(screen,red1,[WIDTH-200,HEIGHT-100,180,90],0,5)
    exit_text = lable_font.render('Close',True,brown)
    screen.blit(exit_text, (WIDTH-169,HEIGHT-70))

    entry_rect = pygame.draw.rect(screen, red1, [400,210,600,100], 5, 5)
    entry_text = lable_font.render(f'{beat_name}',True,brown)

    if typing:
        pygame.draw.rect(screen, mistry, [402,212,595,95], 0, 5) #to show if you can type in names or not 

    screen.blit(entry_text, (430,250))

    return exit_btn,saving_btn,entry_rect

def draw_load_menu(index):

    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    #loaded_clicked = 0

    pygame.draw.rect(screen, pink, [0,0,WIDTH,HEIGHT])
    
    menu_text = lable_font.render('LOAD MENU: Select a beat to load', True, brown)
    screen.blit(menu_text, (470,40))
    loading_btn = pygame.draw.rect(screen, red1, [WIDTH // 2 - 200, HEIGHT-100, 400, 90],0,5)
    loading_text = lable_font.render('Load Beat', True, brown)
    screen.blit(loading_text, (630,HEIGHT-70))

    delete_btn = pygame.draw.rect(screen, red1, [20, HEIGHT-100, 180, 90], 0, 5)
    delete_text = lable_font.render('Delete Beat', True, brown)
    screen.blit(delete_text, (25,HEIGHT - 70))

    exit_btn = pygame.draw.rect(screen,red1,[WIDTH-200,HEIGHT-100,180,90],0,5)
    exit_text = lable_font.render('Close',True,brown)
    screen.blit(exit_text, (WIDTH-155,HEIGHT-70))
    
    #selected beat name become 'mistry' color background
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, mistry, [190, 100 + index*50, 1000, 50])

    #checking saved beats and show it
    for beat in range(len(saved_beats)):
        # display 10 saved beats name in one page, and display names
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beat + 1}', True, brown)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6 # name:_ has 6 spaces
            name_index_end = saved_beats[beat].index(', beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, brown)
            screen.blit(name_text, (240, 100 + beat * 50))
        
        # to select saved bpm, beats, and which one clicked
        if 0<= index < len(saved_beats) and beat == index:  #to select which one to load in
            if 0 <= index < len(saved_beats) and beat == index:
                beats_index_end = saved_beats[beat].index(', bpm:')
                loaded_beats = int(saved_beats[beat][name_index_end + 8:beats_index_end]) # +8 bc ', beats:' has 8 spaces
                bpm_index_end = saved_beats[beat].index(', selected:')
                loaded_bpm = int(saved_beats[beat][beats_index_end + 6:bpm_index_end]) # +6 bc ', bpm:' has 6 spaces

                loaded_clicks_string = saved_beats[beat][bpm_index_end + 14: -3]# ', selected: (('
                loaded_clicks_rows = list(loaded_clicks_string.split("], ["))

            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats,loaded_bpm,loaded_clicked]         
    entry_rect = pygame.draw.rect(screen,red1,[190,90,1000,600],5,5)

    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info

    



run = True
while run:
    timer.tick(fps)
    screen.fill(pink) #background

    boxes = draw_grid(clicked,act_beat, active_list)

    play_pause = pygame.draw.rect(screen, red1, [50, HEIGHT-150,200,100], 0, 5)
    play_text = lable_font.render('Play/Pause', True, bro)
    screen.blit(play_text, (70,HEIGHT - 130))

    if playing:
        play_text2 = medium_font.render('Playing', True, brown)
    
    else:
        play_text2 = medium_font.render('Paused', True, brown)
    screen.blit(play_text2, (70,HEIGHT - 100))
    #bpm stuff
    bpm_rect = pygame.draw.rect(screen, red1, [300,HEIGHT-150,200,100],0,5)
    bpm_text = medium_font.render('Beats Per Minute', True, brown)
    screen.blit(bpm_text, (308,HEIGHT-130))
    bpm_text2 = lable_font.render(f'{bpm}', True, brown)
    screen.blit(bpm_text2, (370,HEIGHT-100))
    bpm_add_rect = pygame.draw.rect(screen, red1, [510,HEIGHT-150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, red1, [510,HEIGHT-100, 48, 48], 0, 5)
    add_text = medium_font.render('+5', True, brown)
    sub_text = medium_font.render('-5', True, brown)
    screen.blit(add_text, (520, HEIGHT-140))
    screen.blit(sub_text, (520, HEIGHT-90))

    #beats stuff
    beats_rect = pygame.draw.rect(screen, red1, [600,HEIGHT-150,200,100],0,5)
    beats_text = medium_font.render('Beats In Loop', True, brown)
    screen.blit(beats_text, (618,HEIGHT-130))
    beats_text2 = lable_font.render(f'{beats}', True, brown)
    screen.blit(beats_text2, (680,HEIGHT-100))
    beats_add_rect = pygame.draw.rect(screen, red1, [810,HEIGHT-150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, red1, [810,HEIGHT-100, 48, 48], 0, 5)
    add_text = medium_font.render('+1', True, brown)
    sub_text = medium_font.render('-1', True, brown)
    screen.blit(add_text, (820, HEIGHT-140))
    screen.blit(sub_text, (820, HEIGHT-90))

    #Instrumrnts rects
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0,i*100),(200,100))
        instrument_rects.append(rect)

    #save and load stuff
    save_button = pygame.draw.rect(screen, red1, [900,HEIGHT-150,200,48],0,5)
    load_button = pygame.draw.rect(screen, red1, [900,HEIGHT-100,200,48],0,5)
    
    save_text = medium_font.render('Save Beats', True, brown)
    load_text = medium_font.render('Load Beats', True, brown)

    screen.blit(save_text, (920, HEIGHT-140))
    screen.blit(load_text, (920, HEIGHT-90))

    #cleat board
    clear_button = pygame.draw.rect(screen, red1, [1150,HEIGHT-150,200,100],0,5)
    clear_text = lable_font.render('Clear All', True, brown)
    screen.blit(clear_text, (1190, HEIGHT-120))

    if beat_changed:
        play_notes()
        beat_changed = False

    if save_menu:
        exit_button, saving_btn, entry_rectangle = draw_save_menu(beat_name, typing)

    if load_menu:
        exit_button,loading_btn,entry_rectangle, delete_btn,loaded_info = draw_load_menu(index)
    

    for event in pygame.event.get():  #to tract every event in in users cpnputer, mouse move, keyboard typr.
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos): #check the position of the selected box
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1 
        
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos) and playing:
                playing = False
            elif play_pause.collidepoint(event.pos) and not playing:
                playing = True
                act_beat = 0
                act_len = 0

            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5

            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)

            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)

            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            #instruments
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1

        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False

            if entry_rectangle.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50

            if save_menu:
                
                if saving_btn.collidepoint(event.pos):
                    file = open('saved_beats.txt', 'w') # w to write to it
                    saved_beats.append(f'name: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}\n')
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ''


            if load_menu:
                
                if delete_btn.collidepoint(event.pos):
                    if 0<= index<len(saved_beats):
                        saved_beats.pop(index)

                if loading_btn.collidepoint(event.pos):
                    if 0<=index<len(saved_beats):
                        beats = loaded_info[0]
                        bpm = loaded_info[1]
                        clicked = loaded_info[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
                print(beats, bpm, clicked)   
                
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name)>0 and typing: #check if user pressed backspace after typed name
                #removed the text
                beat_name = beat_name[:-1]

       

            

    beat_len = 3600//bpm

    if playing:
        if act_len < beat_len:
            act_len += 1
        else:
            act_len = 0
            if act_beat < beats-1:
                 act_beat+=1
                 beat_changed = True
            else:
                act_beat = 0
                beat_changed = True


    pygame.display.flip()
file = open('saved_beats.txt', 'w')
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()

pygame.quit()



