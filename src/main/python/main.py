#THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
#IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS.

from src.main.python.UC3MTravel import HotelManager
from HotelManagementException import HotelManagementException


def main():
    mng = HotelManager()
    res = mng.ReaddatafromJSOn("test.json")
    strRes = res.__str__()
    print(strRes)
    print("CreditCard: " + res.CREDITCARD)
    print(res.LOCALIZER)

if __name__ == "__main__":
    main()
