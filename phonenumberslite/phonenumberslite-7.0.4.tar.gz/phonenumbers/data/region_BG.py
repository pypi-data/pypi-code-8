"""Auto-generated file, do not edit by hand. BG metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BG = PhoneMetadata(id='BG', country_code=359, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[23567]\\d{5,7}|[489]\\d{6,8}', possible_number_pattern='\\d{5,9}'),
    fixed_line=PhoneNumberDesc(national_number_pattern='2(?:[0-8]\\d{5,6}|9\\d{4,6})|(?:[36]\\d|5[1-9]|8[1-6]|9[1-7])\\d{5,6}|(?:4(?:[124-7]\\d|3[1-6])|7(?:0[1-9]|[1-9]\\d))\\d{4,5}', possible_number_pattern='\\d{5,8}', example_number='2123456'),
    mobile=PhoneNumberDesc(national_number_pattern='(?:8[7-9]|98)\\d{7}|4(?:3[0789]|8\\d)\\d{5}', possible_number_pattern='\\d{8,9}', example_number='48123456'),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{5}', possible_number_pattern='\\d{8}', example_number='80012345'),
    premium_rate=PhoneNumberDesc(national_number_pattern='90\\d{6}', possible_number_pattern='\\d{8}', example_number='90123456'),
    shared_cost=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    personal_number=PhoneNumberDesc(national_number_pattern='700\\d{5}', possible_number_pattern='\\d{5,9}', example_number='70012345'),
    voip=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    pager=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    uan=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    voicemail=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(2)(\\d{5})', format='\\1 \\2', leading_digits_pattern=['29'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(2)(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['2'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['43[124-7]|70[1-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{2})', format='\\1 \\2 \\3', leading_digits_pattern=['43[124-7]|70[1-9]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[78]00'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2,3})', format='\\1 \\2 \\3', leading_digits_pattern=['[356]|4[124-7]|7[1-9]|8[1-6]|9[1-7]'], national_prefix_formatting_rule='0\\1'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['48|8[7-9]|9[08]'], national_prefix_formatting_rule='0\\1')],
    mobile_number_portable_region=True)
