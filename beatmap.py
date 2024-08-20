class OsuBeatmap:
    def __init__(self,hit_objects ,audio, split, folder, beatmapset_id, beatmap_id, approved, total_length, hit_length, version,
                 file_md5, diff_size, diff_overall, diff_approach, diff_drain, mode, count_normal, count_slider,
                 count_spinner, submit_date, approved_date, last_update, artist, artist_unicode, title, title_unicode,
                 creator, creator_id, bpm, source, tags, genre_id, language_id, favourite_count, rating, storyboard,
                 video, download_unavailable, audio_unavailable, playcount, passcount, packs, max_combo, diff_aim,
                 diff_speed, difficultyrating):
        self.hit_objects = hit_objects
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

    def __repr__(self):
        return f"OsuBeatmap({self.title} - {self.artist})"

import math
from typing import List, Tuple

    
def process_hitobject(hitobject: str) -> List[str]:
    parts = hitobject.split(',')
    hit_type = int(parts[3])
    
    if hit_type in {1, 5}:
        # Handle hit objects of type 1 or 4
        if len(parts)==5:
            parts.append("0:0:0:0:")
        subpart = parts[5].split(":")
        subpart.pop()
        subpart = [int(i) for i in subpart]
        parts = [int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4])] + [-1] * 10 + subpart + [-1]
        return [parts + ['-1'] * (11 - len(parts))]  # Length 11
    
    elif hit_type in {2, 6}:
        # Handle hit objects of type 2 or 6 (slider)
        # slider_data = parts[5]
        
        return split_slider(hitobject)
    
    elif hit_type in {8, 12}:
        # Handle hit objects of type 8 or 12
        if len(parts)==6:
            parts.append("0:0:0:0:")
        return [[int(parts[0]),int(parts[1]),int(parts[2]),int(parts[3]),int(parts[4]),int(parts[5]) ]+ [-1] * 9 +[0,0,0,0,-1]]  # Pad to length 11
    
    else:
        return [parts]  # Return as-is if no special handling    



def parse_osu_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = {}
        hit_objects = []
        current_section = None
        
        for line in file:
            line = line.strip()
            if line.startswith('['):
                # Handle section headers
                current_section = line[1:-1]
                continue
            
            if current_section == 'HitObjects' and line:
                for l in process_hitobject(line):
                    hit_objects.append(l)
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
    # Create an instance of OsuBeatmap using the parsed data
    return OsuBeatmap(
        hit_objects=hit_objects,
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
        difficultyrating=float(data.get('DifficultyRating', 0))
    )




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
def split_slider(slider_data: str):
    print(slider_data)
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
            segment = [int(new_x),int(new_y),int(parts[2]),int(parts[3]),int(parts[4]),2,int(new_x),int(new_y),int(parts[6]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
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
            segment = [int(new_x),int(new_y),int(parts[2]),int(parts[3]),int(parts[4]),1,int(new_x),int(new_y),int(parts[6]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
            new_segments.append(segment)

    elif slider_type == 'P':
        # Perfect circle interpolation
        # Extract center and radius
        center = path_points[0]
        radius = math.sqrt((path_points[1][0] - center[0])**2 + (path_points[1][1] - center[1])**2)
        total_points = num_points
        angle_increment = 2 * math.pi / total_points
        
        for i in range(num_points):
            angle = i * angle_increment
            new_x, new_y = circle_point(center, radius, angle)
            subpart = parts[-1].split(":")
            subpart.pop()
            subpart = [int(i) for i in subpart]
            # slider_point_toint_data = slider_points_data[i].split(':')
            slider_point_toint_data = [int(i) for i in slider_points_data[i].split(':')]#+[int(i) for i in slider_points_data[i+1].split(':')]
            segment = [int(new_x),int(new_y),int(parts[2]),int(parts[3]),int(parts[4]),3,int(new_x),int(new_y),int(parts[6]),int(slider_points[i])]+slider_point_toint_data+subpart+[0 if i == 0 else 2 if i == num_points - 1 else 1]
            new_segments.append(segment)
    
    print(new_segments)

    return new_segments

# # Example slider data and split operation
# slider_data = "431,86,96039,6,0,P|406:144|433:238,1,157.500006008148,0|0,1:0|0:0,0:0:0:0:"

# # Split the slider into segments
# new_slider_segments = split_slider(slider_data)
# # Output the new segments
# for segment in new_slider_segments:
#     print(segment)