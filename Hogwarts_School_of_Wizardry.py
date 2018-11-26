import datetime
from typing import NamedTuple
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


class HogwartsMember:
    """
    Creates a member of the Hogwarts School of Magic
    """

    def __init__(self, name: str, birthyear: int, sex: str):
        self._name = name
        self.birthyear = birthyear
        self.sex = sex
        self._traits = {}

    def __repr__(self):
        return f"Class:{self.__class__.__name__}, Name: {self._name}, Birthyear: {self.birthyear}"

    def says(self, words: str):
        return f"{self._name} says {words}"

    def add_trait(self, trait, value=True):
        self._traits[trait] = value

    def print_traits(self):
        true_traits = [trait for trait, value in self._traits.items() if value]
        false_traits = [trait for trait, value in self._traits.items() if not value]

        print(f"{self._name}'s positive traits are :{', '.join(true_traits)}" f" and the negative traits are {', '.join(false_traits)}")

    """
    The following function is an implementation of the pythonic way of EAFP
    Which means asking for forgiveness is bettter than asking for permission principle.
    """

    def exhibits_trait(self, trait):
        try:
            value = self._traits[trait]
        except KeyError:
            print(f"{self._name} does not have a character trait with the name '{trait}'")
            return

        if value:
            print(f"Yes, {self._name} is {trait}!")
        else:
            print(f"No, {self._name} is not {trait}!")

    @staticmethod
    def school_headmaster():
        return HogwartsMember('Albus Dumbledore', 1881, 'male')

    @property
    def age(self):
        now = datetime.datetime.now().year
        return now - self.birthyear

    @property
    def name(self):
        return self._name


class Pupil(HogwartsMember):
    """
    Create a Castle Kilmere Pupil
    """

    def __init__(self, name: str, birthyear: int, sex: str, house: str, start_year: int, pet: tuple=None):
        super().__init__(name, birthyear, sex)
        self.house = house
        self.start_year = start_year

        if pet is not None:
            self.pet_name, self.pet_type = pet

        self._elms = {
            'Broomstick Flying': False,
            'Art': False,
            'Magical Theory': False,
            'Foreign Magical Systems': False,
            'Charms': False,
            'Defence Against Dark Magic': False,
            'Divination': False,
            'Herbology': False,
            'History of Magic': False,
            'Potions': False,
            'Transfiguration': False}

        self._friends = []

        self.known_spells = set()

    @staticmethod
    def passed(grade):
        '''Dictionary of grades that are passing or not'''

        grades = {
            'E': True,
            'Exceptional': True,
            'G': True,
            'Good': True,
            'A': True,
            'Acceptable': True,
            'P': False,
            'Poor': False,
            'H': False,
            'Horrible': False,
        }
        return grades.get(grade, False)

    def learn_spell(self, spell):
        if spell.min_year is not None:
            if spell.min_year >= self.current_year:
                self.known_spells.add(spell)
                print(f"{self._name} now know's the spell {spell.name}")

            elif self.exhibits_trait('Highly Intelligent'):
                self.known_spells.add(spell)
                print(f"{self._name} now know's the spell {spell.name}")

            elif self.current_year < spell.min_year:
                print('Student is too young to learn this type of magic!')

        elif spell.__class__.__name__ in ['Hex', 'Curse']:
            # Only Slytherin's would study hexes and curses
            if (self.house == 'Slytherin'):
                print(f"{self._name} now knows spell {spell.name}")
                self.known_spells.add(spell)

            else:
                print(f"How dare you study a hex or curse?!")

    def cast_spell(self, spell):
        if spell.__class__.__name__ in ['Hex', 'Curse']:
            if self.house == 'Slytherin':
                print(f"{self._name} has cast {spell.name}")
            else:
                print('How dare you cast a hex or a curse')
        elif spell in self.known_spells:
            print(f"{self._name} has cast {spell.name}")

        elif spell.name not in self.known_spells:
            print(f"You can't cast the {spell.name} spell correctly "
                  f" - you have to study it first! ")

    @classmethod
    def ron(cls):
        return cls('Ronald Weasley', 1990, 'male', 'Gryffindor', 2018)

    @classmethod
    def hermione(cls):
        return cls('Flynn Gibbs', 1990, 'female', 'Gryffindor', 2018, ('Twiggles', 'owl'))

    @classmethod
    def cassidy(cls):
        return cls('Cassidy', 1991, 'female', 'Gryffindor', 2018, ('Ramses', 'cat'))

    @classmethod
    def adrien(cls):
        return cls('Adrien Fulford', 1992, 'male', 'Slytherin', 2018, ('Unnamed', 'owl'))

    @property
    def friends(self):
        return f"{self._name}'s current friends are: {[person._name for person in self._friends]}"

    @property
    def current_year(self):
        now = datetime.datetime.now().year
        return (now - self.start_year) + 1


# create the setter method for the student and the grade associated.
# Will need to create an assertion that the subject is in the list of classes (to avoid spelling mistake errors or adding in the wrong class altogether)

    @property
    def elms(self):
        return self._elms

    @elms.setter
    def elms(self, subject_and_grade):
        try:
            subject, grade = subject_and_grade
        except ValueError:
            raise ValueError("Insert the subject and grade as such (Subject, Grade)")

        passed = self.passed(grade)

        if passed:
            self._elms[subject] = True
        else:
            print("Exam not passed, Didn't get the elm")

    @elms.deleter
    def elms(self):
        print("Caution, you are deleting this students' ELM's! "
              "You should only do that if she/he dropped out of school without passing any exam!")
        del self._elms

    def befriend(self, person):
        """Adds another person to your list of friends"""
        if (person.__class__.__name__ != 'HogwartsMember'
            and self.house != 'Slytherin'
                and person.house == 'Slytherin'):
            print("Are you sure you want to be friends with someone from Slytherin?")

        self._friends.append(person)
        print(f"{person._name} is now your friend!")


class Professor(HogwartsMember):
    """
    Creates a Castle Kilmere professor
    """

    def __init__(self, name: str, birthyear: int, sex: str, subject: str, house: str=None):
        super().__init__(name, birthyear, sex)
        self.subject = subject
        if house is not None:
            self.house = house

    def __repr__(self):
        return f"Class: {__class__.__name__}, Name: {self._name}, Birthyear: {self.birthyear}, Subject: {self.subject}"

    @classmethod
    def mirren(cls):
        return cls('Miranda Mirren', 1963, 'female', 'Transfiguration', 'Gryffindor')

    @classmethod
    def blade(cls):
        return cls('Blade Bardock', 1988, 'male', 'Potions', 'Slytherin')

    def __repr__(self):
        return f"Class:{self.__class__.__name__}, Name: {self._name}, Birthyear: {self.birthyear}"


class Ghost(HogwartsMember):
    """
    Creates a Castle Kilmere ghost
    """

    def __init__(self, name, birthyear, sex, year_of_death, house=None):
        super().__init__(name, birthyear, sex)
        self.year_of_death = year_of_death

        if house is not None:
            self.house = house

    def __repr__(self):

        return f"{self.__class__.__name__}, Name:{self._name}, Birthyear: {self.birthyear}, Year of Death: {self.year_of_death}"

    @classmethod
    def mocking(cls):
        return cls('Mocking Jay', 1956, 'M', 1997, 'Gryffindor')


class Spell(metaclass=ABCMeta):

    def __init__(self, name: str, incantation: str, effect: str, min_year: int = None):
        self.name = name
        self.incantation = incantation
        self.effect = effect
        self.min_year = min_year

        @abstractmethod
        def cast(self):
            pass

        @property
        @abstractmethod
        def defining_feature(self):
            pass

        def __repr__(self):
            return f"{self.__class__.__name__}({self.name}, incantation: '{self.incantation}', effect: {self.effect})"


class Charm(Spell):

    def __init__(self, name: str, incantation: str, effect: str, difficulty: str =None, min_year: int = None):
        super().__init__(name, incantation, effect, min_year)
        self.difficulty = difficulty

    def cast(self):
        return print(f"{self.incantation}!")

    @property
    def defining_feature(self):
        return ("Alteration of the object's inherent qualities, "
                "that is, its behaviour and capabilities")

    @classmethod
    def stuporus_ratiato(cls):
        return cls('Stuporus Ratatio', 'simple', 'Levitates objects')

    @classmethod
    def lumos(cls):
        return cls('Lumos', 'Lumos', 'Illuminates the wand tip', 'simple', 5)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.incantation}, Difficulty: {self.difficulty}, Effect: {self.effect}"


class Hex(Spell):
    def __init__(self, name: str, incantation: str, effect: str, difficulty: str =None, min_year: int = None):
        super().__init__(name, incantation, effect)
        self.difficulty = difficulty

    def cast(self):
        return print(f"{self.incantation}")

    @property
    def defining_feature(self):
        return ("They are affiliated with Dark Magic, darker than a jinx but not as dark as a curse,and generally causes moderate suffering to the victim")


class Jinx(Spell):
    """
    Creates a jinx -
    a spell whose effects are irritating but amusing
    """

    def __init__(self, name: str, incantation: str, effect: str):
        super().__init__(name, incantation, effect)

    @property
    def defining_feature(self):
        return ("Minor darf magic - "
                "a spell whose effects are irritating but amusing, "
                "almost playful and of minor inconvenience to the target")

    def cast(self):
        pass


class Curse(Spell):
    """
    Creates a curse -
    a spell that affects an object in a stflynngly negative manner
    """

    def __init__(self, name: str, incantation: str, effect: str, difficulty: str = None):
        super().__init__(name, incantation, effect)

    @property
    def defining_feature(self):
        return ("Worst kind of dark magic - "
                "Intended to affect an object in a stflynngly negative manner.")

    def cast(self):
        pass


class CounterSpell(Spell):
    """
    Creates a counter-spell -
    a spell that inhibits the effect of another spell
    """

    def __init__(self, name: str, incantation: str, effect: str):
        super().__init__(name, incantation, effect)

    @property
    def defining_feature(self):
        return ("Inhibites the effects of another spell")

    def cast(self):
        pass


class HealingSpell(Spell):
    """
    Creates a healing-spell -
    a spell that improves the condition of a living object
    """

    def __init__(self, name: str, incantation: str, effect: str):
        super().__init__(name, incantation, effect)

    @property
    def defining_feature(self):
        return ("Improves the condition of a living object")

    def cast(self):
        pass


class DarkArmyMember(NamedTuple):
    name: str
    birthyear: int

    @property
    def leader(self):
        lord_odon = HogwartsMember('Lord Odon', 1939, 'Male')
        return lord_odon

    def __repr__(self):
        return f"Name: {self.name} and birthyear is {self.birthyear} "


@dataclass
class House():
    name: str
    traits: list
    year_founded: int
    head: Professor
    ghost: Ghost

    def age(self):
        now = datetime.datetime.now().year
        return f"{self.name} is {now - self.year_founded + 1} years old"


if __name__ == "__main__":
    now = 1993

    wing_lev = Charm.stuporus_ratiato()
    rictum = Charm('Tickling Charm', 'Rictumsempra', 'Causes victim to laugh nonstop', min_year=5)
    stickfast = Hex('Stickfast Hex', 'Colloshoo', "Makes target's shoes stick to ground")
    crutio = Curse('Cruciatus Curse', 'Crucio', 'Causes intense, excruciating pain for victim', 'difficult')

    ron = Pupil.ron()
    hermione = Pupil.hermione()
    adrien = Pupil.adrien()
    cassidy = Pupil.cassidy()
    cassidy.add_trait('highly intelligent')
    mirren = Professor.mirren()
    mocking_ghost = Ghost.mocking()

    print("ron knows the following spells: ", ron.known_spells)
    print("ron is currently in year: ", ron.current_year)
    ron.learn_spell(wing_lev)
    print('=======================================')

    # Test whether ron can learn a spell he is too young for
    ron.learn_spell(rictum)
    # Can cassidy study the spell?
    hermione.learn_spell(rictum)
    print('=======================================')

    # Test whether ron can study a hex
    ron.learn_spell(stickfast)
    print('=======================================')
    # Can Malfoy perform a hex?
    adrien.learn_spell(stickfast)
    print('=======================================')

    # Test whether ron can study a curse
    ron.learn_spell(crutio)
    print('=======================================')
    # Can Malfoy study a curse?
    adrien.learn_spell(crutio)
    print('=======================================')

    # Test whether ron can cast a Charm
    ron.cast_spell(wing_lev)
    print('=======================================')

    # What about a hex?
    ron.cast_spell(stickfast)
    print('=======================================')

    # What about Malfoy?
    adrien.cast_spell(stickfast)
    print('=======================================')

    gryffindor = House('Gryffindor', '[bravery, gryffindor]', 991, mirren, mocking_ghost)
    print(gryffindor.age())
