
""""
def buildProfile(firstName, lastName, **otherInfo):
    profile = {}
    profile['firstName'] = firstName
    profile['lastName'] = lastName

    for key, value in otherInfo.items():
        profile[key] = value
    return profile



user1 = buildProfile('Allen', 'Ylagan',
                     location = 'angles',
                     age = 19,
                     program = 'BSIT')

print(user1)

"""

class studentProfile:
    def __init__(self, firstName, lastName,):
        self.firstName = firstName
        self.lastName = lastName

    @property
    def fullName(self):
        fullname =  "{} {}".format(self.firstName, self.lastName)
        return fullname


user1 = studentProfile('Allen', 'Ylagan',)

print(user1.fullName)