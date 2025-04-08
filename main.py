import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id":str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card-security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Changes the availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thanks for your reservation!
        Your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        """
        return content

class SpaReservation:
    def __init__(self, customer_name, hotel_object, spa_question):
        self.customer_name = customer_name
        self.hotel = hotel_object
        self.spa_question = spa_question

    def generate(self):
        if spa_question == "yes":
            content = f"""
            Thanks for your SPA reservation!
            Here your SPA booking data:
            Name: {self.customer_name}
            Hotel: {self.hotel.name}
            """
            return content
        else:
            print("Thank you anyway!")


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True

class SecurityCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecurityCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate("mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa_question = input("Would you like to book a SPA reservation? (yes/no):").strip()
            spa = SpaReservation(customer_name=name, hotel_object=hotel, spa_question=spa_question)
            print(spa.generate())
        else:
            print("Invalid credentials")
    else:
        print("Invalid credit card number")
else:
    print("The hotel is not available")