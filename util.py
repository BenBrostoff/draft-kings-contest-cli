def time_conversion(td):
    seconds = td.seconds
    micro = td.microseconds
    ms = micro / 1000
    rem = ms / 1000
    return seconds + rem