import hashlib
import json



class HotelReservation:
    def __init__(self, creditcardNumb, nAMeAndSURNAME, IDCARD, phonenumber, room_type, arrival_date, num_days):
        self.__crEDITcardnumber = creditcardNumb
        self.__NAME_SURNAME = nAMeAndSURNAME
        self.__idcard = IDCARD
        self.__phonenumber = phonenumber
        self.__roomtype = room_type
        self.__ARRIVAL = arrival_date
        self.__num_days = num_days

    def __str__(self):
        json_info = {
            "credit_card": self.__crEDITcardnumber,
            "name_surname": self.__NAME_SURNAME,
            "id_card": self.__idcard,
            "phone_number": self.__phonenumber,
            "room_type": self.__roomtype,
            "arrival_date": self.__ARRIVAL,
            "num_days": self.__num_days,
        }
        return json.dumps(json_info)

    @property
    def LOCALIZER(self):
        return hashlib.md5(self.__str__().encode()).hexdigest()
