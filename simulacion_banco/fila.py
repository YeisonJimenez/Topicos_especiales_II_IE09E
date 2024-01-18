"""
This program simulates a bank queue.

Yeison S Jimenez Mejia
Electrical Engineering
Specials topics II
Universidad Tecnologica de Pereira- UTP
"""


class Row:
    """"
    This class depict a bank row
    """

    def __init__(self, max_row):
        """
        This function initializes the class
        :param max_row: maximum elements contains in row
        """
        self.the_row = list()  # empty list
        self.counter = 0  # people counter
        self.max_row = max_row  # maximum limit

    def enter(self, element):
        """
        This method is to enter elements to the row

        :param element: Is a object that row enter the_row
        :return: None
        """
        if self.max_row > self.size():
            # Add element to end of row
            self.the_row.append(element)
            # Counter update
            self.counter += 1

    def exit(self):
        """
        Method for get out an element from row
        :return: an object that leave of row
        """
        if self.the_row.__len__() >= 1:
            object = self.the_row.pop(0)
        # else:
        #     raise IndexError('The row is empty!')
        else:
            object = None
        return object

    def size(self):
        """
        This method show the amount of elements from row
        :return: The amount of elements from row
        """
        return len(self.the_row)  # Size of queue

    def restart(self):
        """
        This method to restart the row
        :return: None
        """
        self.counter = 0
        self.the_row = list()

    def obj_leave(self):
        """
        This method to returns the object  leaves the row
        :return: first element from the row
        """
        return self.the_row[0]

    def empty_row(self):
        """
        This method returns if the row is empty
        :return: Boolean. True if the row ist empty
        """
        return self.the_row.__len__() < 1


# Safeguard
if __name__ == '__main__':
    # unit tests:
    my_row = Row(3)  # max_row = 3
    # add something names to the row:
    my_row.enter("Brayan")
    my_row.enter("Byron")
    my_row.enter("Daniel")
    my_row.enter("Diego")
    my_row.enter("Hamilton")
    print(my_row.the_row)

    print(my_row.size())
    print(my_row.obj_leave())
    print('Is empty the row?: ', my_row.empty_row())
    print('The object that is exiting is: ', my_row.exit())
