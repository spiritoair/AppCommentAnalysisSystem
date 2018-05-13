from time import strftime, localtime
from datetime import timedelta, date
import calendar


year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())

def today():
    '''''
    get today,date format="YYYY-MM-DD"
    '''''
    return date.today()

def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)

def get_days_of_month(year, mon):
    '''''
    get days of month
    '''
    return calendar.monthrange(int(year), int(mon))[1]

def getyearandmonth(n=0):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon + n
    if (n >= 0):
        if (totalmon <= 12):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(int(thisyear), j))
            j = addzero(j)
            return (str(thisyear), str(j), days)
    else:
        if ((totalmon > 0) and (totalmon < 12)):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)

def get_today_month(n=0):
    '''''
    获取当前日期前后N月的日期
    if n>0, 获取当前日期前N月的日期
    if n<0, 获取当前日期后N月的日期
    date format = "YYYY-MM-DD"
    '''
    (y, m, d) = getyearandmonth(n)
    arr = (y, m, d)
    if (int(day) < int(d)):
        arr = (y, m, day)
    return "-".join("%s" % i for i in arr)

def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if (nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs