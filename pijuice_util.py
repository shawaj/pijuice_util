#!/usr/bin/env python

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

if __name__ == '__main__':
    import pijuice
    import argparse, logging

    parser = argparse.ArgumentParser(description='Command line utility for a PiJiuce')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--enable-wakeup', action='store_true', help='enable the wakeup flag')

    parser.add_argument('--verbose', action='count', help='crank up logging')

    args = parser.parse_args()

    logging.basicConfig (level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    if args.verbose > 0:
        logging.getLogger().setLevel(logging.DEBUG)

    pj = pijuice.PiJuice(1, 0x14)
    rtc = pj.rtcAlarm

    if args.enable_wakeup:
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
