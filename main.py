import enum
from re import M
from numpy import insert, sort
import math
import pygame
import random

pygame.init()

class DrawInfomation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0, 255, 0 
    RED = 255, 0, 0
    BLUE = 0,0,255
    BACKGROUND_COLOR = WHITE
    
    GRADIENTS = [
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    FONT = pygame.font.SysFont('comicsans',15)
    LARGE_FONT = pygame.font.SysFont('comicsans',20)
  
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self,width,height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height-self.TOP_PAD)/ (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    
    title = draw_info.LARGE_FONT.render("{} - {}".format(algo_name, 'Ascending' if ascending else 'Descending') , 1, draw_info.GREEN if ascending else draw_info.RED)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending | UP - Faster | DOWN - Slower" , 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.FONT.render("I(i) - InsertionSort | S - SelectionSort | B - BubbleSort" , 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i%3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window,color,(x,y, draw_info.block_width,draw_info.height))

    if clear_bg:
        pygame.display.update()    
def generate_starting_list(n,min_val,max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst    
    n = len(lst)
    update = True
    while(update == True and n>1):
        update = False
        for i in range(len(lst)-1):
            if (lst[i+1] < lst[i] and ascending) or (lst[i+1] > lst[i] and not ascending):
                lst[i],lst[i+1] = lst[i+1],lst[i]
                update = True
                draw_list(draw_info,{i: draw_info.GREEN, i+1: draw_info.RED}, True)
                yield True
        n-= 1
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(1,n):
        
        
        
        while i>0 and ((lst[i]<lst[i-1] and ascending) or (lst[i]>lst[i-1] and not ascending)):
                lst[i],lst[i-1] = lst[i-1],lst[i]
                i -= 1
                draw_list(draw_info,{i: draw_info.GREEN, i+1: draw_info.RED}, True)
                yield True
def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst)
  
    for i in range(n-1):
        holder = i
        for j in range(i,n):
            if (lst[j]< lst[holder] and ascending) or (lst[j] > lst[holder] and not ascending):
                holder = j
                draw_list(draw_info,{i: draw_info.GREEN, j: draw_info.RED, holder: draw_info.BLUE}, True)
                yield True 
        lst[i],lst[holder] = lst[holder],lst[i]



def main():
    FPS = 60
    run = True
    n = 50
    min_val = 0
    max_val = 100
    clock = pygame.time.Clock()
    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInfomation(800,600,lst)
    sorting = False
    ascending = True
    
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

   
    
    while run:
        clock.tick(FPS)
        if sorting:
            try: 
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False 
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            
            elif event.key == pygame.K_a and sorting == False :
                ascending = True
                
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            
            elif event.key == pygame.K_DOWN and FPS - 20 >= 20:
                FPS -= 20
            elif event.key == pygame.K_UP and FPS + 20 <= 120:
                FPS += 20
            
            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and sorting == False:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

            
                

    
    pygame.quit()

if __name__ == "__main__":
    main()


