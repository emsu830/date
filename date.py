# Author: Emily Su
# Last Revised: February 2022

class Date:
    '''The Date class constructs a date object and defines methods and operators for the date object.'''
    month_dict = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    
    @staticmethod
    def is_leap_year(year):
        '''Returns True if the year is a leap year; False if the year is not a leap year.'''
        return (year%4 == 0 and year%100 != 0) or year%400 == 0
    
    @staticmethod
    def days_in(year,month):
        '''Dictionary determining how many days are in a designated month - accounting for leap years.'''
        return Date.month_dict[month] + (1 if month == 2 and Date.is_leap_year(year) else 0)
    
    
    def __init__(self, year: int, month: int, day: int):
        '''Initializes a date object for a valid year (>= 0), month (between inclusive 1 - 12), and day (between inclusive 1 and the last day of the month).
        Parameters:
        year (int): year of date object
        month (int): month of date object
        day (int): day of date object
        '''
        assert type(year) is int and year >= 0, 'Date.__init__: invalid year (' + str(year) + '); must be type of int greater than or equal to 0'
        assert type(month) is int and 1 <= month <= 12, 'Date.__init__: invalid month (' + str(month) + '); must be type of int between inclusive range 1 to 12'
        assert type(day) is int and 1 <= day <= self.days_in(year, month), 'Date.__init__: invalid day (' + str(day) + '); must be type of int between inclusive range 1 to ' + str(self.days_in(year,month))
        
        self.year = year
        self.month = month
        self.day = day


    def __getitem__(self, index):
        '''Index operator to return the Date object's year, month, or day, or a tuple of these attributes.
        Parameter:
        index (str or tuple of strs): string of 'y', 'm', or 'd' or a tuple of these strings'''
        if type(index) is str and index.lower() in ['y', 'm','d']:
            if index.lower() == 'y':
                return self.year
            elif index.lower() == 'm':
                return self.month
            elif index.lower() == 'd':
                return self.day
        elif type(index) is tuple:
            temp = []
            for i in index:
                if i.lower() == 'y':
                    temp.append(self.year)
                elif i.lower() == 'm':
                    temp.append(self.month)
                elif i.lower() == 'd':
                    temp.append(self.day)
            return tuple(temp)
        else:
            raise IndexError('Date.__getitem__: invalid index (' + str(index) +"); must be a str of 'y', 'm', or 'd' or a tuple of these strings")

    
    def __repr__(self):
        '''Returns a printable representational string of a date.
        String format example: Date(2020, 1, 1)'''
        return 'Date(' + ','.join((str(self.year), str(self.month), str(self.day))) + ')'
    
    
    def __str__(self):
        '''Returns a string of date in the format month/day/year.'''
        return '/'.join((str(self.month), str(self.day), str(self.year)))
    
    
    def __len__(self):
        '''Returns the number of days elapsed from January 1, 0000.'''
        days_elapsed = 0
        days_elapsed += self.day - 1
        
        if self.month > 1: 
            for m in range(1, self.month):
                days_elapsed += self.days_in(self.year, m)
        
        if self.year > 0:
            for y in range(self.year):
                if self.is_leap_year(y):
                    days_elapsed += 366
                else:
                    days_elapsed += 365
            
        return days_elapsed
    
    
    def __eq__(self, right):
        '''Returns a bool indicating whether two date objects are equal.
        Parameter:
        right (Date object): date to be compared against self
        
        Return:
        True: the two dates are equal
        False: the two dates are not equal'''
        if type(right) == type(self) and self.__str__() == right.__str__():
                return True
        else:
            return False
    
    
    def __lt__(self, right):
        '''Returns a bool indicating whether self is less than the right date object.
        Parameter:
        right (Date object): date to be compared against self
        
        Return:
        True: self is less than the right date object
        False: self is not less than the right date object'''
        if type(self) == type(right):
            return self.__len__() < right.__len__()
        elif type(right) is int:
            return self.__len__() < right
        else:
            return NotImplemented
    
    
    def __add__(self, right):
        '''Returns a new date object adding self to the right operand.
        Parameter: 
        right (int): positive or negative integer to be added to self'''
        upd_year = self.year
        upd_month = self.month
        upd_day = self.day
        
        if type(right) is not int:
            raise TypeError('Date.__add__: right operand (' + str(right) + ') not supported; must be of type int or Date')
        elif right > 0:
            for __ in range(right):
                if upd_day < self.days_in(upd_year, upd_month):
                    upd_day += 1
                else:
                    if upd_month < 12:
                        upd_month += 1
                        upd_day = 1
                    else:
                        upd_year += 1
                        upd_month = 1
                        upd_day = 1
        elif right < 0:
            for __ in range(-right):
                if upd_day > 1:
                    upd_day -= 1
                else:
                    if upd_month > 1:
                        upd_month -= 1
                        upd_day = self.days_in(upd_year,upd_month)
                    else:
                        upd_year -= 1
                        upd_month = 12
                        upd_day = 31
        
        return Date(upd_year, upd_month, upd_day)
    
    
    def __radd__(self, left):
        return self.__add__(left)
                            
    
    def __sub__(self, right):
        '''Returns the result of subtracting self from the right operand.
        If right is an int, the result is the number of days in the past from self.
        If right is a Date object, the result is the number of days between self and the right operand.
        Parameter:
        right (int or Date object): integer to be subtracted from self, or Date to be compared against self'''
        if type(right) is int:
            return self.__add__(-right)
        elif type(self) == type(right):
            return self.__len__() - right.__len__()
        else:
            raise TypeError('Date.__sub__: right operand (' + str(right) + ') not supported; must be of type int or Date')
    
    
    def __call__(self, new_year, new_month, new_day):
        '''Allows a date object to be callable with three integers representing an updated year, month, or day.
        If any of the parameters are not legal (see __init__), raises AssertionError.'''
        assert type(new_year) is int and new_year >= 0, 'Date.__init__: invalid year (' + str(new_year) + '); must be type of int greater than or equal to 0'
        assert type(new_month) is int and 1 <= new_month <= 12, 'Date.__init__: invalid month (' + str(new_month) + '); must be type of int between inclusive range 1 to 12'
        assert type(new_day) is int and 1 <= new_day <= self.days_in(new_year, new_month), 'Date.__init__: invalid day (' + str(new_day) + '); must be type of int between inclusive range 1 to ' + str(self.days_in(self.year,self.month))
        
        self.year = new_year
        self.month = new_month
        self.day = new_day
    
    
if __name__ == '__main__':
    # Simple tests
    print('str, repr')
    d = Date(2016,4,15)
    print('d = ' + str(d))
    print('d = ' + repr(d))
    
    print('\nindex')
    print('year: ' + str(d['y']))
    print('month: ' + str(d['m']))
    print('day: ' + str(d['d']))
    print('year, month: ' + str(d[('y', 'm')]))
    
    print('\n==, !=, <, >')
    d1 = Date(2022, 2, 15)
    print(str(d) + ' == ' + str(d1) + ': ' + str(d == d1))
    print(str(d) + ' != ' + str(d1) + ': ' + str(d != d1))
    print(str(d) + ' < ' + str(d1) + ': ' + str(d < d1))
    print(str(d) + ' > ' + str(d1) + ': ' + str(d > d1))
    
    print('\nlen, add, sub')
    print('days elapsed since 1/1/0000: ' + str(len(d)))
    print(str(d) + ' + 100 days: ' + str(d + 100))
    print('50 days + ' + str(d) + ': ' + str(50 + d))
    print(str(d) + ' - 100 days: ' + str(d - 100))
    d3 = Date(2016, 5, 20)
    print('days between ' + str(d) + ' and ' + str(d3) + ': ' + str(d - d3))
    d4 = Date(2000, 7, 10)
    print('days between ' + str(d) + ' and ' + str(d4) + ': ' + str(d - d4))
    # print()
    # import driver
    # driver.default_file_name = 'bscq31W22.txt'
    # driver.default_show_traceback = True
    # # driver.default_show_exception = True
    # # driver.default_show_exception_message = True
    # driver.driver()