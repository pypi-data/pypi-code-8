"""HEC-RAS Output variables

-------------------------------------------------------------------------------
| Name              | ID | Description                                        |
-------------------------------------------------------------------------------
  PROFILE               1  Profile number.
  WS_ELEV               2  Calculated water surface from energy equation.
  EG_ELEV               3  Energy gradeline for given WSEL.
  MAX_CHL_DPTH          4  Maximum main channel depth.
  MIN_CH_EL             5  Minimum channel elevation.
  Q_LEFT                6  Flow in left overbank.
  Q_CHANNEL             7  Flow in main channel.
  Q_RIGHT               8  Flow in right overbank.
  Q_TOTAL               9  Total flow in cross section.
  FLOW_AREA            10  Total area of cross section active flow.
  FLOW_AREA_L          11  Area of left overbank active flow.
  FLOW_AREA_CH         12  Area of main channel active flow.
  FLOW_AREA_R          13  Area of right overbank active flow.
  WP_TOTAL             14  Wetted perimeter of total cross section.
  WP_LEFT              15  Wetted perimeter of left overbank.
  WP_CHANNEL           16  Wetted perimeter of main channel.
  WP_RIGHT             17  Wetted perimeter of right overbank.
  CONV_TOTAL           18  Conveyance of total cross section.
  CONV_LEFT            19  Conveyance of left overbank.
  CONV_CHNL            20  Conveyance of main channel.
  CONV_RIGHT           21  Conveyance of right overbank.
  VEL_HEAD             22  Velocity head.
  VEL_TOTAL            23  Average velocity of flow in total cross section.
  VEL_LEFT             24  Average velocity of flow in left overbank.
  VEL_CHNL             25  Average velocity of flow in main channel.
  VEL_RIGHT            26  Average velocity of flow in right overbank.
  ALPHA                27  Alpha - energy weighting coefficient.
  BETA                 28  Beta - momentum weighting coefficient.
  TOP_WDTH_ACT         29  Top width of the wetted cross section, not including
                           ineffective flow.
  EG_SLOPE             30  Slope of the energy grade line at a cross section.
  VOLUME               31  Cumulative volume of water from the downstream end
                           of the reach (including ineffective areas).
  AREA                 32  Flow area of the entire cross section including
                           ineffective flow.
  AREA_LEFT            33  Flow area of the left overbank including ineffective
                           flow.
  AREA_CHANNEL         34  Flow area of the main channel including ineffective
                           flow.
  AREA_RIGHT           35  Flow area of the right overbank including
                           ineffective flow.
  STA_WS_LFT           36  Left station where water intersects the ground.
  STA_WS_RGT           37  Right station where water intersects the ground.
  LEFT_STA_EFF         38  Furthest left station where there is effective flow.
  RGHT_STA_EFF         39  Furthest right station that still has effective
                           flow.
  LENGTH_WTD           40  Weighted length based on flow distribution, in left
                           bank, channel, and right bank.
  LENGTH_LEFT          41  Downstream reach length of the left overbank.
  LENGTH_CHNL          42  Downstream reach length of the main channel to next
                           XS (unless BR is d/s, then this is the distance to
                           the deck/roadway).
  LENGTH_RGHT          43  Downstream reach length of the right overbank.
  MANN_WTD_LEFT        44  Conveyance weighted Manning's n for the left
                           overbank.
  MANN_WTD_CHNL        45  Conveyance weighted Manning's n for the main
                           channel.
  MANN_WTD_RGHT        46  Conveyance weighted Manning's n for the right
                           overbank.
  MANN_COMP            47  Mannings n value for main channel based on composite
                           roughness equation.
  FROUDE_N_CHL         48  Froude number for the main channel.
  FROUDE_N_XS          49  Froude number for the entire cross section.
  TRVL_TME_AVG         50  Cumulative travel time based on the average velocity
                           of the entire cross section per reach.
  TRVL_TME_CHL         51  Cumulative travel time based on the average velocity
                           of the main channel per reach.
  CONV_RATIO           52   Ratio of the conveyance of the current cross
                           section to the conveyance of the downstream cross
                           section.
  SPECIF_FORCE         53  The specific force for this cross section at the
                           computed water surface elevation.
  SPC_FORCE_PR         54  Specific force prime.  For mixed flow, the specific
                           force at this cross section for the flow regime that
                           does not control.
  WS_PRIME             55  Water surface prime.  For mixed flow, the water
                           surface of the flow regime that does not control.
  CRIT_WS              56  Critical water surface elevation.  Water surface
                           corresponding to the minimum energy on the energy
                           versus depth curve.
  CRIT_EG              57  Critical energy elevation.  Minumum energy on the
                           energy versus depth curve.
  CRIT_DEPTH           58  Critical depth.  Corresponds to critical water
                           surface.
  FRCTN_LOSS           59  Friction loss between two cross sections.
  C_E_LOSS             60  Contraction or expansion loss between two cross
                           sections.
  HEADLOSS             61  Total energy loss between two cross sections.
  TOP_WIDTH            62  Top width of the wetted cross section.
  TOP_W_LEFT           63  Top width of the left overbank.  Does not include
                           `islands', but it does include ineffective flow.
  TOP_W_CHNL           64  Top width of the main channel.  Does not include
                           `islands', but it does include ineffective flow.
  TOP_W_RIGHT          65  Top width of the right overbank.  Does not include
                           `islands', but it does include ineffective flow.
  NUM_TRIALS           66  Current number (or final number) of trials attempted
                           before the energy equation is balanced.
  STD_STP_CASE         67  Standard step method used to determine WSEL (1 =
                           successful convergence, 2 = minimum error,
                           3 = resorted to critical depth).
  FRCTN_SLOPE          68  Representative friction slope between two cross
                           sections.
  FRCTN_SLP_MD         69  Friction slope averaging method used.
  MIN_ERROR            70  The minimum error, between the calculated and
                           assumed water surfaces when balancing the energy
                           equation.
  DELTA_WS             71  Change in water surface through culvert(s) and
                           Bridge(s).
  DELTA_EG             72  Change in energy grade line through culvert(s) and
                           Bridge(s).
  Q_CULV_GROUP         73  Flow through all barrels in a culvert.
  Q_BARREL             74  Flow through one barrel in a culvert.
  WS_US                75  Upstream water surface elevation upstream of bridge,
                           culvert or weir (specific to that opening, not
                           necessarily the energy weighted average).
  CLV_EG_NO_WR         76  Energy grade elevation at the culvert that was
                           calculated without the weir.
  EG_US                77  Upstream energy grade elevation at bridge or culvert
                           (specific to that opening, not necessarily the
                           weighted average).
  EG_IC                78  Upstream energy gradeline based on inlet control.
  EG_OC                79  Upstream energy gradeline based on outlet control.
  CULV_NML_DEPTH       80  Normal depth for this culvert (and flow).
  CULV_VEL_DS          81  Velocity in culvert at defined downstream.
  CULV_VEL_US          82  Velocity in culvert at defined upstream.
  CULV_FRCTN_LS        83  Friction loss through the culvert.
  CULV_ENTR_LOSS       84  Entrance loss (energy loss due only to entrance).
  CULV_EXIT_LOSS       85  Exit loss (energy loss due to exit).
  CULV_FULL_LEN        86  The length that the culvert flows full.
  CULV_CRT_DEPTH       87  Critical depth inside the culvert.
  CULV_INV_EL_UP       88  Culvert invert elevation upstream.
  CULV_INV_EL_DN       89  Culvert invert elevation downstream.
  CULV_EG_INLET        90  Energy gradeline inside the culvert at the inlet.
  CULV_EG_OUTLET       91  Energy gradeline inside the culvert at the outlet.
  CULV_WS_INLET        92  Water surface elevation inside the culvert at the
                           inlet.
  CULV_WS_OUTLET       93  Water surface elevation inside the culvert at the
                           outlet.
  Q_WEIR               94  Flow over the weir.
  WEIR_FLOW_AREA       95  Area of the flow going over the weir.
  WEIR_STA_LFT         96  Station where flow starts on the left side.
  WEIR_STA_RGT         97  Station where flow ends on the right side.
  WEIR_MAX_DEPTH       98  The maximum depth over the weir.
  WEIR_AVG_DEPTH       99  The average depth over the weir.
  WEIR_SUBMERG        100  The ratio of the downstream depth above the weir to
                           the upstream depth above the weir.
  MIN_EL_WEIR_FLOW    101  Elevation where weir flow begins.
  WR_TOP_WDTH         102  Top width of water over the weir.
  ENERGY_WR_WS        103  Water surface elevation upstream of bridge for low
                           flow energy method and weir flow.
  YARNELL_WS          104  Water surface elevation upstream of bridge for
                           Yarnell method.
  WSPRO_WS            105  Water surface elevation upstream of bridge for the
                           WSPRO method.
  PRS_WR_WS_          106  Water surface elevation upstream of bridge for
                           pressure and/or weir method.
  ENERGY_WS           107  Water surface elevation upstream of bridge for
                           energy only method.
  MOMEN_WS            108  Water surface elevation upstream of bridge for
                           momentum method.
  PRS_O_WS            109  Water surface elevation upstream of bridge for
                           pressure only method.
  ENERGY_WR_EG        110  Energy grade elevation upstream of bridge for energy
                           method .
  YARNELL_EG          111  Energy grade elevation upstream of bridge for
                           Yarnell method.
  WSPRO_EG            112  Energy grade elevation upstream of bridge for the
                           WSPRO method.
  PRS_WR_EG           113  Energy grade elevation upstream of bridge for
                           pressure and/or weir method.
  ENERGY_EG           114  Energy grade elevation upstream of bridge for energy
                           only method.
  MOMEN_EG            115  Energy grade elevation upstream of bridge for
                           momentum method.
  PRS_O_EG            116  Energy grade elevation upstream of bridge for
                           pressure only method.
  BR_SEL_METHOD       117  Selected bridge method.
  MIN_EL_PRS          118  Elevation at the bridge when pressure flow begins.
  CRIT_NUM            119  Number of critical depths found.
  CRIT_WS_1           120  Water surface elevation of first critical depth.
  CRIT_WS_2           121  Water surface elevation of second critical depth.
  CRIT_WS_3           122  Water surface elevation of third critical depth.
  CRIT_ENRGY_1        123  Energy associated with first critical depth.
  CRIT_ENRGY_2        124  Energy associated with second critical depth.
  CRIT_ENRGY_3        125  Energy associated with third critical depth.
  HYDR_DEPTH          126  Hydraulic depth for cross section.
  HYDR_DEPTH_L        127  Hydraulic depth in left over bank.
  HYDR_DEPTH_C        128  Hydraulic depth in channel.
  HYDR_DEPTH_R        129  Hydraulic depth for right over bank.
  DECK_WIDTH          130  Width of Deck.
  N_BARRELS           131  Number of barrels in a culvert.
  Q_BRIDGE            132  Flow through a bridge opening.
  VOL_LEFT            133  Cumulative volume of water in the left overbank from
                           the downstream end of the reach (including
                           ineffective areas).
  VOL_CHAN            134  Cumulative volume of water in the channel from the
                           downstream end of the reach (including ineffective
                           areas).
  VOL_RIGHT           135  Cumulative volume of water in the right overbank
                           from the downstream end of the reach (including
                           ineffective areas).
  MIN_EL              136  Minimum overall section elevation.
  ENC_VAL_1           137  Target for encroachment analysis.
  ENC_VAL_2           138  Second target for encroachment analysis.
  ENC_STA_L           139  Left station of encroachment.
  ENC_STA_R           140  Right station of encroachment.
  DIST_CENTER_L       141  Distance from center of channel to left
                           encroachment.
  DIST_CENTER_R       142  Distance from center of channel to right
                           encroachment.
  K_PERC_L            143  Conveyance reduction from left encroachment.
  K_PERC_R            144  Conveyance reduction from right encroachment.
  Q_PERC_L            145  Percent of flow in left overbank.
  Q_PERC_CHAN         146  Percent of flow in main channel.
  Q_PERC_R            147  Percent of flow in right overbank.
  PROF_DELTA_WS       148  Difference in WS between current profile and WS for
                           first profile.
  PROF_DELTA_EG       149  Difference in EG between current profile and EG for
                           first profile.
  SHEAR_TOTAL         150  Shear stress in total section.
  SHEAR_LOB           151  Shear stress in left overbank.
  SHEAR_CHAN          152  Shear stress in main channel.
  SHEAR_ROB           153  Shear stress in right overbank.
  POWER_TOTAL         154  Total stream power.
  POWER_LOB           155  Total stream power in left overbank.
  POWER_CHAN          156  Total stream power in main channel.
  POWER_ROB           157  Total stream power in right overbank.
  CH_STA_L            158  Left station of channel.
  CH_STA_R            159  Right station of channel.
  BASE_WS             160  Water surface for first profile (used in comparison
                           of encroachments).
  CENTER_STATION      161  Center station of main channel.
  XS_DELTA_WS         162  Change in water surface between current section and
                           next one downstream.
  XS_DELTA_EG         163  Change in energy gradeline between current section
                           and next one downstream.
  SA_TOTAL            164  Cumulative surface area for entire cross section
                           (including ineffective areas) from the downstream
                           end of the reach.
  SA_LEFT             165  Cumulative surface area for left overbank (including
                           ineffective areas) from the downstream end of the
                           reach.
  SA_CHAN             166  Cumulative surface area for main channel (including
                           ineffective areas) from the downstream end of the
                           reach.
  SA_RIGHT            167  Cumulative surface area for right overbank
                           (including ineffective areas) from the downstream
                           end of the reach.
  ENC_METHOD          168  Encroachment method.
  Q_GATE_GROUP        169  Flow through all gate openings in a gate group.
  GATE_OPEN_HT        170  Height of gate opening.
  GATE_NOPEN          171  The number of gates opened in the current group.
  GATE_AREA           172  The flow area in an opened gate.
  GATE_SUBMERG        173  The ratio of the downstream depth above the gate to
                           the upstream depth above the gate.
  GATE_INVERT         174  Gate spillway invert elevation.
  Q_GATES             175  Total flow through all of the gate groups of an
                           inline/lateral structure.
  BR_OPEN_AREA        176  Total area of the entire bridge opening.
  COEF_OF_Q           177  WSPRO bridge method coefficient of discharge.
  CUM_CH_LEN          178  Cumulative Channel Length from the downstream end of
                           the reach.
  ENC_WD              179  Encroachment Width.
  OBS_WS              180  Observed Water Surface.
  WS_AIR_ENTR         181  Water surface elevation accounting for air
                           entrainment.
  BR_OPEN_VEL         182  Average velocity inside the bridge opening (Maximum
                           of BU and BD).
  ICE_THICK_LOB       183  Ice thickness in the left overbank.
  ICE_THICK_CHAN      184  Ice thickness in the main channel.
  ICE_THICK_ROB       185  Ice thickness in the right overbank.
  ICE_VOL_TOTAL       186  Cummulative volume of ice in an ice jam.
  ICE_VOL_LOB         187  Cummulative volume of ice in the left overbank for
                           an ice jam.
  ICE_VOL_CHAN        188  Cummulative volume of ice in the main channel for an
                           ice jam.
  ICE_VOL_ROB         189  Cummulative volume of ice in the right overbank for
                           an ice jam.
  ICE_TOP_LOB         190  The top elevation of ice in the left overbank.
  ICE_TOP_CHAN        191  The top elevation of ice in the main channel.
  ICE_TOP_ROB         192  The top elevation of ice in the right overbank.
  ICE_BTM_LOB         193  The bottom elevation of ice in the left overbank.
  ICE_BTM_CHAN        194  The bottom elevation of ice in the main channel.
  ICE_BTM_ROB         195  The bottom elevation of ice in the right overbank.
  INVERT_SLOPE        196  The slope from the invert of this cross section to
                           the next cross section downstream.
  LOB_ELEV            197  The ground elevation at the left bank of the main
                           channel.
  ROB_ELEV            198  The ground elevation at the right bank of the main
                           channel.
  L_FREEBOARD         199  The freeboard in the main channel at the left bank.
  R_FREEBOARD         200  The freeboard in the main channel at the right bank.
  LEVEE_EL_LEFT       201  The elevation of the left levee.
  LEVEE_EL_RIGHT      202  The elevation of the right levee.
  INEFF_EL_LEFT       203  The elevation of the left ineffective area.
  INEFF_EL_RIGHT      204  The elevation of the right ineffective area.
  L_LEVEE_FRBRD       205  The freeboard before the left levee is over-topped.
  R_LEVEE_FRBRD       206  The freeboard before the right levee is over-topped.
  MANN_WTD_TOTAL      207  Mannings n value for the total main cross section.
  HYDR_RADIUS         208  Hydraulic radius for cross section.
  HYDR_RADIUS_L       209  Hydraulic radius in left over bank.
  HYDR_RADIUS_C       210  Hydraulic radius in channel.
  HYDR_RADIUS_R       211  Hydraulic radius for right over bank.
  HYDR_RAD_2_3        212  Hydraulic radius for cross section to the 2/3 power.
  WS_DS               213  Water surface downstream.
  EG_DS               214  Energy elevation downstream.
  MIN_WEIR_EL         215  Minimum weir elevation.
  PERC_Q_LEAVING      216  Percentage of flow leaving through a lateral
                           structure.
  Q_US                217  Flow in cross section upstream of a lateral
                           structure.
  Q_DS                218  Flow in cross section downstream of lateral
                           structure.
  WEIR_STA_US         219  Upstream station for weir flow starts.
  WEIR_STA_DS         220  Downstream station where weir flow ends.
  Q_LEAVING_TOTAL     221  Total flow leaving in a lateral structure including
                           all gates, culverts and lateral rating curves.
  SA_MIN_EL           222  Minimum elevation of a storage area.
  SA_AREA             223  Surface area of a storage area.
  SA_VOLUME           224  Storage volume of a storage area.
  TOP_W_ACT_LEFT      225  Top width of the wetted left bank, not including
                           ineffective flow.
  TOP_W_ACT_CHAN      226  Top width of the wetted channel, not including
                           ineffective flow.
  TOP_W_ACT_RIGHT     227  Top width of the wetted right bank, not including
                           ineffective flow.
  CULV_DEPTH_BLOCKED  228  Depth of fill in a culvert.
  CULV_INLET_MANN_N   229  The composite n value at the culvert inlet.
  CULV_OUTLET_MANN_N  230  The composite n value at the culvert outlet.
  ICE_WS_ERR          231  Convergence error in water surface for dynamic ice
                           jam.
  ICE_ERR             232  Convergence error in ice thickness for dynamic ice
                           jam.
  PIPING_FLOW         233  Flow from piping weir failure.
  BREACH_CL           234  Center line of weir breach.
  BREACH_WD           235  Bottom width of weir breach.
  BREACH_BOTTOM_EL    236  Bottom Elevation of weir breach.
  BREACH_TOP_EL       237  Top Elevation of weir breach.
  BREACH_SSL          238  Left side slope of weir breach.
  BREACH_SSR          239  Right side slope of weir breach.
  Q_PUMP_GROUP        240  Pump group flow.
  Q_LAT_RC            241  Lateral rating curve flow.
  Q_CULV              242  Total flow in all culvert groups.
  CULV_LENGTH         243  Length of the culvert barrel.
  Q_PUMP_STATION      244  Total flow in all pump groups in a pump station.
  WS_INLET            245  WS at the inlet of a pump station.
  WS_OUTLET           246  WS at the outlet of a pump station.
  PUMPING_HEAD        247  Pumping head for the pump station.
  INFLOW              248  Total inflow into a storage area.
  OUTFLOW             249  Total outflow into a storage area.
  NET_FLUX            250  Net inflow - outflow for a storage area.
  ENC_OFFSET_L        251  Minimum setback from the left overbank station.
  ENC_OFFSET_R        252  Minimum setback from the right overbank station.
  MIN_CH_PILOT        253  Minimum channel elevation (including pilot
                           channels).
  DIFF                254  Difference between the previous two columns.
  MIN_CH_EL_STA       255  Station of the minimum channel elevation.
  CULV_AREA_DS        256  Cross sectional flow area in culvert at defined
                           downstream.
  CULV_AREA_US        257  Cross sectional flow area in culvert at defined
                           upstream.
  GATE_WEIR_COEF      258  Coefficient used in weir flow over the gate.
  WEIR_COEF           259  Coefficient used in weir flow.
  Q_BREACH            260  Flow through a breach.
  BREACH_AVG_VELOCITY 261  Average flow velocity through a breach.
  BREACH_FLOW_AREA    262  Flow area through a breach.
  LEFT_STATION        263  Left station of the cross section.
  RIGHT_STATION       264  Right station of the cross section.
  LEVEE_STA_LEFT      265  Left levee station.
  LEVEE_STA_RIGHT     266  Right levee station.
  Q_INLINE_RC         267  Inline Outlet rating curve flow.
  Q_OUTLET_TS         268  Inline/Lateral Outlet time series flow.
  """
import sys


PROFILE = 1
WS_ELEV = 2
EG_ELEV = 3
MAX_CHL_DPTH = 4
MIN_CH_EL = 5
Q_LEFT = 6
Q_CHANNEL = 7
Q_RIGHT = 8
Q_TOTAL = 9
FLOW_AREA = 10
FLOW_AREA_L = 11
FLOW_AREA_CH = 12
FLOW_AREA_R = 13
WP_TOTAL = 14
WP_LEFT = 15
WP_CHANNEL = 16
WP_RIGHT = 17
CONV_TOTAL = 18
CONV_LEFT = 19
CONV_CHNL = 20
CONV_RIGHT = 21
VEL_HEAD = 22
VEL_TOTAL = 23
VEL_LEFT = 24
VEL_CHNL = 25
VEL_RIGHT = 26
ALPHA = 27
BETA = 28
TOP_WDTH_ACT = 29
EG_SLOPE = 30
VOLUME = 31
AREA = 32
AREA_LEFT = 33
AREA_CHANNEL = 34
AREA_RIGHT = 35
STA_WS_LFT = 36
STA_WS_RGT = 37
LEFT_STA_EFF = 38
RGHT_STA_EFF = 39
LENGTH_WTD = 40
LENGTH_LEFT = 41
LENGTH_CHNL = 42
LENGTH_RGHT = 43
MANN_WTD_LEFT = 44
MANN_WTD_CHNL = 45
MANN_WTD_RGHT = 46
MANN_COMP = 47
FROUDE_N_CHL = 48
FROUDE_N_XS = 49
TRVL_TME_AVG = 50
TRVL_TME_CHL = 51
CONV_RATIO = 52
SPECIF_FORCE = 53
SPC_FORCE_PR = 54
WS_PRIME = 55
CRIT_WS = 56
CRIT_EG = 57
CRIT_DEPTH = 58
FRCTN_LOSS = 59
C_E_LOSS = 60
HEADLOSS = 61
TOP_WIDTH = 62
TOP_W_LEFT = 63
TOP_W_CHNL = 64
TOP_W_RIGHT = 65
NUM_TRIALS = 66
STD_STP_CASE = 67
FRCTN_SLOPE = 68
FRCTN_SLP_MD = 69
MIN_ERROR = 70
DELTA_WS = 71
DELTA_EG = 72
Q_CULV_GROUP = 73
Q_BARREL = 74
WS_US = 75
CLV_EG_NO_WR = 76
EG_US = 77
EG_IC = 78
EG_OC = 79
CULV_NML_DEPTH = 80
CULV_VEL_DS = 81
CULV_VEL_US = 82
CULV_FRCTN_LS = 83
CULV_ENTR_LOSS = 84
CULV_EXIT_LOSS = 85
CULV_FULL_LEN = 86
CULV_CRT_DEPTH = 87
CULV_INV_EL_UP = 88
CULV_INV_EL_DN = 89
CULV_EG_INLET = 90
CULV_EG_OUTLET = 91
CULV_WS_INLET = 92
CULV_WS_OUTLET = 93
Q_WEIR = 94
WEIR_FLOW_AREA = 95
WEIR_STA_LFT = 96
WEIR_STA_RGT = 97
WEIR_MAX_DEPTH = 98
WEIR_AVG_DEPTH = 99
WEIR_SUBMERG = 100
MIN_EL_WEIR_FLOW = 101
WR_TOP_WDTH = 102
ENERGY_WR_WS = 103
YARNELL_WS = 104
WSPRO_WS = 105
PRS_WR_WS_ = 106
ENERGY_WS = 107
MOMEN_WS = 108
PRS_O_WS = 109
ENERGY_WR_EG = 110
YARNELL_EG = 111
WSPRO_EG = 112
PRS_WR_EG = 113
ENERGY_EG = 114
MOMEN_EG = 115
PRS_O_EG = 116
BR_SEL_METHOD = 117
MIN_EL_PRS = 118
CRIT_NUM = 119
CRIT_WS_1 = 120
CRIT_WS_2 = 121
CRIT_WS_3 = 122
CRIT_ENRGY_1 = 123
CRIT_ENRGY_2 = 124
CRIT_ENRGY_3 = 125
HYDR_DEPTH = 126
HYDR_DEPTH_L = 127
HYDR_DEPTH_C = 128
HYDR_DEPTH_R = 129
DECK_WIDTH = 130
N_BARRELS = 131
Q_BRIDGE = 132
VOL_LEFT = 133
VOL_CHAN = 134
VOL_RIGHT = 135
MIN_EL = 136
ENC_VAL_1 = 137
ENC_VAL_2 = 138
ENC_STA_L = 139
ENC_STA_R = 140
DIST_CENTER_L = 141
DIST_CENTER_R = 142
K_PERC_L = 143
K_PERC_R = 144
Q_PERC_L = 145
Q_PERC_CHAN = 146
Q_PERC_R = 147
PROF_DELTA_WS = 148
PROF_DELTA_EG = 149
SHEAR_TOTAL = 150
SHEAR_LOB = 151
SHEAR_CHAN = 152
SHEAR_ROB = 153
POWER_TOTAL = 154
POWER_LOB = 155
POWER_CHAN = 156
POWER_ROB = 157
CH_STA_L = 158
CH_STA_R = 159
BASE_WS = 160
CENTER_STATION = 161
XS_DELTA_WS = 162
XS_DELTA_EG = 163
SA_TOTAL = 164
SA_LEFT = 165
SA_CHAN = 166
SA_RIGHT = 167
ENC_METHOD = 168
Q_GATE_GROUP = 169
GATE_OPEN_HT = 170
GATE_NOPEN = 171
GATE_AREA = 172
GATE_SUBMERG = 173
GATE_INVERT = 174
Q_GATES = 175
BR_OPEN_AREA = 176
COEF_OF_Q = 177
CUM_CH_LEN = 178
ENC_WD = 179
OBS_WS = 180
WS_AIR_ENTR = 181
BR_OPEN_VEL = 182
ICE_THICK_LOB = 183
ICE_THICK_CHAN = 184
ICE_THICK_ROB = 185
ICE_VOL_TOTAL = 186
ICE_VOL_LOB = 187
ICE_VOL_CHAN = 188
ICE_VOL_ROB = 189
ICE_TOP_LOB = 190
ICE_TOP_CHAN = 191
ICE_TOP_ROB = 192
ICE_BTM_LOB = 193
ICE_BTM_CHAN = 194
ICE_BTM_ROB = 195
INVERT_SLOPE = 196
LOB_ELEV = 197
ROB_ELEV = 198
L_FREEBOARD = 199
R_FREEBOARD = 200
LEVEE_EL_LEFT = 201
LEVEE_EL_RIGHT = 202
INEFF_EL_LEFT = 203
INEFF_EL_RIGHT = 204
L_LEVEE_FRBRD = 205
R_LEVEE_FRBRD = 206
MANN_WTD_TOTAL = 207
HYDR_RADIUS = 208
HYDR_RADIUS_L = 209
HYDR_RADIUS_C = 210
HYDR_RADIUS_R = 211
HYDR_RAD_2_3 = 212
WS_DS = 213
EG_DS = 214
MIN_WEIR_EL = 215
PERC_Q_LEAVING = 216
Q_US = 217
Q_DS = 218
WEIR_STA_US = 219
WEIR_STA_DS = 220
Q_LEAVING_TOTAL = 221
SA_MIN_EL = 222
SA_AREA = 223
SA_VOLUME = 224
TOP_W_ACT_LEFT = 225
TOP_W_ACT_CHAN = 226
TOP_W_ACT_RIGHT = 227
CULV_DEPTH_BLOCKED = 228
CULV_INLET_MANN_N = 229
CULV_OUTLET_MANN_N = 230
ICE_WS_ERR = 231
ICE_ERR = 232
PIPING_FLOW = 233
BREACH_CL = 234
BREACH_WD = 235
BREACH_BOTTOM_EL = 236
BREACH_TOP_EL = 237
BREACH_SSL = 238
BREACH_SSR = 239
Q_PUMP_GROUP = 240
Q_LAT_RC = 241
Q_CULV = 242
CULV_LENGTH = 243
Q_PUMP_STATION = 244
WS_INLET = 245
WS_OUTLET = 246
PUMPING_HEAD = 247
INFLOW = 248
OUTFLOW = 249
NET_FLUX = 250
ENC_OFFSET_L = 251
ENC_OFFSET_R = 252
MIN_CH_PILOT = 253
DIFF = 254
MIN_CH_EL_STA = 255
CULV_AREA_DS = 256
CULV_AREA_US = 257
GATE_WEIR_COEF = 258
WEIR_COEF = 259
Q_BREACH = 260
BREACH_AVG_VELOCITY = 261
BREACH_FLOW_AREA = 262
LEFT_STATION = 263
RIGHT_STATION = 264
LEVEE_STA_LEFT = 265
LEVEE_STA_RIGHT = 266
Q_INLINE_RC = 267
Q_OUTLET_TS = 268


def print_help(sort_alpha=False):
    """Print a table of all the available variable names.

    Parameters
    ----------
    sort_alpha : bool, optional
        True to order output table aphabetically.
    """
    current_module = sys.modules[__name__]
    doc = current_module.__doc__

    if sort_alpha:
        break_ = '-'*79
        start_table = doc.split('\n').index(break_) + 3
        content = doc.split('\n')[start_table:-1]
        last = ['  ---']
        content += last*2

        names = []
        dic = {}  # varname, lines
        i = 0
        while True:
            line = content[i]
            name = line[2:].split(' ')[0]
            line_next = content[i+1]
            line_next_next = content[i+2]

            if line_next[2] != ' ':
                i += 1
                lines = [line]
            elif line_next[2] == ' ' and line_next_next[2] != ' ':
                i += 2
                lines = [line, line_next]
            elif line_next[2] == ' ' and line_next_next[2] == ' ':
                i += 3
                lines = [line, line_next, line_next_next]

            dic[name] = lines
            names.append(name)

            if i >= len(content) - 2:
                break

        names = sorted(names)
        content = doc.split('\n')[:start_table]
        for name in names:
            content += dic[name]
        print('\n' .join(content))
    else:
        print(doc)


if __name__ == '__main__':
    print_help()
    print_help(sort_alpha=True)
