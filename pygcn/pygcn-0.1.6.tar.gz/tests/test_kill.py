import threading
import gcn
import gcn.voeventclient
import gcn.handlers
import socket
import time

# Set up logger
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

payloads = ['''<?xml version = '1.0' encoding = 'UTF-8'?>
<voe:VOEvent
      ivorn="ivo://nasa.gsfc.gcn/Fermi#GBM_Flt_Pos_2011-09-04T03:54:36.02_336801278_45-956"
      role="observation" version="1.1"
      xmlns:voe="http://www.ivoa.net/xml/VOEvent/v1.1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v1.1 http://www.ivoa.net/xml/VOEvent/VOEvent-v1.1.xsd" >
  <Who>
    <AuthorIVORN>ivo://nasa.gsfc.tan/gcn</AuthorIVORN>
    <Author>
      <shortName>Fermi (via VO-GCN)</shortName>
      <contactName>Julie Mcenery</contactName>
      <contactPhone>+1-301-286-1632</contactPhone>
      <contactEmail>Julie.E.McEnery@nasa.gov</contactEmail>
    </Author>
    <Date>2011-09-04T03:54:51</Date>
    <Description>This VOEvent message was created with GCN VOE version: 1.4 04jun11</Description>
  </Who>
  <What>
    <Param name="Packet_Type"    value="111" />
    <Param name="Pkt_Ser_Num"    value="10" />
    <Param name="TrigID"         value="336801278" ucd="meta.id" />
    <Param name="Sequence_Num"   value="45" ucd="meta.id.part" />
    <Param name="Burst_TJD"      value="15808" unit="days" ucd="time" />
    <Param name="Burst_SOD"      value="14076.02" unit="sec" ucd="time" />
    <Param name="Burst_Inten"    value="117" unit="cts" ucd="phot.count" />
    <Param name="Trig_Timescale" value="8.192" unit="sec" ucd="time.interval" />
    <Param name="Data_Timescale" value="8.192" unit="sec" ucd="time.interval" />
    <Param name="Data_Signif"    value="8.00" unit="sigma" ucd="stat.snr" />
    <Param name="Phi"            value="55.00" unit="deg" ucd="pos.az.azi" />
    <Param name="Theta"          value="65.00" unit="deg" ucd="pos.az.zd" />
    <Param name="SC_Long"        value="115.18" unit="deg" ucd="pos.earth.lon" />
    <Param name="SC_Lat"         value="0.00" unit="deg" ucd="pos.earth.lat" />
    <Param name="Algorithm"             value="3" unit="dn" />
    <Param name="Most_Likely_Index"     value="4" unit="dn" />
    <Param name="Most_Likely_Prob"      value="93" />
    <Param name="Sec_Most_Likely_Index" value="8" unit="dn" />
    <Param name="Sec_Most_Likely_Prob"  value="5" />
    <Param name="Hardness_Ratio"        value="1.39" ucd="arith.ratio" />
    <Param name="Trigger_ID"            value="0x0" />
    <Param name="Misc_flags"            value="0x1000000" />
    <Group name="Trigger_ID" >
      <Param name="Def_NOT_a_GRB"         value="false" />
      <Param name="Target_in_Blk_Catalog" value="false" />
      <Param name="Spatial_Prox_Match"    value="false" />
      <Param name="Temporal_Prox_Match"   value="false" />
      <Param name="Test_Submission"       value="false" />
    </Group>
    <Group name="Misc_Flags" >
      <Param name="Values_Out_of_Range"   value="false" />
      <Param name="Delayed_Transmission"  value="true" />
      <Param name="Flt_Generated"         value="true" />
      <Param name="Gnd_Generated"         value="false" />
    </Group>
    <Param name="Coords_Type"   value="1" unit="dn" />
    <Param name="Coords_String" value="source_object" />
    <Group name="Obs_Support_Info" >
      <Description>The Sun and Moon values are valid at the time the VOEvent XML message was created.</Description>
      <Param name="Sun_RA"        value="162.74" unit="deg" ucd="pos.eq.ra" />
      <Param name="Sun_Dec"       value="7.33" unit="deg" ucd="pos.eq.dec" />
      <Param name="Sun_Distance"  value="48.74" unit="deg" ucd="pos.angDistance" />
      <Param name="Sun_Hr_Angle"  value="-2.03" unit="hr" />
      <Param name="Moon_RA"       value="241.71" unit="deg" ucd="pos.eq.ra" />
      <Param name="Moon_Dec"      value="-22.42" unit="deg" ucd="pos.eq.dec" />
      <Param name="MOON_Distance" value="43.86" unit="deg" ucd="pos.angDistance" />
      <Param name="Moon_Illum"    value="43.70" unit="%" ucd="arith.ratio" />
      <Param name="Galactic_Long" value="303.07" unit="deg" ucd="pos.galactic.lon" />
      <Param name="Galactic_Lat"  value="31.12" unit="deg" ucd="pos.galactic.lat" />
      <Param name="Ecliptic_Long" value="204.91" unit="deg" ucd="pos.ecliptic.lon" />
      <Param name="Ecliptic_Lat"  value="-24.00" unit="deg" ucd="pos.ecliptic.lat" />
    </Group>
    <Description>The Fermi-GBM location of a transient.</Description>
  </What>
  <WhereWhen>
    <ObsDataLocation xmlns="http://www.ivoa.net/xml/STC/stc-v1.30.xsd">
      <ObservatoryLocation xlink:href="ivo://STClib/Observatories#GEOLUN/" xlink:type="simple" id="GEOLUN" />
      <ObservationLocation>
        <AstroCoordSystem xlink:href="ivo://STClib/CoordSys#UTC-FK5-GEO/" xlink:type="simple" id="FK5-UTC-GEO" />
        <AstroCoords coord_system_id="FK5-UTC-GEO">
          <Time unit="s">
            <TimeInstant>
              <ISOTime>2011-09-04T03:54:36.02</ISOTime>
            </TimeInstant>
          </Time>
          <Position2D unit="deg">
            <Name1>RA</Name1>
            <Name2>Dec</Name2>
            <Value2>
              <C1 pos_unit="deg">193.0000</C1>
              <C2 pos_unit="deg">-31.7500</C2>
            </Value2>
            <Error2Radius>17.4333</Error2Radius>
          </Position2D>
        </AstroCoords>
      </ObservationLocation>
    </ObsDataLocation>
  <Description>The RA,Dec coordinates are of the type: source_object.</Description>
  </WhereWhen>
  <How>
    <Description>Fermi Satellite, GBM Instrument</Description>
    <Reference uri="http://gcn.gsfc.nasa.gov/fermi.html" type="url" />
  </How>
  <Why importance="0.5">
    <Inference probability="0.5">
      <Concept>process.variation.burst;em.gamma</Concept>
    </Inference>
  </Why>
  <Citations>
    <EventIVORN cite="followup">ivo://nasa.gsfc.gcn/Fermi#GBM_Alert_2011-09-04T03:54:36.02_336801278_1-954</EventIVORN>
    <Description>This is an updated position to the original trigger.</Description> 
  </Citations>
  <Description>
  </Description>
</voe:VOEvent>
'''.encode('UTF-8'),
'''<?xml version = '1.0' encoding = 'UTF-8'?>
<voe:VOEvent
      ivorn="ivo://nasa.gsfc.gcn/gcn"
      role="observation" version="1.1"
      xmlns:voe="http://www.ivoa.net/xml/VOEvent/v1.1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      xsi:schemaLocation="http://www.ivoa.net/xml/VOEvent/v1.1 http://www.ivoa.net/xml/VOEvent/VOEvent-v1.1.xsd" >
  <What>
    <Param name="Packet_Type" value="4" />
  </What>
</voe:VOEvent>
'''.encode('UTF-8')]


def serve(payloads, host='127.0.0.1', port=8099, retransmit_timeout=0, log=None):
    """Rudimentary GCN server, for testing purposes. Serves just one connection
    at a time, and repeats the same payloads in order, repeating, for each
    connection."""
    if log is None:
        log = logging.getLogger('gcn.serve')

    sock = socket.socket()
    try:
        sock.bind((host, port))
        log.info("bound to %s:%d", host, port)
        sock.listen(0)
        for i in range(5):
            conn, addr = sock.accept()
            log.info("connected to %s:%d", addr, port)
            try:
                for payload in payloads:
                    time.sleep(retransmit_timeout)
                    gcn.voeventclient._send_packet(conn, payload)
            except socket.error:
                log.exception('error communicating with peer')
            finally:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except socket.error:
                    log.exception("could not shut down socket")

                try:
                    conn.close()
                except socket.error:
                    log.exception("could not close socket")
                else:
                    log.info("closed socket")
    finally:
        sock.close()

class MessageCounter(object):
    def __init__(self):
        self.count = 0
    def __call__(self, *args):
        self.count += 1

def test_reconnect_after_kill():
    """Test that the client recovers if the server closes the connection."""
    server_thread = threading.Thread(
        group=None, target=serve, args=(payloads,), kwargs=dict(retransmit_timeout=0.1))
    server_thread.daemon = True
    server_thread.start()

    handler = MessageCounter()

    client_thread = threading.Thread(
        group=None, target=gcn.listen,
        kwargs=dict(host='127.0.0.1', max_reconnect_timeout=4,
            handler=gcn.handlers.include_notice_types(111)(handler)))
    client_thread.daemon = True
    client_thread.start()

    time.sleep(5)
    assert handler.count == 5
