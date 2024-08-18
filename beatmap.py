class OsuBeatmap:
    def __init__(self, audio, split, folder, beatmapset_id, beatmap_id, approved, total_length, hit_length, version,
                 file_md5, diff_size, diff_overall, diff_approach, diff_drain, mode, count_normal, count_slider,
                 count_spinner, submit_date, approved_date, last_update, artist, artist_unicode, title, title_unicode,
                 creator, creator_id, bpm, source, tags, genre_id, language_id, favourite_count, rating, storyboard,
                 video, download_unavailable, audio_unavailable, playcount, passcount, packs, max_combo, diff_aim,
                 diff_speed, difficultyrating):
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



def parse_osu_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = {}
        for line in file:
            if line.startswith('['):
                # Skip section headers like [General], [Metadata], etc.
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()

    # Create an instance of OsuBeatmap using the parsed data
    return OsuBeatmap(
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
