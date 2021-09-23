import random
import datetime
from room import Room, MONTHS, DAYS_PER_MONTH


class Reservation:
    booking_numbers = []

    def __init__(self, name, room_reserved, check_in, check_out, booking_number=None):
        if not room_reserved.is_available(check_in, check_out):
            raise AssertionError("Input room is not available at the specified dates")

        self.name = name
        self.room_reserved = room_reserved
        self.check_in = check_in
        self.check_out = check_out

        if (type(booking_number) == int and len(str(booking_number)) == 13) and str(booking_number)[0] != '0':
            if booking_number in Reservation.booking_numbers:
                raise AssertionError("Booking number had already been used")

        elif booking_number is None:
            booking_number = random.randint(1000000000000, 9999999999999)
            while booking_number in Reservation.booking_numbers:
                booking_number = random.randint(1000000000000, 9999999999999)
        else:
            raise AssertionError("Booking number is not a valid 13 digit number")
        self.booking_number = booking_number
        Reservation.booking_numbers.append(self.booking_number)

        temp_date = check_in
        delta = datetime.timedelta(days=1)
        while temp_date < check_out:
            room_reserved.reserve_room(temp_date)
            temp_date += delta

    def __str__(self):
        return "Booking number: " + str(self.booking_number) + "\nName: " + str(self.name) +"\nRoom reserved: " + str(self.room_reserved) +\
        "\nCheck-in date: " +  str(self.check_in) + "\nCheck-out date: " + str(self.check_out)

    def to_short_string(self):
        return "" + str(self.booking_number) +"--"+str(self.name)

    @classmethod
    def from_short_string(cls, details_string, check_in, check_out, room):
        booking_number, client_name = details_string.split('--')
        booking_number = int(booking_number)
        return cls(client_name,room,check_in,check_out,booking_number)

    @staticmethod
    def get_reservations_from_row(room, tuple_list):
        result = {}
        for i in range(len(tuple_list)):
            if len(tuple_list[i][3]) > 0:
                booking_number, client_name = tuple_list[i][3].split("--")
                booking_number = int(booking_number)
                date1 = datetime.date(tuple_list[i][0], MONTHS.index(tuple_list[i][1])+1, tuple_list[i][2])
                for j in range(i+1, len(tuple_list)):
                    if tuple_list[j][3].split("--")[0] == str(booking_number):
                        date2 = datetime.date(tuple_list[j][0], MONTHS.index(tuple_list[j][1]) + 1, tuple_list[j][2])
                        if date1 < date2:
                            temp_date2 = date2 + datetime.timedelta(days=1)
                            result[booking_number] = Reservation(client_name, room, date1, temp_date2, booking_number)
                        else:
                            temp_date1 = date1 + datetime.timedelta(days=1)
                            result[booking_number] = Reservation(client_name, room, date2, temp_date1, booking_number)

        return result









if __name__ == '__main__':
    random.seed(987)
    Reservation.booking_numbers = []
    r1 = Room("Queen", 105, 80.0)
    r1.set_up_room_availability(MONTHS, 2021)
    rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
    rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
    print(rsv_dict[1953400675629])
