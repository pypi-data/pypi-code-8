# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from __sdl_mixer import ffi, lib
from .structs import unbox, Struct
from _sdl.structs import u8
from _sdl.autohelpers import SDL_version

def Mix_AllocateChannels(numchans):
    """
    ``int Mix_AllocateChannels(int)``
    """
    numchans_c = numchans
    rc = lib.Mix_AllocateChannels(numchans_c)
    return rc

def Mix_ChannelFinished(channel_finished):
    """
    ``void Mix_ChannelFinished(void Mix_ChannelFinished(int))``
    """
    channel_finished_c = unbox(channel_finished, 'void(*)(int)')
    lib.Mix_ChannelFinished(channel_finished_c)

def Mix_CloseAudio():
    """
    ``void Mix_CloseAudio(void)``
    """
    lib.Mix_CloseAudio()

def Mix_EachSoundFont(function, data):
    """
    ``int Mix_EachSoundFont(int Mix_EachSoundFont(char const *, void *), void *)``
    """
    function_c = unbox(function, 'int(*)(char const *, void *)')
    data_c = unbox(data, 'void *')
    rc = lib.Mix_EachSoundFont(function_c, data_c)
    return rc

def Mix_ExpireChannel(channel, ticks):
    """
    ``int Mix_ExpireChannel(int, int)``
    """
    channel_c = channel
    ticks_c = ticks
    rc = lib.Mix_ExpireChannel(channel_c, ticks_c)
    return rc

def Mix_FadeInChannelTimed(channel, chunk, loops, ms, ticks):
    """
    ``int Mix_FadeInChannelTimed(int, Mix_Chunk *, int, int, int)``
    """
    channel_c = channel
    chunk_c = unbox(chunk, 'Mix_Chunk *')
    loops_c = loops
    ms_c = ms
    ticks_c = ticks
    rc = lib.Mix_FadeInChannelTimed(channel_c, chunk_c, loops_c, ms_c, ticks_c)
    return rc

def Mix_FadeInMusic(music, loops, ms):
    """
    ``int Mix_FadeInMusic(Mix_Music *, int, int)``
    """
    music_c = unbox(music, 'Mix_Music *')
    loops_c = loops
    ms_c = ms
    rc = lib.Mix_FadeInMusic(music_c, loops_c, ms_c)
    return rc

def Mix_FadeInMusicPos(music, loops, ms, position):
    """
    ``int Mix_FadeInMusicPos(Mix_Music *, int, int, double)``
    """
    music_c = unbox(music, 'Mix_Music *')
    loops_c = loops
    ms_c = ms
    position_c = position
    rc = lib.Mix_FadeInMusicPos(music_c, loops_c, ms_c, position_c)
    return rc

def Mix_FadeOutChannel(which, ms):
    """
    ``int Mix_FadeOutChannel(int, int)``
    """
    which_c = which
    ms_c = ms
    rc = lib.Mix_FadeOutChannel(which_c, ms_c)
    return rc

def Mix_FadeOutGroup(tag, ms):
    """
    ``int Mix_FadeOutGroup(int, int)``
    """
    tag_c = tag
    ms_c = ms
    rc = lib.Mix_FadeOutGroup(tag_c, ms_c)
    return rc

def Mix_FadeOutMusic(ms):
    """
    ``int Mix_FadeOutMusic(int)``
    """
    ms_c = ms
    rc = lib.Mix_FadeOutMusic(ms_c)
    return rc

def Mix_FadingChannel(which):
    """
    ``Mix_Fading Mix_FadingChannel(int)``
    """
    which_c = which
    rc = lib.Mix_FadingChannel(which_c)
    return rc

def Mix_FadingMusic():
    """
    ``Mix_Fading Mix_FadingMusic(void)``
    """
    rc = lib.Mix_FadingMusic()
    return rc

def Mix_FreeChunk(chunk):
    """
    ``void Mix_FreeChunk(Mix_Chunk *)``
    """
    chunk_c = unbox(chunk, 'Mix_Chunk *')
    lib.Mix_FreeChunk(chunk_c)

def Mix_FreeMusic(music):
    """
    ``void Mix_FreeMusic(Mix_Music *)``
    """
    music_c = unbox(music, 'Mix_Music *')
    lib.Mix_FreeMusic(music_c)

def Mix_GetChunk(channel):
    """
    ``Mix_Chunk * Mix_GetChunk(int)``
    """
    channel_c = channel
    rc = lib.Mix_GetChunk(channel_c)
    return Mix_Chunk(rc)

def Mix_GetChunkDecoder(index):
    """
    ``char const * Mix_GetChunkDecoder(int)``
    """
    index_c = index
    rc = lib.Mix_GetChunkDecoder(index_c)
    return ffi.string(rc).decode('utf-8')

def Mix_GetMusicDecoder(index):
    """
    ``char const * Mix_GetMusicDecoder(int)``
    """
    index_c = index
    rc = lib.Mix_GetMusicDecoder(index_c)
    return ffi.string(rc).decode('utf-8')

def Mix_GetMusicHookData():
    """
    ``void * Mix_GetMusicHookData(void)``
    """
    rc = lib.Mix_GetMusicHookData()
    return rc

def Mix_GetMusicType(music):
    """
    ``Mix_MusicType Mix_GetMusicType(Mix_Music const *)``
    """
    music_c = unbox(music, 'Mix_Music const *')
    rc = lib.Mix_GetMusicType(music_c)
    return rc

def Mix_GetNumChunkDecoders():
    """
    ``int Mix_GetNumChunkDecoders(void)``
    """
    rc = lib.Mix_GetNumChunkDecoders()
    return rc

def Mix_GetNumMusicDecoders():
    """
    ``int Mix_GetNumMusicDecoders(void)``
    """
    rc = lib.Mix_GetNumMusicDecoders()
    return rc

def Mix_GetSoundFonts():
    """
    ``char const * Mix_GetSoundFonts(void)``
    """
    rc = lib.Mix_GetSoundFonts()
    return ffi.string(rc).decode('utf-8')

def Mix_GetSynchroValue():
    """
    ``int Mix_GetSynchroValue(void)``
    """
    rc = lib.Mix_GetSynchroValue()
    return rc

def Mix_GroupAvailable(tag):
    """
    ``int Mix_GroupAvailable(int)``
    """
    tag_c = tag
    rc = lib.Mix_GroupAvailable(tag_c)
    return rc

def Mix_GroupChannel(which, tag):
    """
    ``int Mix_GroupChannel(int, int)``
    """
    which_c = which
    tag_c = tag
    rc = lib.Mix_GroupChannel(which_c, tag_c)
    return rc

def Mix_GroupChannels(from_, to, tag):
    """
    ``int Mix_GroupChannels(int, int, int)``
    """
    from__c = from_
    to_c = to
    tag_c = tag
    rc = lib.Mix_GroupChannels(from__c, to_c, tag_c)
    return rc

def Mix_GroupCount(tag):
    """
    ``int Mix_GroupCount(int)``
    """
    tag_c = tag
    rc = lib.Mix_GroupCount(tag_c)
    return rc

def Mix_GroupNewer(tag):
    """
    ``int Mix_GroupNewer(int)``
    """
    tag_c = tag
    rc = lib.Mix_GroupNewer(tag_c)
    return rc

def Mix_GroupOldest(tag):
    """
    ``int Mix_GroupOldest(int)``
    """
    tag_c = tag
    rc = lib.Mix_GroupOldest(tag_c)
    return rc

def Mix_HaltChannel(channel):
    """
    ``int Mix_HaltChannel(int)``
    """
    channel_c = channel
    rc = lib.Mix_HaltChannel(channel_c)
    return rc

def Mix_HaltGroup(tag):
    """
    ``int Mix_HaltGroup(int)``
    """
    tag_c = tag
    rc = lib.Mix_HaltGroup(tag_c)
    return rc

def Mix_HaltMusic():
    """
    ``int Mix_HaltMusic(void)``
    """
    rc = lib.Mix_HaltMusic()
    return rc

def Mix_HookMusic(mix_func, arg):
    """
    ``void Mix_HookMusic(void Mix_HookMusic(void *, unsigned char *, int), void *)``
    """
    mix_func_c = unbox(mix_func, 'void(*)(void *, unsigned char *, int)')
    arg_c = unbox(arg, 'void *')
    lib.Mix_HookMusic(mix_func_c, arg_c)

def Mix_HookMusicFinished(music_finished):
    """
    ``void Mix_HookMusicFinished(void Mix_HookMusicFinished(void))``
    """
    music_finished_c = unbox(music_finished, 'void(*)(void)')
    lib.Mix_HookMusicFinished(music_finished_c)

def Mix_Init(flags):
    """
    ``int Mix_Init(int)``
    """
    flags_c = flags
    rc = lib.Mix_Init(flags_c)
    return rc

def Mix_Linked_Version():
    """
    ``SDL_version const * Mix_Linked_Version(void)``
    """
    rc = lib.Mix_Linked_Version()
    return SDL_version(rc)

def Mix_LoadMUS(file):
    """
    ``Mix_Music * Mix_LoadMUS(char const *)``
    """
    file_c = u8(file)
    rc = lib.Mix_LoadMUS(file_c)
    return Mix_Music(rc)

def Mix_LoadMUSType_RW(src, type, freesrc):
    """
    ``Mix_Music * Mix_LoadMUSType_RW(SDL_RWops *, Mix_MusicType, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    type_c = type
    freesrc_c = freesrc
    rc = lib.Mix_LoadMUSType_RW(src_c, type_c, freesrc_c)
    return Mix_Music(rc)

def Mix_LoadMUS_RW(src, freesrc):
    """
    ``Mix_Music * Mix_LoadMUS_RW(SDL_RWops *, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = lib.Mix_LoadMUS_RW(src_c, freesrc_c)
    return Mix_Music(rc)

def Mix_LoadWAV_RW(src, freesrc):
    """
    ``Mix_Chunk * Mix_LoadWAV_RW(SDL_RWops *, int)``
    """
    src_c = unbox(src, 'SDL_RWops *')
    freesrc_c = freesrc
    rc = lib.Mix_LoadWAV_RW(src_c, freesrc_c)
    return Mix_Chunk(rc)

def Mix_OpenAudio(frequency, format, channels, chunksize):
    """
    ``int Mix_OpenAudio(int, unsigned short, int, int)``
    """
    frequency_c = frequency
    format_c = format
    channels_c = channels
    chunksize_c = chunksize
    rc = lib.Mix_OpenAudio(frequency_c, format_c, channels_c, chunksize_c)
    return rc

def Mix_Pause(channel):
    """
    ``void Mix_Pause(int)``
    """
    channel_c = channel
    lib.Mix_Pause(channel_c)

def Mix_PauseMusic():
    """
    ``void Mix_PauseMusic(void)``
    """
    lib.Mix_PauseMusic()

def Mix_Paused(channel):
    """
    ``int Mix_Paused(int)``
    """
    channel_c = channel
    rc = lib.Mix_Paused(channel_c)
    return rc

def Mix_PausedMusic():
    """
    ``int Mix_PausedMusic(void)``
    """
    rc = lib.Mix_PausedMusic()
    return rc

def Mix_PlayChannelTimed(channel, chunk, loops, ticks):
    """
    ``int Mix_PlayChannelTimed(int, Mix_Chunk *, int, int)``
    """
    channel_c = channel
    chunk_c = unbox(chunk, 'Mix_Chunk *')
    loops_c = loops
    ticks_c = ticks
    rc = lib.Mix_PlayChannelTimed(channel_c, chunk_c, loops_c, ticks_c)
    return rc

def Mix_PlayMusic(music, loops):
    """
    ``int Mix_PlayMusic(Mix_Music *, int)``
    """
    music_c = unbox(music, 'Mix_Music *')
    loops_c = loops
    rc = lib.Mix_PlayMusic(music_c, loops_c)
    return rc

def Mix_Playing(channel):
    """
    ``int Mix_Playing(int)``
    """
    channel_c = channel
    rc = lib.Mix_Playing(channel_c)
    return rc

def Mix_PlayingMusic():
    """
    ``int Mix_PlayingMusic(void)``
    """
    rc = lib.Mix_PlayingMusic()
    return rc

def Mix_QuerySpec(frequency=None, format=None, channels=None):
    """
    ``int Mix_QuerySpec(int *, unsigned short *, int *)``
    """
    frequency_c = unbox(frequency, 'int *')
    format_c = unbox(format, 'unsigned short *')
    channels_c = unbox(channels, 'int *')
    rc = lib.Mix_QuerySpec(frequency_c, format_c, channels_c)
    return (rc, frequency_c[0], format_c[0], channels_c[0])

def Mix_QuickLoad_RAW(mem, len):
    """
    ``Mix_Chunk * Mix_QuickLoad_RAW(unsigned char *, unsigned int)``
    """
    mem_c = unbox(mem, 'unsigned char *')
    len_c = len
    rc = lib.Mix_QuickLoad_RAW(mem_c, len_c)
    return Mix_Chunk(rc)

def Mix_QuickLoad_WAV(mem=None):
    """
    ``Mix_Chunk * Mix_QuickLoad_WAV(unsigned char *)``
    """
    mem_c = unbox(mem, 'unsigned char *')
    rc = lib.Mix_QuickLoad_WAV(mem_c)
    return (Mix_Chunk(rc), mem_c[0])

def Mix_Quit():
    """
    ``void Mix_Quit(void)``
    """
    lib.Mix_Quit()

def Mix_RegisterEffect(chan, f, d, arg):
    """
    ``int Mix_RegisterEffect(int, void Mix_RegisterEffect(int, void *, int, void *), void Mix_RegisterEffect(int, void *), void *)``
    """
    chan_c = chan
    f_c = unbox(f, 'void(*)(int, void *, int, void *)')
    d_c = unbox(d, 'void(*)(int, void *)')
    arg_c = unbox(arg, 'void *')
    rc = lib.Mix_RegisterEffect(chan_c, f_c, d_c, arg_c)
    return rc

def Mix_ReserveChannels(num):
    """
    ``int Mix_ReserveChannels(int)``
    """
    num_c = num
    rc = lib.Mix_ReserveChannels(num_c)
    return rc

def Mix_Resume(channel):
    """
    ``void Mix_Resume(int)``
    """
    channel_c = channel
    lib.Mix_Resume(channel_c)

def Mix_ResumeMusic():
    """
    ``void Mix_ResumeMusic(void)``
    """
    lib.Mix_ResumeMusic()

def Mix_RewindMusic():
    """
    ``void Mix_RewindMusic(void)``
    """
    lib.Mix_RewindMusic()

def Mix_SetDistance(channel, distance):
    """
    ``int Mix_SetDistance(int, unsigned char)``
    """
    channel_c = channel
    distance_c = distance
    rc = lib.Mix_SetDistance(channel_c, distance_c)
    return rc

def Mix_SetMusicCMD(command):
    """
    ``int Mix_SetMusicCMD(char const *)``
    """
    command_c = u8(command)
    rc = lib.Mix_SetMusicCMD(command_c)
    return rc

def Mix_SetMusicPosition(position):
    """
    ``int Mix_SetMusicPosition(double)``
    """
    position_c = position
    rc = lib.Mix_SetMusicPosition(position_c)
    return rc

def Mix_SetPanning(channel, left, right):
    """
    ``int Mix_SetPanning(int, unsigned char, unsigned char)``
    """
    channel_c = channel
    left_c = left
    right_c = right
    rc = lib.Mix_SetPanning(channel_c, left_c, right_c)
    return rc

def Mix_SetPosition(channel, angle, distance):
    """
    ``int Mix_SetPosition(int, int16_t, unsigned char)``
    """
    channel_c = channel
    angle_c = angle
    distance_c = distance
    rc = lib.Mix_SetPosition(channel_c, angle_c, distance_c)
    return rc

def Mix_SetPostMix(mix_func, arg):
    """
    ``void Mix_SetPostMix(void Mix_SetPostMix(void *, unsigned char *, int), void *)``
    """
    mix_func_c = unbox(mix_func, 'void(*)(void *, unsigned char *, int)')
    arg_c = unbox(arg, 'void *')
    lib.Mix_SetPostMix(mix_func_c, arg_c)

def Mix_SetReverseStereo(channel, flip):
    """
    ``int Mix_SetReverseStereo(int, int)``
    """
    channel_c = channel
    flip_c = flip
    rc = lib.Mix_SetReverseStereo(channel_c, flip_c)
    return rc

def Mix_SetSoundFonts(paths):
    """
    ``int Mix_SetSoundFonts(char const *)``
    """
    paths_c = u8(paths)
    rc = lib.Mix_SetSoundFonts(paths_c)
    return rc

def Mix_SetSynchroValue(value):
    """
    ``int Mix_SetSynchroValue(int)``
    """
    value_c = value
    rc = lib.Mix_SetSynchroValue(value_c)
    return rc

def Mix_UnregisterAllEffects(channel):
    """
    ``int Mix_UnregisterAllEffects(int)``
    """
    channel_c = channel
    rc = lib.Mix_UnregisterAllEffects(channel_c)
    return rc

def Mix_UnregisterEffect(channel, f):
    """
    ``int Mix_UnregisterEffect(int, void Mix_UnregisterEffect(int, void *, int, void *))``
    """
    channel_c = channel
    f_c = unbox(f, 'void(*)(int, void *, int, void *)')
    rc = lib.Mix_UnregisterEffect(channel_c, f_c)
    return rc

def Mix_Volume(channel, volume):
    """
    ``int Mix_Volume(int, int)``
    """
    channel_c = channel
    volume_c = volume
    rc = lib.Mix_Volume(channel_c, volume_c)
    return rc

def Mix_VolumeChunk(chunk, volume):
    """
    ``int Mix_VolumeChunk(Mix_Chunk *, int)``
    """
    chunk_c = unbox(chunk, 'Mix_Chunk *')
    volume_c = volume
    rc = lib.Mix_VolumeChunk(chunk_c, volume_c)
    return rc

def Mix_VolumeMusic(volume):
    """
    ``int Mix_VolumeMusic(int)``
    """
    volume_c = volume
    rc = lib.Mix_VolumeMusic(volume_c)
    return rc

MIX_INIT_FLAC = lib.MIX_INIT_FLAC
MIX_INIT_MOD = lib.MIX_INIT_MOD
MIX_INIT_MODPLUG = lib.MIX_INIT_MODPLUG
MIX_INIT_MP3 = lib.MIX_INIT_MP3
MIX_INIT_OGG = lib.MIX_INIT_OGG
MIX_INIT_FLUIDSYNTH = lib.MIX_INIT_FLUIDSYNTH

MIX_NO_FADING = lib.MIX_NO_FADING
MIX_FADING_OUT = lib.MIX_FADING_OUT
MIX_FADING_IN = lib.MIX_FADING_IN

MUS_NONE = lib.MUS_NONE
MUS_CMD = lib.MUS_CMD
MUS_WAV = lib.MUS_WAV
MUS_MOD = lib.MUS_MOD
MUS_MID = lib.MUS_MID
MUS_OGG = lib.MUS_OGG
MUS_MP3 = lib.MUS_MP3
MUS_MP3_MAD = lib.MUS_MP3_MAD
MUS_FLAC = lib.MUS_FLAC
MUS_MODPLUG = lib.MUS_MODPLUG

class Mix_Chunk(Struct):
    """Wrap `Mix_Chunk`"""
    @property
    def allocated(self): return self.cdata.allocated
    @allocated.setter
    def allocated(self, value): self.cdata.allocated = value
    @property
    def abuf(self): return self.cdata.abuf
    @abuf.setter
    def abuf(self, value): self.cdata.abuf = value
    @property
    def alen(self): return self.cdata.alen
    @alen.setter
    def alen(self, value): self.cdata.alen = value
    @property
    def volume(self): return self.cdata.volume
    @volume.setter
    def volume(self, value): self.cdata.volume = value
    freeChunk = Mix_FreeChunk
    volumeChunk = Mix_VolumeChunk

class Mix_Music(Struct):
    """Wrap `Mix_Music`"""
    fadeInMusic = Mix_FadeInMusic
    fadeInMusicPos = Mix_FadeInMusicPos
    freeMusic = Mix_FreeMusic
    getMusicType = Mix_GetMusicType
    playMusic = Mix_PlayMusic

