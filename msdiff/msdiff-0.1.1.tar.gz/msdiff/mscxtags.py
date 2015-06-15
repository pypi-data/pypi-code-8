problematic_spanners = [
    'endSpanner',
    'Glissando',
    'HairPin',
    'Ottava',
    'Pedal',
    'Slur',
    'Tie'
]

problematic_invisible = ['BarLine'] + problematic_spanners

# Tags of the elements that can be colored with a single call
# of `set_color`.
simple_colorable_tags = [
  'Accidental',
  'Arpeggio',
  'Articulation',
  'BarLine',
  'Breath',
  'Clef',
  'Dynamic',
  'Glissando',
  'HairPin',
  'KeySig',
  'Note',
  'Ottava',
  'Pedal',
  'RepeatMeasure',
  'Rest',
  'TimeSig',
  'Tremolo',
  'Trill'
]
