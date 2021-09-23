import datetime
import random
import copy
import os
from room import Room, MONTHS, DAYS_PER_MONTH
from reservation import Reservation

class Hotel:

    def __init__(self, name, rooms=[], reservations={}):
        self.name = name
        self.rooms = copy.deepcopy(rooms)
        self.reservations = copy.deepcopy(reservations)

    def make_reservation(self, client_name, room_type, check_in, check_out):
        room = Room.find_available_room(self.rooms, room_type, check_in, check_out)
        if room:
            temp_reserv = Reservation(client_name,room,check_in,check_out)
            self.reservations[temp_reserv.booking_number] = temp_reserv
            return temp_reserv.booking_number
        raise AssertionError("No room of the given type is available")

    def get_receipt(self,booking_numbers):
        result = 0
        for element in booking_numbers:
            if element in self.reservations:
                reservation = self.reservations[element]
                result += reservation.room_reserved.price*(reservation.check_out-reservation.check_in).days
        return float(result)

    def get_reservation_for_booking_number(self, booking_number):
        if booking_number in self.reservations:
            return self.reservations[booking_number]
        return None

    def cancel_reservation(self, booking_number):
        if booking_number in self.reservations:
            temp_date = self.reservations[booking_number].check_in
            delta = datetime.timedelta(days=1)
            while temp_date < self.reservations[booking_number].check_out:
                self.reservations[booking_number].room_reserved.make_available(temp_date)
                temp_date += delta
            self.reservations.pop(booking_number)

    def get_available_room_types(self):
        result = []
        types = list([room.room_type for room in self.rooms])
        for key in self.reservations:
                    types.remove(self.reservations[key].room_reserved.room_type)
        for type in types:
            if not type in result:
                result.append(type)
        return result

    @staticmethod
    def load_hotel_info_file(path):
        f = open(path, 'r')
        temp_list = f.read().split("\n")
        hotel_name = temp_list[0]

        result = []
        for element in temp_list[1:len(temp_list)-1]:
            data = element[5:].split(',')
            result.append(Room(data[1], int(data[0]), float(data[2])))
        f.close()
        return hotel_name, result

    def save_hotel_info_file(self):
        directory = ''
        for char in self.name:
            if char == ' ':
                directory += '_'
            else:
                directory += char.lower()
        if not os.path.exists("hotels/"+directory):
            os.mkdir("hotels/"+directory)
        f = open("hotels/"+directory+"/hotel_info.txt", 'w')
        f.write(self.name + '\n')


        for room in self.rooms:
            f.write(str(room)+ '\n')
        f.close()

    @staticmethod
    def load_reservation_strings_for_month(folder_name, month, year):
        f = open("hotels/" + folder_name + "/" + str(year) + "_" + str(month) + ".csv")
        result = {}
        temp_list = f.read().split('\n')
        for element in temp_list[:len(temp_list)-1]:
            single_list = element.split(',')
            values = []
            for i in range(1,len(single_list)):
                values.append((year, month, i, single_list[i]))
            result[int(single_list[0])] = values[:]
        f.close()
        return result

    def save_reservations_for_month(self, month, year):
        directory = ''
        for char in self.name:
            if char == ' ':
                directory += '_'
            else:
                directory += char.lower()
        if not os.path.exists("hotels/" + directory):
            os.mkdir("hotels/" + directory)
        f = open("hotels/" + directory + "/" + str(year) + "_" + str(month) + ".csv", 'w')

        data = [[None for i in range(DAYS_PER_MONTH[MONTHS.index(month)])] for j in range(len(self.rooms))]

        for i in range(len(self.rooms)):
            temp_dict = self.rooms[i].availability

            if (year, MONTHS.index(month)+1) in temp_dict:

                for j in range(1,len(temp_dict[(year, MONTHS.index(month)+1)])):
                    if not temp_dict[(year, MONTHS.index(month)+1)][j]:

                        for number in self.reservations:
                            day = datetime.date(year, MONTHS.index(month)+1, j)
                            if self.reservations[number].check_in <= day < self.reservations[number].check_out and self.reservations[number].room_reserved == self.rooms[i]:
                                print('ok')
                                data[i][j-1] = self.reservations[number].to_short_string()
        for i in range(len(data)):
            f.write(str(self.rooms[i].room_num) + ',')
            for j in range(len(data[i])):
                if data[i][j] is None:
                    f.write(',')
                elif j != len(data[i])-1:
                    f.write(data[i][j] + ',')
                else:
                    f.write(data[i][j])
            f.write('\n')
        f.close()

    def save_hotel(self):
        self.save_hotel_info_file()
        if len(self.rooms) != 0:
            min_year = self.reservations[list(self.reservations.keys())[0]].check_in.year
            max_year = self.reservations[list(self.reservations.keys())[0]].check_in.year
            for key in self.reservations:
                if self.reservations[key].check_in.year < min_year:
                    min_year = self.reservations[key].check_in.year
                if self.reservations[key].check_in.year > max_year:
                    max_year = self.reservations[key].check_in.year
            for year in range(min_year,max_year+1):
                for month in range(12):
                    self.save_reservations_for_month(MONTHS[month], year)

    @classmethod
    def load_hotel(cls, folder_name):
        temp_hotel = Hotel('temp')
        hotel_name, hotel_room = temp_hotel.load_hotel_info_file("hotels/" + folder_name + "/hotel_info.txt")
        file_years = []
        result = {}
        for file in os.listdir('hotels/' + folder_name):
            if len(file) > 4 and file[len(file) - 4:] == ".csv" and not int(file[:4]) in file_years:
                file_years.append(int(file[:4]))

        temp_list = [[] for i in range(len(hotel_room))]
        temp_dict = {}
        for year in file_years:
            for month in range(12):
                temp_dict[month] = Hotel.load_reservation_strings_for_month(folder_name, MONTHS[month], year)
        for year in file_years:
            for month in range(12):
                for room in hotel_room:
                    room.set_up_room_availability(MONTHS, year)
                    temp_list[room.room_num - 1].extend(temp_dict[month][room.room_num])

        for room in hotel_room:
            tmp_L = [e for e in temp_list[room.room_num - 1] if e[3] != ""]
            tmp_L2 = []
            tmp_L3 = []
            for i in range(len(tmp_L)):
                if not tmp_L[i][3] in tmp_L3:
                    tmp_L2.append(tmp_L[i])
                    tmp_L3.append(tmp_L[i][3])
                    for j in range(1, len(tmp_L) + 1):
                        if tmp_L[len(tmp_L) - j][3] == tmp_L[i][3]:
                            tmp_L2.append(tmp_L[len(tmp_L) - j])
                            break
                else:
                    continue
            tmp = Reservation.get_reservations_from_row(room, tmp_L2)
            for key in tmp:
                result[key] = tmp[key]

        return cls(hotel_name, hotel_room, result)





















if __name__ == '__main__':
    random.seed(137)
    Reservation.booking_numbers = []
    hotel = Hotel.load_hotel('overlook_hotel')
    print(hotel.name)

    print(str(hotel.rooms[236]))

    print(hotel.reservations[9998701091820])


