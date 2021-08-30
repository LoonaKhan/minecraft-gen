from utils.json_utils import *
from utils.pygame_utils import *
from random import choice
import pygame
from utils.system.sys_info import mid_x, mid_y
CHUNK_SIZE = 16

RENDER_DISTANCE = 8

def gen_list(size, array, base):
    if size == base: array.append(size);return array

    else:
        list = gen_list(size - 1, array, base)
        array.append(size); return array

def get_current_chunk(pos:list[int], chunk_size=CHUNK_SIZE):
    """
    Gets the current chunk.

    Takes the current coordinates and divides it by the chunk size. it casts the result to an integer and returns it.

    Examples:
        >>>pos=[16,16]
        >>>get_current_chunk(pos)
        [1,1]

        >>>pos=[5,4]
        >>>get_current_chunk(pos)
        [0,0]
    """
    chunk = [int(pos[0]/chunk_size), int(pos[1]/chunk_size)]
    return chunk

def gen_chunk(chunk, path="chunks/"):
    """
    Generates a chunk.

    takes in the chunk number, and then generates a json file for said chunk containing all the chunk properties
    Chunk properties:
        number = the chunk number. equal to :param chunk:   eg: [12,5].
        colour = the colour all blocks in the chunk are coloured. meant to distinguish one chunk from the next
        reference = the chunk origin relative to the global coordinates. all other chunk blocks are relative to this
        blocks = all the blocks in the chunk. each chunk has chunk coordinates relative to the reference.
    """

    # creates the file
    file_path = path + str(chunk) + ".json"
    chunk_data = create_json(file_path)

    c = Colours; colours = [
        c.red,
        c.blue,
        c.green,
        c.gray,
        c.yellow,
        c.orange,
        c.brown,
        c.pink,
        c.purple,
        c.light_blue,
        c.light_red,
        c.light_green
    ] #generates all the possible colours and then chooses a colour to draw the chunk in
    colour = choice(colours)

    chunk_data["number"] = chunk #number of the chunk if we need it
    chunk_data["colour"] = colour
    chunk_data["reference"] = [chunk[0]*CHUNK_SIZE, chunk[1]*CHUNK_SIZE] #reference block
    chunk_data["blocks"] = {}; blocks = chunk_data["blocks"]

    #generates all the blocks
    i=0
    for x in range(0,16):
        for y in range(0,16):
            i+=1
            blocks[f"block{i}"] = {}; block = blocks[f"block{i}"]
            block["coords"] = [x,y] #set the block's chunk coordinates

    update_json(file_path,chunk_data) #save the file
    return chunk_data #load it into ram

def render_chunk(chunk, window):
    """
    Renders a chunk.

    use the reference block coords and each block's chunk coords to draw them as pygame rects of a certain colour.
    each 1 pixel in size.
    """
    reference = chunk["reference"] #reference coords
    colour = chunk["colour"]
    blocks = chunk["blocks"]
    for block in blocks:
        block_coords = blocks[block]["coords"] #gets the chunk coords for each block
        abs_coords = [reference[0]+block_coords[0]+mid_x, reference[1]+block_coords[1]+mid_y] #position of the block
        pygame.draw.rect(window,colour,(abs_coords[0], abs_coords[1],1,1))

def return_chunks(chunk, render_distance=RENDER_DISTANCE):
    chunks = []
    for chunk_x in range(-render_distance,render_distance+1):
        for chunk_y in range(-render_distance,render_distance+1):
            new_chunk = [chunk[0]+chunk_x, chunk[1]+chunk_y]
            chunks.append(new_chunk)

    return chunks

def is_in_render_distance(chunk1, chunk2, render_distance=RENDER_DISTANCE):
    """
    Determines if 2 chunks are within render distance of eachother.

    takes chunk1 and chunk2 and compares them. if either of their elements are not within render distance of eachother,
    it returns False. otherwise, True.
    """
    if abs(chunk1[0] - chunk2[0])>render_distance or abs(chunk1[1] - chunk2[1])>render_distance:
        return False
    return True