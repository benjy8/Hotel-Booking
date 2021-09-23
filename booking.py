import datetime
import random
import matplotlib
import os
from hotel import Hotel


class Booking:

    def __init__(self, hotels):
        self.hotels = hotels[:]


    @classmethod
    def load_system(cls):
        temp_list = []
        for folder_name in os.listdir("hotels/"):
            temp_list.append(Hotel.load_hotel(folder_name))
        return cls(temp_list)






    def menu(self):
        print("Welcome to Booking System")
        print("What would you like to do?")
        print("1 Make a reservation")
        print("2 Cancel a reservation")
        print("3 Look up a reservation")
        choice = input()
        if choice == str(1):
            self.create_reservation()
        elif choice == str(2):
            self.cancel_reservation()
        elif choice == "xyzzy":
            self.delete_reservations_at_random()

        else:
            self.lookup_reservation()

        for hotel in self.hotels:
            hotel.save_hotel()


    def create_reservation(self):
        name = input("Please enter your name: ")
        print("Hi " + name + "! Which hotel would you like to book?")

        for i in range(len(self.hotels)):
            print(str(i + 1) + " " + self.hotels[i].name)

        choice1 = input()

        for i in range(len(self.hotels[choice1-1].get_available_room_types())):
            print(str(i+1)+ " " + self.hotels[choice1-1].get_available_room_types()[i] )

        choice2 = input()

        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date (YYYY-MM-DD): ")

        print("Ok. Making your reservation for a " + self.hotels[choice1-1].get_available_room_types()[choice2-1])

        temp_room = Room.find_available_room(self.hotels[choice1-1].rooms, self.hotels[choice1-1].get_available_room_types()[choice2-1],
                                             datetime.strptime(check_in, '%y-%m-%d'), datetime.strptime(check_out, '%y-%m-%d'))




    def cancel_reservation(self):
        book_number = input("Please enter your booking number: ")
        check = False
        for hotel in self.hotels:
            if book_number in hotel.reservations:
                Hotel.cancel_reservation(book_number)
                print("Cancelled succesfully")
                check = True
        if not check:
            print("Could not find a reservation with that booking number")




    def lookup_reservation(self):
        first_question = input("Do you have your booking number(s)? ")
        if first_question == "yes" :
            booking_number = input("Please enter a booking number (or 'end'): ")
            if not (type(booking_number) == int and len(str(booking_number)) == 13) or not str(booking_number)[0] != '0':
                print("Invalid input")
            if  (type(booking_number) == int and len(str(booking_number)) == 13) or  str(booking_number)[0] != '0':
                for hotel in self.hotels:
                    if booking_number in hotel.reservations:
                        print("Reservation found at hotel " + hotel.name + ":")
                        print(hotel.reservations[booking_number])
        elif first_question == "no":
            name = input("Please enter your name:")
            hotel_name = input("Please enter the hotel you are booked at:")
            room_number = input("Enter the reserved room number:")
            check_in = input("Enter the check-in date (YYYY-MM-DD:")
            check_out = input("Enter the check-out date (YYYY-MM-DD:")

            room = Room.find_available_room(hotel)


    def delete_reservations_at_random(self):
        print("You said the magic word!")
        choice = random.randint(0,len(self.hotels)-1)
        self.hotels[choice].reservations = {}






if __name__ == '__main__':
    system = Booking.load_system()
    len(system.hotels)



