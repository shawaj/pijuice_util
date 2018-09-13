#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

def configDict(config):
    rv = {}

    # TODO: should we camelCase here
    rv['charging_config'] = config.GetChargingConfig()
    rv['battery_profile'] = config.GetBatteryProfile()
    rv['firmware_version'] = config.GetFirmwareVersion()
    return rv

if __name__ == '__main__':
    import pijuice
    import argparse, logging

    parser = argparse.ArgumentParser(description='Command line utility for a PiJiuce')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--enable-wakeup', action='store_true', help='enable the wakeup flag')
    g.add_argument('--get-time', action='store_true', help='print the RTC time')
    g.add_argument('--get-alarm', action='store_true', help='print the RTC alarm')
    g.add_argument('--get-status', action='store_true', help='print the pijiuce config')
    g.add_argument('--get-config', action='store_true', help='print the pijiuce status')

    parser.add_argument('--verbose', action='count', help='crank up logging')

    args = parser.parse_args()

    logging.basicConfig (level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    pj = pijuice.PiJuice(1, 0x14)

    if args.enable_wakeup:
        rtc = pj.rtcAlarm
        ctr = rtc.GetControlStatus()
        logging.debug ('control status before %s', str(ctr))

        logging.debug ('disabling wakeup')
        rtc.SetWakeupEnabled(False)

        ctr = rtc.GetControlStatus()
        logging.debug ('control status after disable %s', str(ctr))

        logging.debug ('enabling wakeup')
        rtc.SetWakeupEnabled(True)
        logging.debug ('wakeup enabled')

        ctr = rtc.GetControlStatus()
        print str(ctr)
        logging.info ('control status is now %s', str(ctr))

    if args.get_time:
        rtc = pj.rtcAlarm
        t = rtc.GetTime()
        print str(t)

    if args.get_alarm:
        rtc = pj.rtcAlarm
        t = rtc.GetAlarm()
        print str(t)

    if args.get_status:
        s = pj.status
        print repr(s)
        print str(s)
        print s.__dict__

    if args.get_config:
        s = pj.config
        print configDict(s)

