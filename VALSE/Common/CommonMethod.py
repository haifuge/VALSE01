def Second2Time(second):
    hour=int(second/3600)
    minute=int((second-hour*3600)/60)
    sec=second%60
    return str(hour)+':'+str(minute)+':'+str(int(sec))


