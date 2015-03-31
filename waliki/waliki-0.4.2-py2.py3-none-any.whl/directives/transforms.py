from docutils import nodes
from docutils.transforms import Transform
from docutils.readers.standalone import Reader

from waliki.plugins import str2object
from waliki.settings import WALIKI_RST_TRANSFORMS


class Emojis(Transform):
    """
    Replace some substitutions if they aren't defined in the document.
    """
    # run before the default Substitutions
    default_priority = 210

    # list taken from from https://github.com/carpedm20/emoji/blob/master/emoji/code.py
    emojis = {'full_moon', 'womans_hat', 'fountain', 'seven', 'sparkles', 'chart_with_upwards_trend', 'relaxed', 'koko', 'blue_book', 'v', 'loud_sound', 'open_mouth', 'one', 'full_moon_with_face', 'yen', 'alien', 'eight_spoked_asterisk', 'smile', 'tiger', 'ng', 'cinema', 'eyeglasses', 'closed_book', 'rocket', 'three', 'fried_shrimp', 'clubs', 'kimono', 'construction_worker', 'mag', 'kissing_smiling_eyes', 'wink', 'joy', 'sweat_smile', 'large_blue_circle', 'end', 'mute', 'ideograph_advantage', 'bullettrain_front', 'five', 'balloon', 'bird', 'two_women_holding_hands', 'e-mail', 'four', 'watermelon', 'point_down', 'clock9', 'black_nib', 'slot_machine', 'beginner', '1234', 'sparkler', 'parking', 'heart', 'clock430', 'open_file_folder', 'information_desk_person', 'disappointed', 'car', 'barber', 'accept', 'repeat_one', 'ear_of_rice', 'lips', 'flower_playing_cards', 'lock_with_ink_pen', 'wheelchair', 'icecream', 'bamboo', 'moyai', 'maple_leaf', 'high_heel', 'ticket', 'ear', 'ledger', 'raised_hands', 'large_blue_diamond', 'dog', 'b', 'busstop', 'eight', 'clipboard', 'four_leaf_clover', 'lantern', 'grapes', 'penguin', 'page_facing_up', 'tada', 'triangular_flag_on_post', 'tea', 'water_buffalo', 'ab', 'birthday', 'wave', 'gift_heart', 'heavy_multiplication_x', 'ophiuchus', 'chart', 'bread', 'bike', 'shoe', 'smile_cat', 'kissing_heart', 'waning_crescent_moon', 'wc', 'thought_balloon', 'sheep', 'wedding', 'ram', 'small_orange_diamond', 'zzz', 'no_smoking', 'bath', 'neutral_face', 'new_moon_with_face', 'key', 'white_medium_small_square', 'herb', 'curry', 'snowman', 'clock6', 'persevere', 'yum', 'smiling_imp', 'oncoming_automobile', 'hibiscus', 'stuck_out_tongue_closed_eyes', 'ant', 'steam_locomotive', 'mans_shoe', 'innocent', 'chart_with_downwards_trend', 'rice', 'children_crossing', 'clapper', 'person_with_blond_hair', 'point_up', 'koala', 'gem', 'pouch', 'bookmark_tabs', 'loop', 'hearts', 'inbox_tray', 'womens', 'bulb', 'sound', 'mountain_railway', 'cupid', 'first_quarter_moon_with_face', 'page_with_curl', 'phone', 'haircut', 'european_castle', 'rage', 'clock10', 'rugby_football', 'white_check_mark', 'it', 'ok_woman', 'clock1130', 'link', 'rice_ball', 'on', 'a', 'aerial_tramway', 'family', 'facepunch', 'japanese_castle', 'japanese_goblin', 'grey_exclamation', 'dog2', 'arrow_up_down', 'izakaya_lantern', 'running', 'signal_strength', 'trident', 'sagittarius', 'heavy_dollar_sign', 'musical_score', 'black_square_button', 'leftwards_arrow_with_hook', 'custard', 'roller_coaster', 'mountain_bicyclist', 'sparkling_heart', 'tv', 'horse', 'six', 'satellite', 'green_book', 'umbrella', 'waning_gibbous_moon', 'two', 'spades', 'bikini', 'hospital', 'curly_loop', 'moneybag', 'speak_no_evil', 'nut_and_bolt', 'pig', 'telephone_receiver', 'tram', 'mouse', 'mag_right', 'clock3', 'bridge_at_night', 'tractor', 'relieved', 'small_blue_diamond', 'frowning', 'minibus', 'school', 'sleeping', 'camel', 'coffee', 'newspaper', 'lemon', 'musical_keyboard', 'u6709', 'person_with_pouting_face', 'busts_in_silhouette', 'pray', 'heavy_plus_sign', 'new', 'kiss', 'rice_cracker', 'clock8', 'blossom', 'pencil', 'poop', 'bear', 'triumph', 'white_circle', 'jp', 'back', 'round_pushpin', 'alarm_clock', 'mount_fuji', 'bus', 'sunrise_over_mountains', 'cd', 'clock930', 'clock4', 'skull', 'currency_exchange', 'weary', 'ring', 'snail', 'beetle', 'u6e80', 'black_large_square', 'footprints', 'restroom', 'game_die', 'hushed', 'twisted_rightwards_arrows', 'doughnut', 'computer', 'imp', 'ok', 'see_no_evil', 'heartbeat', 'hotel', 'worried', 'battery', 'paw_prints', 'keycap_ten', 'point_left', 'airplane', 'grimacing', 'recycle', 'no_entry_sign', 'couplekiss', 'cyclone', 'dango', 'm', 'stew', 'iphone', 'kissing', 'pushpin', 'straight_ruler', 'sunrise', 'light_rail', 'tennis', 'black_medium_small_square', 'smirk_cat', 'zero', 'up', 'u7121', 'convenience_store', 'carousel_horse', 'sun_with_face', 'thumbsup', 'snowboarder', 'video_game', 'put_litter_in_its_place', 'station', 'crescent_moon', 'black_small_square', 'pig_nose', 'meat_on_bone', 'zap', 'clock5', 'house', 'train2', 'bullettrain_side', 'clock7', 'hash', 'sparkle', 'rabbit', 'astonished', 'beers', 'star2', 'beer', 'abc', 'gun', 'chicken', 'jack_o_lantern', 'headphones', 'rewind', 'clock630', 'mushroom', 'shell', 'no_entry', 'dizzy', 'mobile_phone_off', 'waxing_crescent_moon', 'confounded', 'small_red_triangle_down', 'droplet', 'large_orange_diamond', 'post_office', 'arrow_up_small', 'city_sunrise', 'train', 'es', 'pizza', 'moon', 'dvd', 'fireworks', 'laughing', 'flags', 'wavy_dash', 'bank', 'virgo', 'clock11', 'athletic_shoe', 'dash', 'bowling', 'womans_clothes', 'arrow_lower_left', 'trolleybus', 'sushi', 'nail_care', 'sweat', 'bee', 'tshirt', 'fr', 'id', 'pensive', 'heavy_division_sign', 'nose', 'syringe', 'massage', 'envelope', 'baby_symbol', 'smirk', 'honey_pot', 'elephant', 'dizzy_face', 'arrows_counterclockwise', 'rabbit2', 'heart_eyes_cat', 'railway_car', 'older_woman', 'lollipop', 'arrow_heading_down', 'purse', 'heavy_check_mark', 'racehorse', 'speech_balloon', 'date', 'left_luggage', 'cat2', 'monkey_face', 'passport_control', 'arrow_heading_up', 'sunglasses', 'camera', 'suspension_railway', 'black_joker', 'clock330', 'fork_and_knife', 'vhs', 'star', 'eggplant', 'us', 'clock130', 'atm', 'musical_note', 'expressionless', 'ox', 'dragon_face', 'space_invader', 'ballot_box_with_check', 'x', 'punch', 'office', 'running_shirt_with_sash', 'dancers', 'purple_heart', 'goat', 'love_letter', '8ball', 'customs', 'bow', 'loudspeaker', 'heavy_minus_sign', 'scroll', 'cookie', 'open_book', 'golf', 'sake', 'bicyclist', 'cocktail', 'postal_horn', 'gb', 'tm', 'fast_forward', 'scissors', 'last_quarter_moon_with_face', 'minidisc', 'video_camera', 'city_sunset', 'whale', 'anchor', 'arrow_down', 'hourglass_flowing_sand', 'rose', 'watch', 'hatched_chick', 'rainbow', 'chocolate_bar', 'cherry_blossom', 'exclamation', 'crocodile', 'dollar', 'cake', 'money_with_wings', 'anguished', 'ghost', 'heart_decoration', 'floppy_disk', 'vs', 'bar_chart', 'smiley_cat', 'grey_question', 'dress', 'memo', 'art', 'stuck_out_tongue', 'r:u', 'closed_umbrella', 'arrow_upper_left', 'broken_heart', 'wine_glass', 'symbols', 'heavy_exclamation_mark', 'mask', 'cool', 'hear_no_evil', 'scream_cat', 'fuelpump', 'poultry_leg', 'fish', 'ramen', 'pisces', 'seat', 'ambulance', 'sleepy', 'corn', 'books', 'telephone', 'monkey', 'red_circle', 'arrow_up', 'notes', 'libra', 'volcano', 'taurus', 'blush', 'tired_face', 'incoming_envelope', 'cancer', 'boar', 'nine', 'envelope_with_arrow', 'turtle', 'hankey', 'bell', 'baby', 'potable_water', 'rowboat', 'crossed_flags', 'clock530', 'wrench', 'underage', 'bouquet', 'briefcase', 'white_medium_square', 'kissing_cat', 'microscope', 'green_apple', 'kr', 'hammer', 'clock12', 'ribbon', 'mortar_board', 'cop', 'arrow_upper_right', 'rotating_light', 'clock1230', 'lipstick', 'anger', 'crystal_ball', 'night_with_stars', 'pig2', 'boom', 'part_alternation_mark', 'couple_with_heart', 'notebook_with_decorative_cover', 'sweet_potato', 'confetti_ball', 'interrobang', 'email', 'small_red_triangle', 'white_square_button', 'shaved_ice', 'gift', 'hamburger', 'dancer', 'cl', 'fist', 'vibration_mode', 'tropical_fish', 'last_quarter_moon', 'panda_face', 'trophy', 'fries', 'tophat', 'unamused', 'eyes', 'u55b6', 'tulip', 'question', 'leopard', 'mahjong', 'arrow_down_small', 'fallen_leaf', 'pouting_cat', 'person_frowning', 'man_with_gua_pi_mao', 'feet', '-1', 'calendar', 'registered', 'bride_with_veil', 'triangular_ruler', 'raised_hand', 'violin', 'apple', 'euro', 'muscle', 'leo', 'boot', 'eight_pointed_black_star', 'no_mouth', 'door', 'deciduous_tree', 'hamster', 'point_up_2', 'snowflake', 'bomb', 'tent', 'top', 'notebook', 'frog', 'angel', 'walking', 'clap', 'diamond_shape_with_a_dot_inside', 'blue_heart', 'shirt', 'rice_scene', 'black_circle', 'pill', 'runner', 'arrow_left', 'hatching_chick', 'capital_abcd', 'hocho', 'paperclip', 'ocean', 'saxophone', 'metro', 'dolphin', 'sandal', 'fish_cake', 'arrow_backward', 'heart_eyes', 'crying_cat_face', 'bento', 'stuck_out_tongue_winking_eye', 'soccer', 'clock730', 'clock830', 'scorpius', 'guitar', 'clock1', 'chestnut', 'department_store', 'poodle', 'love_hotel', 'mailbox_with_no_mail', 'no_bell', 'crown', 'information_source', 'open_hands', 'necktie', 'sob', 'card_index', 'evergreen_tree', 'partly_sunny', 'sweat_drops', 'telescope', 'mega', 'orange_book', 'gemini', 'cat', 'black_medium_square', 'basketball', 'older_man', 'green_heart', 'u6708', 'unlock', 'sunny', 'wolf', 'repeat', 'man_with_turban', 'helicopter', 'electric_plug', 'name_badge', 'aries', 'european_post_office', 'earth_americas', 'clock230', 'white_large_square', 'baggage_claim', 'raising_hand', 'bookmark', 'jeans', 'arrow_double_down', 'peach', 'honeybee', 'ship', 'woman', 'grinning', 'toilet', 'checkered_flag', 'copyright', 'pound', 'pear', 'candy', 'japanese_ogre', 'bust_in_silhouette', 'diamonds', 'abcd', 'vertical_traffic_light', 'u7533', 'horse_racing', 'police_car', 'waxing_gibbous_moon', 'fearful', 'knife', 'collision', 'globe_with_meridians', 'cloud', 'earth_africa', 'tongue', 'flashlight', 'confused', 'mouse2', 'school_satchel', 'movie_camera', 'christmas_tree', 'radio_button', 'swimmer', 'boy', 'pager', 'baby_bottle', 'whale2', 'scream', 'smiley', 'pineapple', 'rooster', 'hand', 'smoking', 'oncoming_taxi', 'snake', 'princess', 'ski', 'red_car', 'ok_hand', 'tokyo_tower', 'melon', 'u6307', 'banana', 'o2', 'sailboat', 'dolls', 'angry', 'fax', 'egg', 'fire', 'arrow_right_hook', 'trumpet', 'revolving_hearts', 'kissing_closed_eyes', 'heartpulse', 'joy_cat', 'cow2', 'girl', 'credit_card', 'mens', 'mountain_cableway', 'oden', 'thumbsdown', 'closed_lock_with_key', 'disappointed_relieved', 'football', 'fire_engine', 'baby_chick', 'fishing_pole_and_fish', 'cold_sweat', 'cactus', 'u7a7a', 'flushed', 'palm_tree', 'shit', 'house_with_garden', 'blowfish', 'shower', 'monorail', 'arrow_forward', 'performing_arts', 'white_small_square', 'arrow_lower_right', 'non-potable_water', 'cn', 'arrows_clockwise', 'capricorn', 'outbox_tray', 'circus_tent', 'leaves', 'clock2', 'book', 'o', 'file_folder', 'foggy', 'u5272', 'satisfied', 'surfer', '+1', 'arrow_right', 'traffic_light', 'low_brightness', 'u7981', 'ice_cream', 'secret', '100', 'dart', 'strawberry', 'milky_way', 'bug', 'package', 'radio', 'calling', 'clock1030', 'pencil2', 'octopus', 'no_mobile_phones', 'aquarius', 'tiger2', 'two_men_holding_hands', 'factory', 'uk', 'hourglass', 'earth_asia', 'taxi', 'tanabata_tree', 'cry', 'spaghetti', 'baseball', 'microphone', 'handbag', 'man', 'dromedary_camel', 'two_hearts', 'ferris_wheel', 'point_right', 'wind_chime', 'yellow_heart', 'congratulations', 'bangbang', 'no_pedestrians', 'cow', 'de', 'oncoming_bus', 'blue_car', 'church', 'no_bicycles', 'rat', 'do_not_litter', 'sunflower', 'speaker', 'flipper', 'no_good', 'left_right_arrow', 'warning', 'santa', 'construction', 'mailbox', 'articulated_lorry', 'guardsman', 'mailbox_with_mail', 'mailbox_closed', 'negative_squared_cross_mark', 'soon', 'hotsprings', 'japan', 'oncoming_police_car', 'couple', 'free', 'tangerine', 'first_quarter_moon', 'sa', 'u5408', 'six_pointed_star', 'tomato', 'new_moon', 'grin', 'white_flower', 'dragon', 'truck', 'cherries', 'tropical_drink', 'postbox', 'seedling', 'high_brightness', 'boat', 'lock', 'arrow_double_up', 'stars', 'bathtub', 'sos', 'statue_of_liberty', 'speedboat'}

    def apply(self, **kwargs):
        # only handle those not otherwise defined in the document
        to_handle = self.emojis - set(self.document.substitution_defs)
        for ref in self.document.traverse(nodes.substitution_reference):
            refname = ref['refname']
            if refname in to_handle:
                node = nodes.image(
                    uri='http://www.tortue.me/emoji/{0}.png'.format(refname),
                    alt=refname,
                    classes=['emoji'],
                    height="24px",
                    width="24px")
                ref.replace_self(node)



class WalikiReader(Reader):

    def get_transforms(self):
        transforms = [str2object(transform) for transform in WALIKI_RST_TRANSFORMS]
        return Reader.get_transforms(self) + transforms


