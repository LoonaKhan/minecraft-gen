"""
MESH-STYLE WORLD GENERATION

Developer: MON-Emperor
Date: 2021-08-29

A 2d minecraft-like world generator
"""
from globvars import *
from utils.pygame_utils import *
from utils.system.sys_info import *
import os

window = create_window(resolution=(sc_w,sc_h),caption="Mesh world gen")
running = True

loaded_chunks = {}
while running:
    #checking the exit conditions
    exit_conditions("Escape")

    mouse_coords = mouse.get_pos(); p_coords = [mouse_coords[0]-mid_x, mouse_coords[1]-mid_y] #gets mouse coords

    cur_chunk = get_current_chunk(p_coords) #gets the current chunk. based on the mouse coords

    #deletes chunks that arent in render distance
    bad_chunks = []
    for loaded_chunk in loaded_chunks:
        #print("h")
        chunk_name = loaded_chunks[loaded_chunk]["number"] #get the name of the chunk
        in_render_distance = is_in_render_distance(chunk_name, cur_chunk)
        if not in_render_distance: bad_chunks.append(loaded_chunk)
    for bad_chunk in bad_chunks:
        loaded_chunks.pop(bad_chunk); bad_chunks.remove(bad_chunk)


    #determine what chunks to load into ram
    surrounding_chunks = return_chunks(cur_chunk)
    for surrounding_chunk in surrounding_chunks:
        if f"{surrounding_chunk}" not in loaded_chunks: #if its not loaded into ram
            try: chunk_data = load_json(f"chunks/{surrounding_chunk}.json") #searches the chunk folders for the specific chunk
            except:chunk_data = gen_chunk(surrounding_chunk) #if the file does not exist, create it

            loaded_chunks[f"{chunk_data['number']}"] = chunk_data #add the chunk data into ram



    #renders the chunks
    for loaded_chunk in loaded_chunks:
        loaded_chunk = loaded_chunks[loaded_chunk]
        render_chunk(loaded_chunk, window)

    # all HUD elements
    show_fps(window); show_memory(os.getpid(), window)
    render_text(f"Coords: {p_coords}", window, (10, 70))
    render_text(f"Chunk: {cur_chunk}", window, (10, 100))

    #update screen
    update_screen(window, FPS, Colours.black)