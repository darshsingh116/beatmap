import math
from typing import List, Tuple
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv

#setting data path
load_dotenv()
archive_path = os.getenv('ARCHIVE_PATH')


class OsuBeatmap:
    def __init__(self,hit_objects, timing_points  ,audio, split, folder, beatmapset_id, beatmap_id, approved, total_length, hit_length, version,
                 file_md5, diff_size, diff_overall, diff_approach, diff_drain, mode, count_normal, count_slider,
                 count_spinner, submit_date, approved_date, last_update, artist, artist_unicode, title, title_unicode,
                 creator, creator_id, bpm, source, tags, genre_id, language_id, favourite_count, rating, storyboard,
                 video, download_unavailable, audio_unavailable, playcount, passcount, packs, max_combo, diff_aim,
                 diff_speed, difficultyrating ,sliderMultiplier):
        self.hit_objects = hit_objects
        self.timing_points = timing_points 
        self.audio = audio
        self.split = split
        self.folder = folder
        self.beatmapset_id = beatmapset_id
        self.beatmap_id = beatmap_id
        self.approved = approved
        self.total_length = total_length
        self.hit_length = hit_length
        self.version = version
        self.file_md5 = file_md5
        self.diff_size = diff_size
        self.diff_overall = diff_overall
        self.diff_approach = diff_approach
        self.diff_drain = diff_drain
        self.mode = mode
        self.count_normal = count_normal
        self.count_slider = count_slider
        self.count_spinner = count_spinner
        self.submit_date = submit_date
        self.approved_date = approved_date
        self.last_update = last_update
        self.artist = artist
        self.artist_unicode = artist_unicode
        self.title = title
        self.title_unicode = title_unicode
        self.creator = creator
        self.creator_id = creator_id
        self.bpm = bpm
        self.source = source
        self.tags = tags
        self.genre_id = genre_id
        self.language_id = language_id
        self.favourite_count = favourite_count
        self.rating = rating
        self.storyboard = storyboard
        self.video = video
        self.download_unavailable = download_unavailable
        self.audio_unavailable = audio_unavailable
        self.playcount = playcount
        self.passcount = passcount
        self.packs = packs
        self.max_combo = max_combo
        self.diff_aim = diff_aim
        self.diff_speed = diff_speed
        self.difficultyrating = difficultyrating
        self.sliderMultiplier = sliderMultiplier

    def __repr__(self):
        return f"OsuBeatmap({self.title} - {self.artist})"


    
def process_hitobject(hitobject: str, uninherited_timingpointvar: int, inherited_timingpointvar: int, timing_points: List[str],sm:str) -> Tuple[List[str], int, int]:
    parts = hitobject.split(',')
    hit_type = int(parts[3])
    sm = float(sm)

    # Convert hit_type to a binary string
    binary_representation = bin(hit_type)[-4:]

    # Check the last three bits
    last_three_bits = binary_representation.zfill(3)  # Ensure it's always 3 bits long

    # Find indices of '1' bits
    indices_of_ones = [i for i, bit in enumerate(reversed(last_three_bits)) if bit == '1']

    #calc corresponding timing point
    timestamp = int(parts[2])
    timingpoint_for_this_hitobject = []
    
    if float(timing_points[inherited_timingpointvar][1])>0 :

        uninherited_timingpointvar = inherited_timingpointvar
        # inherited_timingpointvar += 1
    if inherited_timingpointvar+1 == len(timing_points):
        timingpoint_for_this_hitobject = timing_points[inherited_timingpointvar]
    else:
        if int(timing_points[inherited_timingpointvar+1][0]) < timestamp:
            while int(timing_points[inherited_timingpointvar+1][0]) < timestamp:
                inherited_timingpointvar += 1


        if int(timing_points[inherited_timingpointvar+1][0]) == timestamp:
            timingpoint_for_this_hitobject = timing_points[inherited_timingpointvar+1]
            inherited_timingpointvar += 1
        else:
            if inherited_timingpointvar == 0:
                timingpoint_for_this_hitobject = [timestamp,-100,0,0,0,0,0,0]
                # raise ValueError("Anomoly where starting ob dont have a timing point ... in beatmap.py line 79.")
            else:
                timingpoint_for_this_hitobject = timing_points[inherited_timingpointvar]
    

    #calc now
    # print(hitobject)
    # print(timingpoint_for_this_hitobject)

    uninherited_timingpoint_for_this_hitobject = timing_points[uninherited_timingpointvar]
    timingpoint_for_this_hitobject[1] = str(abs(float(timingpoint_for_this_hitobject[1])))

    footerListWithTimingPointsData = [float(value) for value in timingpoint_for_this_hitobject] + [float(value) for value in uninherited_timingpoint_for_this_hitobject]

    if 0 in indices_of_ones:
        # Handle hit objects of type 1 or 4
        if len(parts)==5:
            parts.append("0:0:0:0:")
        subpart = parts[5].split(":")
        subpart.pop()
        subpart = [int(i) for i in subpart]
        parts = [int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4])] + [0] * 8 + subpart + [0]
        return [[parts+footerListWithTimingPointsData] ,uninherited_timingpointvar,inherited_timingpointvar]  # Length 11
    
    elif 1 in indices_of_ones:
        # Handle hit objects of type 2 or 6 (slider)
        # slider_data = parts[5]
            #calc slider duration
        beatlen=float(timing_points[uninherited_timingpointvar][1])
        svm = (100.0/abs(float(timingpoint_for_this_hitobject[1])))
        length = float(parts[7])
        slider_duration_per_sliderpoint = (length / (sm * 100 * svm) * beatlen)
        split_slider_list = split_slider(hitobject,slider_duration_per_sliderpoint,timingpoint_for_this_hitobject)
        split_slider_with_footer = [sublist+footerListWithTimingPointsData for sublist in split_slider_list]
        return [split_slider_with_footer,uninherited_timingpointvar,inherited_timingpointvar]
    
    elif 3 in indices_of_ones:
        # Handle hit objects of type 8 or 12
        if len(parts)==6:
            parts.append("0:0:0:0:")
        subpart = parts[6].split(":")
        subpart.pop()
        subpart = [int(i) for i in subpart]
        return [[[int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4]),int(parts[5])]+ [0] * 7 +subpart+[0] + footerListWithTimingPointsData],uninherited_timingpointvar,inherited_timingpointvar]  # Pad to length 11
    
    else:
        print(hit_type)
        print(hitobject)
        raise ValueError("Anomoly where hit type is other tan 1,5,2,6,8,12 ... in beatmap.py line 141.")  # Return as-is if no special handling    


    
def parse_osu_file(file_path) -> Tuple[OsuBeatmap , List[str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = {}
        hit_objects = []
        timing_points  = []
        current_section = None
        uninherited_timingpointvar = 0
        inherited_timingpointvar = 0
        sliderMultiplier = 0
        hyperParamFooter = ["","","","","","","","","",]
        # inherit data
        for line in file:
            line = line.strip()
            if line.startswith('['):
                # Handle section headers
                current_section = line[1:-1]
                continue
            
            if current_section == 'HitObjects' and line:
                objs,uninherited_timingpointvar,inherited_timingpointvar = process_hitobject(line,uninherited_timingpointvar,inherited_timingpointvar,timing_points,sliderMultiplier)
                for l in objs:
                    hit_objects.append(l)
                continue
            
            if current_section == 'TimingPoints' and line:
                if(line == ""):
                    continue
                timing_points.append(line.split(','))
                

            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
                if key.strip() == 'StackLeniency':
                    hyperParamFooter[0] = (value.strip())
                    
                elif key.strip() == 'DistanceSpacing':
                    hyperParamFooter[1] = (value.strip())
                elif key.strip() == 'BeatDivisor':
                    hyperParamFooter[2] = (value.strip())
                elif key.strip() == 'HPDrainRate':
                    hyperParamFooter[3] = (value.strip())
                elif key.strip() == 'CircleSize':
                    hyperParamFooter[4] = (value.strip())
                elif key.strip() == 'OverallDifficulty':
                    hyperParamFooter[5] = (value.strip())
                elif key.strip() == 'ApproachRate':
                    hyperParamFooter[6] = (value.strip())
                elif key.strip() == 'SliderTickRate':
                    hyperParamFooter[7] = (value.strip())
                elif key.strip() == 'SliderMultiplier':
                    sliderMultiplier = (value.strip())
                    hyperParamFooter[8]=sliderMultiplier

    # Create an instance of OsuBeatmap using the parsed data
    return [OsuBeatmap(
        hit_objects=hit_objects,
        timing_points = timing_points, 
        audio=data.get('AudioFilename', ''),
        split='',  # Handle this if necessary
        folder='',  # Handle this if necessary
        beatmapset_id=int(data.get('BeatmapSetID', 0)),
        beatmap_id=int(data.get('BeatmapID', 0)),
        approved=int(data.get('Approved', 0)),  # This might be absent in the provided format
        total_length=int(data.get('PreviewTime', 0)),  # osu! files might use 'PreviewTime' or similar
        hit_length=int(data.get('HitLength', 0)),
        version=data.get('Version', ''),
        file_md5='',  # This might be absent in the provided format
        diff_size=float(data.get('CircleSize', 0)),
        diff_overall=float(data.get('OverallDifficulty', 0)),
        diff_approach=float(data.get('ApproachRate', 0)),
        diff_drain=float(data.get('HPDrainRate', 0)),
        mode=int(data.get('Mode', 0)),
        count_normal=0,  # This might be calculated or parsed separately
        count_slider=0,  # This might be calculated or parsed separately
        count_spinner=0,  # This might be calculated or parsed separately
        submit_date='',  # osu! files might not contain submit date
        approved_date='',  # osu! files might not contain approved date
        last_update='',  # osu! files might not contain last update date
        artist=data.get('Artist', ''),
        artist_unicode=data.get('ArtistUnicode', ''),
        title=data.get('Title', ''),
        title_unicode=data.get('TitleUnicode', ''),
        creator=data.get('Creator', ''),
        creator_id=0,  # This might be absent in the provided format
        bpm=float(data.get('BPM', 0)),
        source=data.get('Source', ''),
        tags=data.get('Tags', ''),
        genre_id=int(data.get('Genre', 0)),
        language_id=int(data.get('Language', 0)),
        favourite_count=0,  # This might be absent in the provided format
        rating=0.0,  # This might be absent in the provided format
        storyboard=bool(int(data.get('Storyboard', 0))),
        video=bool(int(data.get('Video', 0))),
        download_unavailable=bool(int(data.get('DownloadUnavailable', 0))),
        audio_unavailable=bool(int(data.get('AudioUnavailable', 0))),
        playcount=0,  # This might be absent in the provided format
        passcount=0,  # This might be absent in the provided format
        packs=data.get('Packs', ''),
        max_combo=int(data.get('MaxCombo', 0)),
        diff_aim=float(data.get('DifficultyAim', 0)),
        diff_speed=float(data.get('DifficultySpeed', 0)),
        difficultyrating=float(data.get('DifficultyRating', 0)),
        sliderMultiplier=float(data.get('SliderMultiplier', 0))
    ),hyperParamFooter]




# Function to interpolate linear points
def interpolate_linear(start, end, t):
    return start + t * (end - start)

# Function to calculate a point on a quadratic Bezier curve
def bezier_point(t, points):
    n = len(points) - 1
    x = sum(math.comb(n, i) * (1 - t)**(n - i) * t**i * points[i][0] for i in range(n + 1))
    y = sum(math.comb(n, i) * (1 - t)**(n - i) * t**i * points[i][1] for i in range(n + 1))
    return x, y

# Function to calculate a point on a perfect circle (P slider type)
def circle_point(center, radius, angle):
    return (
        center[0] + radius * math.cos(angle),
        center[1] + radius * math.sin(angle)
    )

# Function to split slider into segments
def split_slider(slider_data: str, slider_duration_per_sliderpoint: float,timingpoint_for_this_hitobject: List[str]):
    # print(slider_data)
    # Parse slider_data
    parts = slider_data.split(',')
    sliderdatalen = len(parts)
    # if(sliderdatalen<11):
    #         print(slider_data)

    if sliderdatalen<9:
        parts.append("0|0")
    if sliderdatalen<10:
        parts.append("0:0|0:0")
    if sliderdatalen<11:
        parts.append("0:0:0:0:")

    # if sliderdatalen<11:
    #     print(parts)

    start_point = tuple(map(int, parts[:2]))
    slider_type = parts[5][0]
    path_data = parts[5][2:]

    
    slider_points = parts[8].split('|')
    slider_points_data = parts[9].split('|')
    num_points = len(slider_points)

    # Calculate path points
    path_points = [start_point] + [tuple(map(int, p.split(':'))) for p in path_data.split('|')]

    # Initialize new segments list
    new_segments = []
    
    # Generate new segments based on slider type
    if slider_type == 'L':
        # Linear interpolation
        for i in range(num_points):
            t = i / (num_points - 1)
            new_x = interpolate_linear(start_point[0], path_points[-1][0], t)
            new_y = interpolate_linear(start_point[1], path_points[-1][1], t)
            subpart = parts[-1].split(":")
            subpart.pop()
            subpart = [int(i) for i in subpart]
            # slider_point_toint_data = slider_points_data[i].split(':')
            slider_point_toint_data = [int(i) for i in slider_points_data[i].split(':')] #+[int(i) for i in slider_points_data[i+1].split(':')]
            segment = [int(new_x),int(new_y),(int(parts[2])+(int(slider_duration_per_sliderpoint)*i)),int(parts[3]),int(parts[4]),2,int(new_x),int(new_y),int(parts[6]),float(parts[7]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
            new_segments.append(segment)

    elif slider_type == 'B':
        # Bezier curve interpolation
        for i in range(num_points):
            t = i / (num_points - 1)
            new_x, new_y = bezier_point(t, path_points)
            subpart = parts[-1].split(":")
            subpart.pop()
            subpart = [int(i) for i in subpart]
            # slider_point_toint_data = slider_points_data[i].split(':')
            slider_point_toint_data = [int(i) for i in slider_points_data[i].split(':')]#+[int(i) for i in slider_points_data[i+1].split(':')]
            segment = [int(new_x),int(new_y),(int(parts[2])+(int(slider_duration_per_sliderpoint)*i)),int(parts[3]),int(parts[4]),1,int(new_x),int(new_y),int(parts[6]),float(parts[7]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
            new_segments.append(segment)

    elif slider_type == 'P':
        # Perfect circle interpolation
        # Extract center and radius
        
        # center = path_points[0]
        # radius = math.sqrt((path_points[1][0] - center[0])**2 + (path_points[1][1] - center[1])**2)
        # total_points = num_points
        # angle_increment = 2 * math.pi / total_points
        
        # for i in range(num_points):
        #     angle = i * angle_increment
        #     new_x, new_y = circle_point(center, radius, angle)
        #     subpart = parts[-1].split(":")
        #     subpart.pop()
        #     subpart = [int(i) for i in subpart]
        #     # slider_point_toint_data = slider_points_data[i].split(':')
        #     slider_point_toint_data = [int(i) for i in slider_points_data[i].split(':')]#+[int(i) for i in slider_points_data[i+1].split(':')]
        #     segment = [int(new_x),int(new_y),int(parts[2]),int(parts[3]),int(parts[4]),3,int(new_x),int(new_y),int(parts[6]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
        #     new_segments.append(segment)

        
         # Calculate path points
        path_points = [start_point] + [tuple(map(int, p.split(':'))) for p in path_data.split('|')]
        if num_points==2 :
            slider_points = slider_points + ["0"]
            slider_points_data = slider_points_data + ["0:0"]
        elif num_points>3:
            slider_points = slider_points[0:3]
            slider_points_data = slider_points_data[0:3]
        # print(slider_points)
        # print(path_points)
        num_points = len(slider_points)
        for i in range(num_points):
            new_x, new_y = (path_points[i][0],path_points[i][1])
            subpart = parts[-1].split(":")
            subpart.pop()
            subpart = [int(i) for i in subpart]
            # slider_point_toint_data = slider_points_data[i].split(':')
            slider_point_toint_data = [int(i) for i in slider_points_data[i].split(':')]#+[int(i) for i in slider_points_data[i+1].split(':')]
            segment = [int(new_x),int(new_y),(int(parts[2])+int(float(slider_duration_per_sliderpoint/2)*i)),int(parts[3]),int(parts[4]),3,int(new_x),int(new_y),int(parts[6]),float(parts[7]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
            new_segments.append(segment)


        # print(slider_data)
        # print(new_segments)
    
    # print(new_segments)

    return new_segments

# # Example slider data and split operation
# slider_data = "431,86,96039,6,0,P|406:144|433:238,1,157.500006008148,0|0,1:0|0:0,0:0:0:0:"





def load_osu_files_from_df(df):
    new_df = pd.DataFrame()
    # Ensure the processed folder exists
    os.makedirs("processed-beatmaps", exist_ok=True)
    
    for index, row in df.iterrows():
        # Construct the osu! file path
        file_path = os.path.join(archive_path, "train", row['folder'], f"{row['audio']}.osu")
        
        # Check if the file exists before parsing
        if os.path.exists(file_path):
            # Parse the osu! file (assume this returns some data)
            data,hyperParamFooter = parse_osu_file(file_path)

            # Add a new column to the row
            row['StackLeniency'] = hyperParamFooter[0]
            row['DistanceSpacing'] = hyperParamFooter[0]
            row['BeatDivisor'] = hyperParamFooter[0]
            row['HPDrainRate'] = hyperParamFooter[0]
            row['CircleSize'] = hyperParamFooter[0]
            row['OverallDifficulty'] = hyperParamFooter[0]
            row['ApproachRate'] = hyperParamFooter[0]
            row['SliderTickRate'] = hyperParamFooter[0]
            row['SliderMultiplier'] = hyperParamFooter[0]
            
            # Convert the row to a DataFrame and append to new_df
            new_df = pd.concat([new_df, pd.DataFrame([row])], ignore_index=True)
            # print(hyperParamFooter)
            
            # Convert the data to a NumPy array
            data_array = np.array(data.hit_objects)
            
            # Define the save path in the processed folder
            save_path = os.path.join("processed-beatmaps", f"{row['audio']}-b.npy")
            
            # Save the NumPy array to disk
            np.save(save_path, data_array)
        else:
            print(f"File not found: {file_path}")
    
    #save metadata also for retrieval later
    save_df_as_csv(new_df)


def save_df_as_csv(df):
    # Ensure the processed metadata folder exists
    os.makedirs("processed-metadata", exist_ok=True)
    
    # Define the save path in the processed metadata folder
    save_path = os.path.join("processed-metadata", "processed-metadata.csv")
    
    # Save the DataFrame as a CSV file
    df.to_csv(save_path, index=False)
    print(f"DataFrame saved as a CSV at: {save_path}")
