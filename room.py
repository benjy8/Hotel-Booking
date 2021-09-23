import datetime


'''
room.py
Boris Agossou

'''
# declare constants
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
DAYS_PER_MONTH = [31,28,31,30,31,30,31,31,30,31,30,31]

#class Room
class Room:
    #class attributes
    TYPES_OF_ROOM_AVAILABLE = ['twin','double','queen','king']
    #instance attributes
    def __init__(self, rType, rNum, rPricePerNight):
        # check if the room is available
        if rType.lower() in (rT.lower() for rT in Room.TYPES_OF_ROOM_AVAILABLE):
            self.room_type = rType
        else:
            raise AssertionError("Room type not available")
        # check if the room number is positive
        if rNum  > 0:
            self.room_num = rNum
        else:
            raise AssertionError("Room number should be positive")
        # check if the room price is positive
        if rPricePerNight  > 0:
            self.price = rPricePerNight
        else:
            raise AssertionError("Price should be positive")
        # initialize the empty dictionary
        self.availability = {}

    # string representation of room
    def __str__(self):
        return "Room " +str(self.room_num) + "," +self.room_type +"," +str(self.price)


    '''
    :param input list of string representing months
    :param an integer representing the year
    updates the availability of room
    '''
    def set_up_room_availability(self, monthList, yearInt):
        isleap = False
        if (yearInt % 4) == 0:
            if (yearInt % 100) == 0:
                if (yearInt % 400) == 0:
                    isleap = True
                else:
                    isleap = False
            else: # if the year is divisible 400
                isleap = True
        else:
            isleap = False
        # loop through all the given months
        for month in monthList:
            # find the index of month in the MONTHS array
            monthIndex = MONTHS.index(month)
            # create tuple of integers
            monthTuple = (yearInt, monthIndex+1)
            # create a empty list to hold booleans
            days = []
            # first element is None
            days.append(None)
            numDays = DAYS_PER_MONTH[monthIndex]
            # if year is leap year, feb should have 29 days
            if monthIndex == 1 and isleap:
                numDays = 29
            # loop through the number of days
            for day in range(numDays):
                days.append(True)

            # update the availability dictionary
            self.availability[monthTuple] = days
    
    def reserve_room(self, reserveDate):
        if not self.availability[(reserveDate.year, reserveDate.month)][reserveDate.day]:
            raise AssertionError("The room is not available at the given date")
        self.availability[(reserveDate.year, reserveDate.month)][reserveDate.day] = False
    
    def make_available(self, reserveDate):
        self.availability[(reserveDate.year, reserveDate.month)][reserveDate.day] = True
        
    def is_available(self, checkIn, checkOut):
        if checkIn > checkOut:
            raise AssertionError("Check-out date is earlier than check-ins")
        for year in range(checkIn.year, checkOut.year+1):
            if checkIn.month <= checkOut.month:
                for month in range(checkIn.month, checkOut.month+1):
                    for day in range(1, DAYS_PER_MONTH[month-1]):
                        if month == checkIn.month and day >= checkIn.day and not self.availability[(year,month)][day]:
                            return False
                        if month == checkOut.month and day < checkOut.day and not self.availability[(year,month)][day]:
                            return False
                        if month != checkIn.month and month != checkOut.month and not self.availability[(year,month)][day]:                       
                            return False
            else:
                if year == checkIn.year:
                    months = list(range(checkIn.month,13))
                elif year == checkOut.year:
                    months = list(range(1,checkOut.month+1))
                else:
                    months = range(13)
                for month in months:
                    for day in range(1,DAYS_PER_MONTH[month-1]):
                        if month == checkIn.month and day >= checkIn.day and not self.availability[(year,month)][day]:
                            return False
                        if month == checkOut.month and day < checkOut.day and not self.availability[(year,month)][day]:
                            return False
                        if month != checkIn.month and month != checkOut.month and not self.availability[(year,month)][day]:
                            return False
        return True
    
    @staticmethod
    def find_available_room(rooms, roomType, checkIn, checkOut):
        
        if checkIn > checkOut:
            raise AssertionError("Check-out date is earlier than check-ins")
        temp_rooms = [room for room in rooms if room.room_type == roomType]
        for room in temp_rooms:
            if room.is_available(checkIn, checkOut):
                return room
        return None
        
                            


if __name__ == '__main__':
    r = Room("Queen", 105, 80.0)
    r.set_up_room_availability(['Jan', 'Dec'], 2019)
    print(len(r.availability))

    print(len(r.availability[(2019, 11)]))
    print(r.availability[(2019, 11)][5])
