import fanstatic
import js.jquery

library = fanstatic.Library('jquery.simulate', 'resources')

simulate = fanstatic.Resource(
    library, 'jquery.simulate.js',
    depends=[js.jquery.jquery])
