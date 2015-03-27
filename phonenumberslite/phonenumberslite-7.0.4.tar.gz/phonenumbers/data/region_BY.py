"""Auto-generated file, do not edit by hand. BY metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BY = PhoneMetadata(id='BY', country_code=375, international_prefix='810',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-4]\\d{8}|[89]\\d{9,10}', possible_number_pattern='\\d{7,11}'),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:1(?:5(?:1[1-5]|[24]\\d|6[2-4]|9[1-7])|6(?:[235]\\d|4[1-7])|7\\d{2})|2(?:1(?:[246]\\d|3[0-35-9]|5[1-9])|2(?:[235]\\d|4[0-8])|3(?:[26]\\d|3[02-79]|4[024-7]|5[03-7])))\\d{5}', possible_number_pattern='\\d{7,9}', example_number='152450911'),
    mobile=PhoneNumberDesc(national_number_pattern='(?:2(?:5[5679]|9[1-9])|33\\d|44\\d)\\d{6}', possible_number_pattern='\\d{9}', example_number='294911911'),
    toll_free=PhoneNumberDesc(national_number_pattern='8(?:0[13]|20\\d)\\d{7}', possible_number_pattern='\\d{10,11}', example_number='8011234567'),
    premium_rate=PhoneNumberDesc(national_number_pattern='(?:810|902)\\d{7}', possible_number_pattern='\\d{10}', example_number='9021234567'),
    shared_cost=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    personal_number=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    voip=PhoneNumberDesc(national_number_pattern='249\\d{6}', possible_number_pattern='\\d{9}', example_number='249123456'),
    pager=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    uan=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    voicemail=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='8(?:[013]|[12]0)\\d{8}|902\\d{7}', possible_number_pattern='\\d{10,11}', example_number='82012345678'),
    preferred_international_prefix='8~10',
    national_prefix='8',
    national_prefix_for_parsing='8?0?',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2})(\\d{2})', format='\\1 \\2-\\3-\\4', leading_digits_pattern=['17[0-3589]|2[4-9]|[34]', '17(?:[02358]|1[0-2]|9[0189])|2[4-9]|[34]'], national_prefix_formatting_rule='8 0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{2})(\\d{2})', format='\\1 \\2-\\3-\\4', leading_digits_pattern=['1(?:5[24]|6[235]|7[467])|2(?:1[246]|2[25]|3[26])', '1(?:5[24]|6(?:2|3[04-9]|5[0346-9])|7(?:[46]|7[37-9]))|2(?:1[246]|2[25]|3[26])'], national_prefix_formatting_rule='8 0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{2})(\\d{3})', format='\\1 \\2-\\3', leading_digits_pattern=['1(?:5[169]|6[3-5]|7[179])|2(?:1[35]|2[34]|3[3-5])', '1(?:5[169]|6(?:3[1-3]|4|5[125])|7(?:1[3-9]|7[0-24-6]|9[2-7]))|2(?:1[35]|2[34]|3[3-5])'], national_prefix_formatting_rule='8 0\\1'),
        NumberFormat(pattern='([89]\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['8[01]|9'], national_prefix_formatting_rule='8 \\1'),
        NumberFormat(pattern='(8\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['82'], national_prefix_formatting_rule='8 \\1')],
    mobile_number_portable_region=True)
