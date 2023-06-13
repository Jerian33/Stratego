import pygame, random, math, statistics, copy, sys, os

try:
    os.chdir(os.path.join(sys._MEIPASS,"StrategoAssets"))
except Exception:
    os.chdir(os.path.join(os.path.abspath("."),"StrategoAssets"))



WIDTH, HEIGHT = 1720, 1080
FPS = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("RedF.png")
pygame.display.set_caption('Stratego!!')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

MAP_SURF = pygame.transform.scale(pygame.image.load("map.jpg").convert(), (1000, 1000))
MAP = MAP_SURF.get_rect(topleft=(40,40))
TRAY_SURF = pygame.image.load("TrayBGSmall.png").convert_alpha()
TRAY = TRAY_SURF.get_rect(topleft=(1080, 90))
MENU_SURF = pygame.image.load("Stratego_Background.png").convert()
MENU = MENU_SURF.get_rect(center=(WIDTH/2,HEIGHT/2))

buffer = pygame.Surface(screen.get_size())
buffer.fill("Black")


ranks = {
    "2": {"Name": "Scout", "MaxCount": 8},
    "3": {"Name": "Miner", "MaxCount": 5},
    "4": {"Name": "Sergeant", "MaxCount": 4},
    "5": {"Name": "Scout", "MaxCount": 4},
    "6": {"Name": "Scout", "MaxCount": 4},
    "7": {"Name": "Major", "MaxCount": 3},
    "8": {"Name": "Colonel", "MaxCount": 2},
    "9": {"Name": "General", "MaxCount": 1},
    "10": {"Name": "Marshal", "MaxCount": 1},
    "B": {"Name": "Bomb", "MaxCount": 6},
    "S": {"Name": "Spy", "MaxCount": 1},
    "F": {"Name": "Flag", "MaxCount": 1}
}

image_library = {
    "Red": {},
    "Blue": {},
    "Frames": {},
    "RedLarge": {},
    "BlueLarge": {}
}

piece_counter = {
    "Red": {},
    "Blue": {}
}

total_pieces_left = 40

image_library["Red"]["Blank"] = pygame.transform.scale(pygame.image.load("RedBlank.png").convert_alpha(), (90, 90))
image_library["Blue"]["Blank"] = pygame.transform.scale(pygame.image.load("BlueBlank.png").convert_alpha(), (90, 90))
image_library["Red"]["Victory"] = pygame.image.load("VictoryR.png").convert_alpha()
image_library["Blue"]["Victory"] = pygame.image.load("VictoryB.png").convert_alpha()
image_library["RedLarge"]["Blank"] = pygame.transform.scale(pygame.image.load("RedBlank.png").convert_alpha(), (120, 120))
image_library["BlueLarge"]["Blank"] = pygame.transform.scale(pygame.image.load("BlueBlank.png").convert_alpha(), (120, 120))
highlighter = pygame.image.load("Highlight.png").convert_alpha()
shadow = pygame.image.load("PieceShadow.png").convert_alpha()
gold_button_surf = pygame.transform.scale(pygame.image.load("GoldButton.png").convert_alpha(), (200, 106.95))
gold_button = gold_button_surf.get_rect(center=(WIDTH/2,HEIGHT/2))

for image in os.listdir():
    for rank in ranks:
        if "Red" in image:
            if rank+"." in image:
                image_library["Red"][rank] = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (90, 90))
                image_library["RedLarge"][rank] = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (120, 120))
        if "Blue" in image:
            if rank+"." in image:
                image_library["Blue"][rank] = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (90, 90))
                image_library["BlueLarge"][rank] = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (120, 120))

gold_frame_surf = pygame.image.load("GoldFrame.png").convert_alpha()
silver_frame_surf = pygame.image.load("SilverFrame.png").convert_alpha()
battle_frame_surf = pygame.image.load("BattleFrame.png").convert_alpha()
battle_swords_frame_surf = pygame.image.load("BattleSwordsFrame.png").convert_alpha()



for rank in ranks:
    piece_counter["Red"][rank] = ranks[rank]["MaxCount"]
    piece_counter["Blue"][rank] = ranks[rank]["MaxCount"]

bold_font = pygame.font.Font("LibBask_Bold.ttf", 40)
italic_font = pygame.font.Font("LibBask_Ital.ttf", 28)
reg_font = pygame.font.Font("LibBask_Reg.ttf", 18)
counter_font = pygame.font.Font("LibBask_Bold.ttf", 20)

setup_text1 = bold_font.render("Choose your side!", True, "Black")
st_Red_Choice1 = reg_font.render("You have chosen:", True, "Black")
st_Red_Choice2 = bold_font.render("Red!", True, "Red")
st_Red_Choice3 = reg_font.render("You will go first. Place your army!", True, "Black")


st_Blue_Choice1 = reg_font.render("You have chosen:", True, "Black")
st_Blue_Choice2 = bold_font.render("Blue!", True, "Blue")
st_Blue_Choice3 = reg_font.render("You will go second. Place your army!", True, "Black")

blue_attacker_text_render = italic_font.render("Attacker", True, "Blue")
blue_defender_text_render = italic_font.render("Defender", True, "Blue")
red_attacker_text_render = italic_font.render("Attacker", True, "Red")
red_defender_text_render = italic_font.render("Defender", True, "Red")
red_winner_text_render = italic_font.render("RED WINS!!", True, "Red")
blue_winner_text_render = italic_font.render("BLUE WINS!!", True, "Blue")
no_winner_text_render = italic_font.render("MUTUAL DESTRUCTION", True, "Black")


attacker_x, defender_x, winner_x, text_y, battle_piece_y = TRAY.left+(TRAY.width*.25), TRAY.left+(TRAY.width*.75), TRAY.left+(TRAY.width*.5), 240, 360
blue_attacker_text = blue_attacker_text_render.get_rect(center=(attacker_x, text_y))
blue_defender_text = blue_defender_text_render.get_rect(center=(defender_x, text_y))
red_attacker_text = red_attacker_text_render.get_rect(center=(attacker_x, text_y))
red_defender_text = red_defender_text_render.get_rect(center=(defender_x, text_y))
red_winner_text = red_winner_text_render.get_rect(center=(winner_x, text_y))
blue_winner_text = blue_winner_text_render.get_rect(center=(winner_x, text_y))
no_winner_text = no_winner_text_render.get_rect(center=(winner_x, text_y))


red_choice_rect = image_library["Red"]["F"].get_rect(center=(1280, 600))
blue_choice_rect = image_library["Blue"]["F"].get_rect(center=(1480,600))


play_game_text = bold_font.render("Play!", True, "Black")



BOARD = [[None]*10 for _ in range(10)]
for row_ind, row in enumerate(BOARD):
    if row_ind in [4, 5]:
        for col_ind, col in enumerate(row):
            if col_ind in [2, 3, 6, 7]:
                BOARD[row_ind][col_ind] = "W"


key_maps = {
    pygame.K_0: '10',
    pygame.K_1: '10',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_KP0: '10',
    pygame.K_KP1: '10',
    pygame.K_KP2: '2',
    pygame.K_KP3: '3',
    pygame.K_KP4: '4',
    pygame.K_KP5: '5',
    pygame.K_KP6: '6',
    pygame.K_KP7: '7',
    pygame.K_KP8: '8',
    pygame.K_KP9: '9',
    pygame.K_f: 'F',
    pygame.K_b: 'B',
    pygame.K_s: 'S',
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_SPACE: "confirm",
    pygame.K_RETURN: "confirm"
}

key_commands = ["left", "right", "up", "down", "confirm"]



player_side = ""
phase = "MainMenu"


main_menu_begun = False
def mainMenu():
    global main_menu_begun
    screen.fill("Black")
    screen.blit(MENU_SURF, MENU)
    screen.blit(gold_button_surf, gold_button)
    screen.blit(play_game_text, play_game_text.get_rect(center=(WIDTH/2,HEIGHT/2)))
    main_menu_begun = True

def mainMenuEvents(mouse_pos):
    global phase
    if event.type == pygame.MOUSEBUTTONDOWN:
        gold_button.collidepoint(mouse_pos)
        phase = "Setup"



setup_begun = False
def beginSetup():
    global setup_begun
    screen.fill("Black")
    screen.blit(MAP_SURF, MAP)
    screen.blit(TRAY_SURF, TRAY)
    screen.blit(setup_text1, setup_text1.get_rect(center=(1380, 500)))
    screen.blit(image_library["Red"]["F"], red_choice_rect)
    screen.blit(image_library["Blue"]["F"], blue_choice_rect)
    setup_begun = True

def setupEvents():
    global player_side
    if event.type == pygame.MOUSEBUTTONDOWN:
        if red_choice_rect.collidepoint(event.pos):
            player_side = "Red"
        elif blue_choice_rect.collidepoint(event.pos):
            player_side = "Blue"

def Setup():
    global phase, player_side, player_turn
    screen.fill("Black")
    screen.blit(MAP_SURF, MAP)
    screen.blit(TRAY_SURF, TRAY)
    if player_side == "Red":
        screen.blit(st_Red_Choice1, st_Red_Choice1.get_rect(center=(1380, 500)))
        screen.blit(st_Red_Choice2, st_Red_Choice2.get_rect(center=(1380, 540)))
        screen.blit(st_Red_Choice3, st_Red_Choice3.get_rect(center=(1380, 575)))
    elif player_side == "Blue":
        screen.blit(st_Blue_Choice1, st_Blue_Choice1.get_rect(center=(1380, 500)))
        screen.blit(st_Blue_Choice2, st_Blue_Choice2.get_rect(center=(1380, 540)))
        screen.blit(st_Blue_Choice3, st_Blue_Choice3.get_rect(center=(1380, 575)))
    player_turn = True if player_side == "Red" else False
    pygame.display.update()
    setupTray()
    pygame.time.wait(2000)
    phase = "Placement"



class PlacementPiece(pygame.sprite.Sprite):
    def __init__(self, pos, rank):
        super().__init__([placement_pieces])
        self.rank = rank
        self.image = image_library[player_side][rank]
        self.rect = self.image.get_rect(topleft=pos)


    def followMouse(self, pos):
        buffer.blit(shadow, ((pos[0] - 38), (pos[1] - 38)))
        self.rect.centerx, self.rect.centery = pos
        buffer.blit(self.image, self.rect)


class BattlePiece(pygame.sprite.Sprite):
    def __init__(self, is_winner, is_attacker, side, rank):
        super().__init__([battle_pieces])
        self.is_winner = is_winner
        self.is_loser = not is_winner
        self.is_attacker = is_attacker
        self.is_defender = not is_attacker
        self.side = side
        self.rank = rank
        self.using_blank_image = False if player_side == side else True
        self.image = image_library[player_side+"Large"][rank] if not self.using_blank_image else image_library[side+"Large"]["Blank"]
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(center=(attacker_x-100 if is_attacker else defender_x-100, battle_piece_y if is_attacker else battle_piece_y-100))
        self.target_position = None
        self.animation_speed = 5
        self.battle_anim_done = False
        self.result_anim_done = False
        self.loser_x = TRAY.left+100 if self.is_attacker else TRAY.right-100
        self.lost_shrink = False

    def begin_fight_anim(self):
        if not self.target_position:
            if self.is_attacker:
                self.target_position = (attacker_x, battle_piece_y)
            else:
                self.target_position = (defender_x, battle_piece_y)
        if close_enough(self.rect.center, self.target_position, 10):
            if self.side != player_side:
                self.image = image_library[self.side+"Large"][self.rank]
                self.image = pygame.transform.scale(self.image, (120, 120))
                self.rect = self.image.get_rect(center=(attacker_x if self.is_attacker else defender_x, battle_piece_y))
            self.target_position = None
            self.battle_anim_done = True
            
            
    def begin_result_anim(self, timer):

        if timer > battle_phase_2_timer:
            if self.is_winner:
                if not self.target_position:
                    self.target_position = (winner_x, battle_piece_y)
            else:
                if not self.target_position:
                    self.target_position = (self.loser_x, battle_piece_y)
                    if not self.lost_shrink:
                        self.image = image_library[self.side][self.rank]
                        self.lost_shrink = True
            if close_enough(self.rect.center, self.target_position, 10):
                self.rect.center = self.target_position
                self.target_position = None
                self.result_anim_done = True

        elif timer > battle_phase_1_timer:
            if not self.is_attacker:
                if self.using_blank_image:
                    self.image = image_library[self.side+"Large"][self.rank]
                    self.using_blank_image = False
        

class Piece(pygame.sprite.Sprite):
    def __init__(self, row, col, side, rank):
        super().__init__([pieces])
        self.row = row
        self.col = col
        self.rank = rank
        self.image = image_library[player_side][rank] if player_side == side else image_library[side]["Blank"]
        #self.image = image_library[side][rank]
        self.rect = self.image.get_rect(center=getTileCenter(row, col))
        self.side = side
        self.target_position = None
        self.animation_speed = 4
        self.atk_power = 11 if self.rank == "S" else int(self.rank) if self.rank != "F" and self.rank != "B" else 0
        self.def_power = 12 if self.rank == "B" else 1 if self.rank == "S" else int(self.rank) if self.rank != "F" else 0
        self.battle_result = ""
        self.has_moved = False

    def move(self, row, col):
        global selected_piece, comp_selected_piece, moving, player_turn, comp_move_chosen
        if not self.target_position:
            self.target_position = getTileCenter(row, col)
        if close_enough(self.rect.center, self.target_position, 5):
            self.target_position = None
            self.has_moved = True
            BOARD[self.row][self.col] = None
            self.row, self.col = row, col
            BOARD[self.row][self.col] = self
            self.rect = self.image.get_rect(center=getTileCenter(row, col))
            selected_piece, comp_selected_piece, moving = None, None, None
            player_turn = not player_turn
            comp_move_chosen = False

    def scout_atk_move(self, row, col):
        global moving
        if not self.target_position:
            row_diff, col_diff = row - self.row, col - self.col
            if row_diff > 1:
                self.target_position = getTileCenter(self.row+row_diff-1, col)
            elif row_diff < 1:
                self.target_position = getTileCenter(self.row+row_diff+1, col)
            elif col_diff > 1:
                self.target_position = getTileCenter(self.row, col+col_diff-1)
            elif col_diff < 1:
                self.target_position = getTileCenter(self.row, col+col_diff+1)
        if close_enough(self.rect.center, self.target_position, 5):
            self.target_position = None
            moving = None

counter_outer_width = 90
counter_outer_height = 40

counter_inner_width = 80
counter_inner_height = 30

TRAY_LAYOUT = [
    ["8", "9", "10", "F"],
    ["5", "6", "7", "B"],
    ["2", "3", "4", "S"],
]

tray_layout = []

placement_pieces = pygame.sprite.Group()
pieces = pygame.sprite.Group()
battle_pieces = pygame.sprite.Group()

battle_piece_holder = []

placement_piece_selected = None

available_moves = []

selected_piece = None
comp_selected_piece = None
attack_target = None


def setupTray():
    global tray_layout, placement_pieces, gold_button, complete_placement_text, complete_placement_rect
    complete_placement_text = italic_font.render("BATTLE!!", True, player_side)
    gold_button.center = (TRAY.x + TRAY.width/2, 400)
    complete_placement_rect = complete_placement_text.get_rect(center=(gold_button.center))

    tray_row_y = (TRAY.centery + 35)

    for row in TRAY_LAYOUT:
        tray_col_x = (TRAY.left + 50)
        for col in row:
            if row.index(col) == 3:
                tray_col_x += 20
            outer_y = tray_row_y + 92
            inner_y = outer_y + 5
            inner_x = tray_col_x + 5
            #Outer Rect
            outer_rect = pygame.Rect((tray_col_x, outer_y, counter_outer_width, counter_outer_height))
            #Inner Rect
            inner_rect = pygame.Rect((inner_x, inner_y, counter_inner_width, counter_inner_height))
            #Counter
            piece_count = piece_counter[player_side][col]
            piece_count_text = counter_font.render((f'x{piece_count}'), True, "Black")
            piece_count_rect = piece_count_text.get_rect(center=(tray_col_x+45, tray_row_y+112))
            #Piece Image
            PlacementPiece((tray_col_x, tray_row_y), col)
            tray_layout.append([col,outer_rect,inner_rect,piece_count_text,piece_count_rect])
            tray_col_x += 130
        tray_row_y += 135


def placementEvents(mouse_pos):
    global placement_piece_selected, clicked, pressed, piece_counter, phase
    x, y = mouse_pos
    if event.type == pygame.MOUSEBUTTONDOWN:
        if not clicked:
            clicked = True
            if not placement_piece_selected:
                if x > MAP.right and event.button == 1:
                    for piece in placement_pieces:
                        if piece.rect.collidepoint(mouse_pos) and piece_counter[player_side][piece.rank] > 0:
                            placement_piece_selected = PlacementPiece((mouse_pos[0]+45, mouse_pos[1]+45), piece.rank)
                            adjustTrayCounter(placement_piece_selected.rank, "Subtract", player_side)
                            break
                    if gold_button.collidepoint(mouse_pos):
                        if total_pieces_left == 0:
                            generateStartingPositions("Red" if player_side == "Blue" else "Blue")
                        else:
                            generateStartingPositions("Blue")
                            generateStartingPositions("Red")
                        phase = "Game"
                        clicked = False

                elif x < 1040 and y > 640 and event.button == 3:
                    for piece in pieces:
                        if piece.rect.collidepoint(mouse_pos):
                            pieces.remove(piece)
                            BOARD[piece.row][piece.col] = None
                            adjustTrayCounter(piece.rank, "Add", player_side)
                            placement_piece_selected = None
                            break
            elif placement_piece_selected:
                if x > MAP.right or event.button == 3:
                    placement_pieces.remove(placement_piece_selected)
                    adjustTrayCounter(placement_piece_selected.rank, "Add", player_side)
                    placement_piece_selected = None
                elif x < 1040 and y > 640 and event.button == 1:
                    placePiece(x, y, placement_piece_selected.rank)
    elif event.type == pygame.MOUSEBUTTONUP:
        clicked = False
    
    elif event.type == pygame.KEYDOWN:
        if not pressed:
            pressed = True
            if event.key in key_maps and key_maps[event.key] in ranks:
                key = key_maps[event.key]
            else:
                return
            if not placement_piece_selected:
                if x > MAP.right and piece_counter[player_side][key] > 0:
                    placement_piece_selected = PlacementPiece((mouse_pos[0]+45, mouse_pos[1]+45), key)
                    adjustTrayCounter(key, "Subtract", player_side)
                elif x < MAP.right and piece_counter[player_side][key] > 0:
                    placement_piece_selected = PlacementPiece((mouse_pos[0]+45, mouse_pos[1]+45), key)
                    adjustTrayCounter(key, "Subtract", player_side)
                    placePiece(x, y, key)
            elif placement_piece_selected:
                adjustTrayCounter(placement_piece_selected.rank, "Add", player_side)
                placement_pieces.remove(placement_piece_selected)
                placement_piece_selected = PlacementPiece((mouse_pos[0]+45, mouse_pos[1]+45), key)
                adjustTrayCounter(key, "Subtract", player_side)

    elif event.type == pygame.KEYUP:
        pressed = False



def drawPlacementScreen(mouse_pos):
    buffer.fill("Black")
    buffer.blit(MAP_SURF, MAP)
    buffer.blit(TRAY_SURF, TRAY)
    for item in tray_layout:
        col, outer_rect, inner_rect, piece_count_text, piece_count_rect = item
        pygame.draw.rect(buffer, "Black", outer_rect, 0, 5)
        pygame.draw.rect(buffer, "Gray", inner_rect, 0, 5)
        buffer.blit(piece_count_text, piece_count_rect)
    placement_pieces.draw(buffer)
    pieces.draw(buffer)
    if placement_piece_selected == None:
            placementHighlight(mouse_pos)
    else:
        placement_piece_selected.followMouse(mouse_pos)
    if (total_pieces_left == 40 or total_pieces_left == 0) and not placement_piece_selected:
        buffer.blit(gold_button_surf, gold_button)
        buffer.blit(complete_placement_text, complete_placement_rect)
    screen.blit(buffer, (0, 0))

low_tier = ["2", "3", "4"]
mid_tier = ["5", "6", "7"]
high_tier = ["8", "9", "10", "S"]

def generateStartingPositions(side):
    global piece_counter, BOARD, tray_layout
    board = [[None]*10 for _ in range(4)]
    rows = [i for i in range(4)]
    cols = [i for i in range(10)]

    # FLAG

    flag_row = random.choices(rows, [0, .05, .625, .325])[0]
    flag_col = random.choices(cols, [.05, .06, .14, .14, .06, .06, .14, .14, .06, .05])[0]
    board[flag_row][flag_col] = "F"
    if flag_row != 3:
        if flag_col != cols[0] and flag_col != cols[-1]:
            flag_circle = [[flag_col-1, flag_col, flag_col+1] for _ in range(flag_row-1, flag_row+2)]
        elif flag_col == cols[0]:
            flag_circle = [[flag_col, flag_col+1] for _ in range(flag_row-1, flag_row+2)]
        elif flag_col == cols[-1]:
            flag_circle = [[flag_col-1, flag_col] for _ in range(flag_row-1, flag_row+2)]
    else:
        if flag_col != cols[0] and flag_col != cols[-1]:
            flag_circle = [[flag_col-1, flag_col, flag_col+1] for _ in range(flag_row-1, flag_row+1)]
        elif flag_col == cols[0]:
            flag_circle = [[flag_col, flag_col+1] for _ in range(flag_row-1, flag_row+1)]
        elif flag_col == cols[-1]:
            flag_circle = [[flag_col-1, flag_col] for _ in range(flag_row-1, flag_row+1)]
    flag_circle[1].remove(flag_col)

    # BOMBS
    flag_bombs_amount = random.choices([i+1 for i in range(6)], [.02, .2, .33, .33, .1, .02])[0]

    row_bomb_ratio = [.05, .22, .18, .06]
    column_favorability = {3: .05, 2: .1, 1: .15, 0: .5}

    while flag_bombs_amount > 0:
        for row_ind, row in enumerate(flag_circle, flag_row-1):
            bomb_place_ratio = row_bomb_ratio[row_ind]
            negative_adjuster = 0
            for col in row:
                bomb_place_ratio = row_bomb_ratio[row_ind] - negative_adjuster
                
                col_diff = abs(col-flag_col)
                if 0 <= col_diff <= 3:
                    bomb_place_ratio += column_favorability[col_diff]
                if not board[row_ind][col]:
                    if randomBoolean(bomb_place_ratio):
                        board[row_ind][col] = "B"
                        negative_adjuster -= .04
                        piece_counter[side]["B"] -= 1
                        flag_bombs_amount -= 1
                if flag_bombs_amount == 0:
                    break
            if flag_bombs_amount == 0:
                break

    row_bomb_ratio = [.03, .1, .08, .03]
    

    while piece_counter[side]["B"] > 0:
        for row_ind, row in enumerate(board):
            bomb_place_ratio = row_bomb_ratio[row_ind]
            negative_adjuster = 0
            for col_ind, col in enumerate(row):
                bomb_place_ratio = row_bomb_ratio[row_ind] - negative_adjuster
                col_diff = abs(col_ind-flag_col)
                if 0 <= col_diff <= 3:
                    bomb_place_ratio += column_favorability[col_diff]
                if randomBoolean(bomb_place_ratio):
                    if not board[row_ind][col_ind]:
                        board[row_ind][col_ind] = "B"
                        piece_counter[side]["B"] -= 1
                        negative_adjuster -= .01
                if piece_counter[side]["B"] == 0:
                    break
            if piece_counter[side]["B"] == 0:
                break

    pool = [rank for rank, subdict in ranks.items() for _ in range(subdict["MaxCount"]) if rank != "F" and rank != "B"]

    high_tier_tracker = []
    
    while pool:
        for row_ind, row in enumerate(board):
            for col_ind, col in enumerate(row):
                if not board[row_ind][col_ind]: 
                    tier_ratios = [.7, .2, .1]
                    for high_row, high_col in high_tier_tracker:
                        if high_row-1 <= row_ind <= high_row+1:
                            tier_ratios[2] *= .9
                        if high_col-1 <= col_ind <= high_col+1:
                            tier_ratios[2] *= .65
                    if flag_row-1 <= row_ind <= flag_row+1:
                        tier_ratios[2] *= 1.75
                        tier_ratios[1] *= 1.25
                    if flag_col-1 <= col_ind <= flag_col+1:
                        tier_ratios[2] *= 2.5
                        tier_ratios[1] *= 1.75

                    low_selection_available = [rank for rank in pool if rank in low_tier]
                    if not low_selection_available:
                        tier_ratios[0] = 0
                    mid_selection_available = [rank for rank in pool if rank in mid_tier]
                    if not mid_selection_available:
                        tier_ratios[1] = 0
                    high_selection_available = [rank for rank in pool if rank in high_tier]
                    if not high_selection_available:
                        tier_ratios[2] = 0

                    tier = random.choices(["low", "mid", "high"], [ratio/sum(tier_ratios) for ratio in tier_ratios])[0]
                    if tier == "low":
                        selection = random.choice(low_selection_available)
                    elif tier == "mid":
                        selection = random.choice(mid_selection_available)
                    elif tier == "high":
                        selection = random.choice(high_selection_available)

                    board[row_ind][col_ind] = selection
                    piece_counter[side][selection] -= 1
                    pool.remove(selection)
                    if not pool:
                        break
            if not pool:
                break

    if side == player_side:
        for row_ind, row in enumerate(board):
            for col_ind, col in enumerate(row):
                if col:
                    BOARD[row_ind+6][col_ind] = Piece(row_ind+6, col_ind, side, col)
    else:
        for sublist in board:
            sublist.reverse()
        board.reverse()

        for row_ind, row in enumerate(board):
            for col_ind, col in enumerate(row):
                if col:
                    BOARD[row_ind][col_ind] = Piece(row_ind, col_ind, side, col)
    if total_pieces_left == 40:
        for team in piece_counter:
            for rank in piece_counter[team]:
                if rank != "B":
                    piece_counter[team][rank] = 0
                    index = [item[0] for item in tray_layout].index(rank)
                    tray_layout[index][3] = counter_font.render((f'x{0}'), True, "Black")


map_buffer = pygame.Surface((1080, 1080))
map_buffer.fill("Black")

tray_buffer = pygame.Surface((640, 1080))
tray_buffer.fill("Black")


def gameEvents(mouse_pos):
    global selected_piece, attack_target, piece_counter, clicked, pressed
    x, y = mouse_pos
    if event.type == pygame.MOUSEBUTTONDOWN:
        if not clicked:
            clicked = True
            if x < MAP.right and event.button == 1 and not moving and not battling:
                determineGameClick(*getBoardTileFromCoords(x, y))
            elif event.button == 3:
                selected_piece = None

    elif event.type == pygame.MOUSEBUTTONUP:
        clicked = False
    
    elif event.type == pygame.KEYDOWN:
        if not pressed:
            pressed = True
            if event.key in key_maps and key_maps[event.key] in key_commands and not moving and not battling:
                key = key_maps[event.key]

    elif event.type == pygame.KEYUP:
        pressed = False


comp_known_pieces = []

def getCompMove():
    global moving, comp_move_chosen, comp_selected_piece, phase
    comp_move_chosen = True
    comp_moves = []
    comp_pieces = [piece for piece in pieces if piece.side != player_side]
    comp_pieces_remaining = 40 - sum(piece_counter["Red" if player_side == "Blue" else "Blue"].values())
    player_pieces_remaining = 40 - sum(piece_counter[player_side].values())
    for piece in comp_pieces:
        moves = getAvailableMoves(piece)
        if moves:
            for move in moves:
                score = 5
                row, col, type = move[0], move[1], move[2]
                if type == "Move" and row > piece.row:
                    score += 30
                if type == "Move" and comp_known_pieces:
                    for known_piece in comp_known_pieces:
                        actual_row_distance, new_row_distance = abs(known_piece.row-piece.row), abs(known_piece.row-row)
                        actual_col_distance, new_col_distance = abs(known_piece.col-piece.col), abs(known_piece.col-col)
                        if actual_row_distance + actual_col_distance <= 3:
                            is_closer_row = actual_row_distance > new_row_distance
                            is_closer_col = actual_col_distance > new_col_distance
                            if piece.atk_power > known_piece.def_power:
                                if is_closer_row or is_closer_col:
                                    score += 40 if known_piece.rank in high_tier else 25 if known_piece.rank in mid_tier else 10
                            elif piece.rank == "3" and known_piece.rank == "B":
                                if is_closer_row or is_closer_col:
                                    score += 100
                            if piece.def_power < known_piece.atk_power:
                                if not is_closer_row and not is_closer_col:
                                    score += 150 - 10*actual_row_distance if piece.rank in high_tier else 80 - 10*actual_row_distance if piece.rank in mid_tier else 15
                if type == "Attack":
                    blind_bomb_mod = ((3+piece_counter[player_side]["B"])/6)
                    blind_mod = (comp_pieces_remaining//10) + 2
                    score += 10
                    defender = BOARD[row][col]
                    if defender in comp_known_pieces:
                        if piece.rank == "3" and defender.rank == "B":
                            score += 400
                        else:
                            if piece.atk_power > defender.def_power:
                                score += 500 if defender.rank in high_tier else 300 if defender.rank in mid_tier else 200
                            elif piece.atk_power < defender.def_power:
                                score = 1
                            else:
                                if comp_pieces_remaining > player_pieces_remaining:
                                    score += 20*blind_mod if defender.rank in high_tier else 10*blind_mod if defender.rank in mid_tier else 5*blind_mod
                                else:
                                    score += 16*blind_mod if defender.rank in high_tier else 8*blind_mod if defender.rank in mid_tier else 5*blind_mod
                    else:
                        if piece.rank == "3":
                            if row >= 7:
                                blind_bomb_mod = ((6+piece_counter[player_side]["B"])/6)
                            else:
                                blind_mod = 1
                            score *= blind_mod*blind_bomb_mod
                        elif piece.rank in high_tier:
                            if defender.has_moved:
                                score += 250
                            else:
                                blind_bomb_mod = ((1+piece_counter[player_side]["B"])/6)
                                score *= blind_mod*blind_bomb_mod
                        else:
                            score *= blind_mod
                score = int(score) if score > 0 else 1
                comp_moves.append((move, piece, score))
    if not comp_moves:
        phase = ("End", player_side, "Out of Moves")
    #for mve, pce, scr in comp_moves:
        #print(f'Dest: {mve[0]},{mve[1]} | Type: {mve[2]} | Rank: {pce.rank} | Score: {scr}')
    scores = [s[2] for s in comp_moves]
    scores = [s*(s//statistics.median(scores)) for s in scores]
    chosen_move, comp_selected_piece, chosen_score = random.choices(comp_moves, [s/sum(scores) for s in scores])[0]
    pygame.time.wait(1200)
    move_row, move_col, move_type = chosen_move
    #print(f'CHOSEN Move Type: {move_type} | Move Score: {chosen_score} | Move Dest: {move_row},{move_col} | Piece Rank/Pos: {comp_selected_piece.rank}/({comp_selected_piece.row},{comp_selected_piece.col})')
    if move_type == "Move":
        moving = (comp_selected_piece, move_row, move_col)
    elif move_type == "Attack":
        determineBattleVariables(comp_selected_piece, BOARD[move_row][move_col])

bv_empty = {
    "WinningPiece": None,
    "LosingPieces": [],
    "AtkText": None,
    "DefText": None,
    "WinnerText": None,
    "VictorSpace": None
}
battle_variables = copy.deepcopy(bv_empty)
battling = False
def determineBattleVariables(attacker, defender):
    global battle_phase, battle_variables, battle_piece_holder, phase, moving

    battle_variables["VictorSpace"] = (defender.row, defender.col)

    battle_variables["AtkText"]  = (red_attacker_text_render, red_attacker_text) if attacker.side == "Red" else (blue_attacker_text_render, blue_attacker_text)
    battle_variables["DefText"] = (red_defender_text_render, red_defender_text) if defender.side == "Red" else (blue_defender_text_render, blue_defender_text)    

    if defender.rank == "F":
        phase = ("End", attacker.side, "Flag")
    elif attacker.rank == "3" and defender.rank == "B":
        battle_piece_holder.append(BattlePiece(is_winner=True, is_attacker=True, side=attacker.side, rank=attacker.rank))
        battle_piece_holder.append(BattlePiece(is_winner=False, is_attacker=False, side=defender.side, rank=defender.rank))
        battle_variables["WinningPiece"] = attacker
        battle_variables["LosingPieces"] = [defender]
        battle_variables["WinnerText"] = (red_winner_text_render, red_winner_text) if attacker.side == "Red" else (blue_winner_text_render, blue_winner_text)

    else:
        if attacker.atk_power > defender.def_power:
            battle_piece_holder.append(BattlePiece(is_winner=True, is_attacker=True, side=attacker.side, rank=attacker.rank))
            battle_piece_holder.append(BattlePiece(is_winner=False, is_attacker=False, side=defender.side, rank=defender.rank))
            battle_variables["WinningPiece"] = attacker
            battle_variables["LosingPieces"] = [defender]
            battle_variables["WinnerText"] = (red_winner_text_render, red_winner_text) if attacker.side == "Red" else (blue_winner_text_render, blue_winner_text)
        elif attacker.atk_power < defender.def_power:
            battle_piece_holder.append(BattlePiece(is_winner=False, is_attacker=True, side=attacker.side, rank=attacker.rank))
            battle_piece_holder.append(BattlePiece(is_winner=True, is_attacker=False, side=defender.side, rank=defender.rank))
            battle_variables["WinningPiece"] = defender
            battle_variables["LosingPieces"] = [attacker]
            battle_variables["WinnerText"] = (red_winner_text_render, red_winner_text) if defender.side == "Red" else (blue_winner_text_render, blue_winner_text)
        else:
            battle_piece_holder.append(BattlePiece(is_winner=False, is_attacker=True, side=attacker.side, rank=attacker.rank))
            battle_piece_holder.append(BattlePiece(is_winner=False, is_attacker=False, side=defender.side, rank=defender.rank))
            battle_variables["LosingPieces"] = [attacker, defender]
            battle_variables["WinnerText"] = (no_winner_text_render, no_winner_text)
    if attacker.rank == "2":
        moving = (attacker, defender.row, defender.col, True)
    battle_phase = 1

def endBattlePhase():
    global battle_phase, battle_variables, battling, battle_piece_holder, battle_pieces, pieces, moving, selected_piece, comp_selected_piece, player_turn, comp_move_chosen
    for piece in battle_variables["LosingPieces"]:
        adjustTrayCounter(piece.rank, "Add", piece.side)
        BOARD[piece.row][piece.col] = None
        pieces.remove(piece)
        if piece in comp_known_pieces:
            comp_known_pieces.remove(piece)
        del piece
    for piece in battle_pieces:
        battle_pieces.remove(piece)
        del piece
    if battle_variables["WinningPiece"]:
        winner = battle_variables["WinningPiece"]
        if winner.side == player_side:
            comp_known_pieces.append(winner)
        victory_row, victory_col = battle_variables["VictorSpace"]
        moving = (winner, victory_row, victory_col)
    else:
        selected_piece, comp_selected_piece, moving = None, None, None
        player_turn = not player_turn
        comp_move_chosen = False
    battle_phase = 0
    battle_variables = copy.deepcopy(bv_empty)
    battling = False
    battle_piece_holder = []
            
   
battle_phase = 0
battle_phase_1_timer = 1500
battle_phase_2_timer = 2200
battle_phase_3_timer = 3000

def drawBattleAnims(buffer):
    global battle_phase
    if battle_phase == 1:
        buffer.blit(*battle_variables["AtkText"])
        buffer.blit(*battle_variables["DefText"])
        for piece in battle_piece_holder:
            if not piece.battle_anim_done:
                piece.begin_fight_anim()
            if piece.target_position:
                animateMovePiece(piece)
        if all(piece.battle_anim_done for piece in battle_piece_holder):
            battle_phase = 2
    elif battle_phase == 2:
        battle_timer = (current_time-battle_start_time)
        if battle_timer < battle_phase_2_timer:
            buffer.blit(*battle_variables["AtkText"])
            buffer.blit(*battle_variables["DefText"])
        else:
            buffer.blit(*battle_variables["WinnerText"])
        for piece in battle_piece_holder:
            if not piece.result_anim_done:
                piece.begin_result_anim(battle_timer)
            if piece.target_position:
                animateMovePiece(piece)
        if battle_timer > battle_phase_3_timer:
            battle_phase = 3
    elif battle_phase == 3:
        buffer.blit(*battle_variables["WinnerText"])
        endBattlePhase()

        
    battle_pieces.draw(buffer)

def animateMovePiece(piece):
    piece_x, piece_y = piece.rect.center
    target_x, target_y = piece.target_position
    dx = (target_x - piece_x) / piece.animation_speed
    dy = (target_y - piece_y) / piece.animation_speed
    piece.rect.centerx += dx
    piece.rect.centery += dy

def drawGameMap(mouse_pos):
    x, y = mouse_pos
    map_buffer.fill("Black")
    map_buffer.blit(MAP_SURF, MAP)
    if not player_turn:
        if comp_selected_piece:
            if comp_selected_piece.target_position:
                animateMovePiece(comp_selected_piece)
    elif not selected_piece:
        if MAP.left < x < MAP.right and MAP.top < y < MAP.bottom:
            gameHighlight(mouse_pos)
    else:
        if selected_piece.target_position:
            animateMovePiece(selected_piece)
    pieces.draw(map_buffer)
    if selected_piece and not moving:
        if available_move_images:
            for surf, rect in available_move_images:
                map_buffer.blit(surf, rect)
        map_buffer.blit(gold_frame_surf, gold_frame_surf.get_rect(center=getTileCenter(selected_piece.row, selected_piece.col)))
    screen.blit(map_buffer, (0, 0))

def drawGameTray():
    buffer.fill("Black")
    buffer.blit(TRAY_SURF, TRAY)
    if battle_phase:
        drawBattleAnims(buffer)
    for item in tray_layout:
        col, outer_rect, inner_rect, piece_count_text, piece_count_rect = item
        pygame.draw.rect(buffer, "Black", outer_rect, 0, 5)
        pygame.draw.rect(buffer, "Gray", inner_rect, 0, 5)
        buffer.blit(piece_count_text, piece_count_rect)
    placement_pieces.draw(buffer)
    screen.blit(buffer, (0, 0))


def adjustTrayCounter(rank, operation, side):
    global piece_counter, tray_layout, total_pieces_left
    if operation == "Add":
        piece_counter[side][rank] += 1
        total_pieces_left += 1
    else:
        piece_counter[side][rank] -= 1
        total_pieces_left -= 1
    piece_count = piece_counter[side][rank]
    index = [item[0] for item in tray_layout].index(rank)
    tray_layout[index][3] = counter_font.render((f'x{piece_count}'), True, "Black")


def placementHighlight(mouse_pos):
    x, y = mouse_pos
    if x > 1080 and y > 540:
        for piece in placement_pieces:
            if piece.rect.collidepoint(mouse_pos) and piece_counter[player_side][piece.rank] > 0:
                buffer.blit(highlighter, highlighter.get_rect(center=piece.rect.center))

def gameHighlight(mouse_pos):
    global map_buffer
    row, col = getBoardTileFromCoords(*mouse_pos)
    if BOARD[row][col] != None:
        if BOARD[row][col] != "W":
            if BOARD[row][col].side == player_side:
                map_buffer.blit(highlighter, highlighter.get_rect(center=getTileCenter(row, col)))

def randomBoolean(ratio):
    return random.random() < ratio

def determineMove(row, col, moving_side):
    tile = BOARD[row][col]
    if tile == None:
        return (row, col, "Move")
    elif tile == "W":
        pass
    elif tile.side != moving_side:
        return (row, col, "Attack")

def getAvailableMoves(piece):
    global available_moves, available_move_images
    available_moves, available_move_images = [], []
    if piece.rank == "2":
        curr_row, curr_col = piece.row, piece.col
        limits = {"up": False, "down": False, "left": False, "right": False}
        for dist, _ in enumerate(range(10), 1):
            if not limits["up"]:
                up = determineMove(curr_row-dist, curr_col, piece.side) if curr_row-dist >= 0 else None
                if up:
                    available_moves.append(up)
                    if up[2] == "Attack":
                        limits["up"] = True
                else:
                    limits["up"] = True

            if not limits["down"]:
                down = determineMove(curr_row+dist, curr_col, piece.side) if curr_row+dist <= 9 else None
                if down:
                    available_moves.append(down)
                    if down[2] == "Attack":
                        limits["down"] = True
                else:
                    limits["down"] = True

            if not limits["left"]:
                left = determineMove(curr_row, curr_col-dist, piece.side) if curr_col-dist >= 0 else None
                if left:
                    available_moves.append(left)
                    if left[2] == "Attack":
                        limits["left"] = True
                else:
                    limits["left"] = True

            if not limits["right"]:
                right = determineMove(curr_row, curr_col+dist, piece.side) if curr_col+dist <= 9 else None
                if right:
                    available_moves.append(right)
                    if right[2] == "Attack":
                        limits["right"] = True
                else:
                    limits["right"] = True

    elif piece.rank == "F" or piece.rank == "B":
        pass
    
    else:
        for row_ind, row in enumerate(BOARD):
            for col_ind, col in enumerate(row):
                if col_ind == piece.col:
                    if piece.row-1 == row_ind or piece.row+1 == row_ind:
                        move = determineMove(row_ind, col_ind, piece.side)
                        if move:
                            available_moves.append(move)
                elif row_ind == piece.row:
                    if piece.col-1 == col_ind or piece.col+1 == col_ind:
                        move = determineMove(row_ind, col_ind, piece.side)
                        if move:
                            available_moves.append(move)



    if available_moves and player_turn:
        available_move_images = [(battle_swords_frame_surf if move_type == "Attack" else silver_frame_surf,
                            battle_swords_frame_surf.get_rect(center=(getTileCenter(move_row, move_col))) if move_type == "Attack"
                            else silver_frame_surf.get_rect(center=(getTileCenter(move_row, move_col))))
                            for move_row, move_col, move_type in available_moves]
        available_moves = [(row, col) for row, col, _ in available_moves]
    elif available_moves:
        return available_moves

moving = None
def determineGameClick(row, col):
    global selected_piece, attack_target, phase, moving
    tile = BOARD[row][col]
    if selected_piece and (row, col) in available_moves:
        if not tile:
            moving = (selected_piece, row, col)
        else:
            determineBattleVariables(selected_piece, tile)
    elif not tile:
        return False
    elif tile == "W":
        return False
    elif tile.side == player_side:
        selected_piece = tile
        getAvailableMoves(selected_piece)
        return True
    



def getBoardTileFromCoords(x, y):
    row = ((y - 40)//100)
    col = ((x - 40)//100)
    return row, col

def getTileCenter(row, col):
    x = col*100 + 40 + 50
    y = row*100 + 40 + 50
    return x, y

def close_enough(point1, point2, threshold):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= threshold


def placePiece(x, y, rank):
    global placement_piece_selected, piece_counter
    row, col = getBoardTileFromCoords(x, y)
    new_piece = Piece(row, col, player_side, rank)
    if not BOARD[row][col]:
        BOARD[row][col] = new_piece
        placement_pieces.remove(placement_piece_selected)
        placement_piece_selected = None
    else:
        old_rank = BOARD[row][col].rank
        pieces.remove(BOARD[row][col])
        BOARD[row][col] = new_piece
        placement_pieces.remove(placement_piece_selected)
        placement_piece_selected = PlacementPiece((mouse_pos[0]+45, mouse_pos[1]+45), old_rank)


def movePiece(piece, dest_row, dest_col, scout_atk=None):
    if scout_atk:
        piece.scout_atk_move(dest_row, dest_col)
    else:
        piece.move(dest_row, dest_col)


def quitApp():
    global phase
    if event.type == pygame.QUIT:
        phase = "Quit"
        pygame.quit()
        sys.exit()

player_turn = None
comp_move_chosen = False
running = True
clicked = False
pressed = False
while running:
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        quitApp()
        if phase == "MainMenu":
            mainMenuEvents(mouse_pos)
        elif phase == "Setup":
            setupEvents()
        elif phase == "Placement":
            placementEvents(mouse_pos)
        elif phase == "Game":
            if player_turn:
                gameEvents(mouse_pos)
            else:
                if not comp_move_chosen:
                    getCompMove()



    
    if phase == "MainMenu":
        if not main_menu_begun:
            mainMenu()
    elif phase == "Setup":
        if not setup_begun:
            beginSetup()
        if player_side != "":
            Setup()
    elif phase == "Placement":
        drawPlacementScreen(mouse_pos)
    elif phase == "Game":
        if moving:
            movePiece(*moving)
        if not battling:
            if battle_phase:
                battling = True
                battle_start_time = current_time
        drawGameTray()
        drawGameMap(mouse_pos)
    elif phase[0] == "End":
        screen.blit(image_library[phase[1]]["Victory"], (0, 0))
       
    elif phase == "Quit":
        running = False
    pygame.display.update()

    clock.tick(FPS)
