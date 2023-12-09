from PyQt6.QtWidgets import *
from Final_Project_2_UI import *
import csv
import random


class Logic(QMainWindow, Ui_Teams_Window):
    """
    The main logic class for the Teams program.

    Attributes:
    - ui: An instance of the UI class generated by PyQt6.
    - people_list: A list to store information about people.
    - team_list: A list to store information about teams.
    - total: A counter to keep track of the total number of people added.

    Methods:
    - __init__: Initializes the Logic class.
    - add_person: Adds a person to the people_list.
    - cont: Checks if there are more than one person added and prepares for randomization.
    - randomize: Randomly assigns people to teams and writes the teams to a CSV file.
    - reset: Resets the UI elements to their initial state.
    """

    def __init__(self) -> None:
        """
        Initializes the Logic class.
        """
        super().__init__()
        self.ui = Ui_Teams_Window()
        self.people_list: list[list[str, int]] = []
        self.team_list: list[list[list[str, int]]] = []
        self.total: int = 0
        self.ui.setupUi(self)
        self.ui.Per_Group_Label.setVisible(False)
        self.ui.spinBox.setMaximum(4)
        self.ui.spinBox.setMinimum(1)
        self.ui.spinBox.setVisible(False)
        self.ui.Error_Label.setVisible(False)
        self.ui.Randomize_Button.clicked.connect(self.randomize)
        self.ui.Randomize_Button.setVisible(False)
        self.ui.Reset_Button.clicked.connect(self.reset)
        self.ui.Reset_Button.setVisible(False)
        self.ui.Add_Person_Button.clicked.connect(self.add_person)
        self.ui.Continue_Button.clicked.connect(self.cont)

    def add_person(self) -> None:
        """
        Adds a person to the people_list based on the entered name and age.

        Checks if the entered name is alphabetic and the age is numeric.
        """
        name: str = self.ui.Name_Entry.text()
        age: str = self.ui.Age_Entry.text()
        if name.isalpha() and age.isnumeric():
            person: list[str, int] = [name, int(age)]
            self.people_list.append(person)
            self.ui.Error_Label.setVisible(False)
            self.total += 1
            self.ui.Name_Entry.setText('')
            self.ui.Age_Entry.setText('')
        elif not name.isalpha() and age.isnumeric():
            self.ui.Error_Label.setVisible(True)
            self.ui.Error_Label.setText('Names must be letters')
        elif name.isalpha() and not age.isnumeric():
            self.ui.Error_Label.setVisible(True)
            self.ui.Error_Label.setText('Ages must be numbers')
        else:
            self.ui.Error_Label.setVisible(True)
            self.ui.Error_Label.setText('Names must be A-Z and Ages must be 0-9')

    def cont(self) -> None:
        """
        Checks if there are more than one person added and prepares for randomization.
        """
        if self.total > 1:
            self.ui.Per_Group_Label.setVisible(True)
            self.ui.Randomize_Button.setVisible(True)
            self.ui.Reset_Button.setVisible(True)
            self.ui.spinBox.setVisible(True)
            self.ui.Error_Label.setVisible(False)
        else:
            self.ui.Error_Label.setVisible(True)
            self.ui.Error_Label.setText("Add more than one person!")

    def randomize(self) -> None:
        """
        Randomly assigns people to teams and writes the teams to a CSV file.
        """
        num_elements: int = self.ui.spinBox.value()
        if self.total % num_elements == 0:
            for j in range(int(len(self.people_list) / num_elements)):
                team: list[list[str, int]] = []
                for i in range(num_elements):
                    random_index: int = random.randint(0, len(self.people_list) - 1)
                    team.append(self.people_list.pop(random_index))
                self.team_list.append(team)
            with open('teams.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.team_list)
        else:
            self.ui.Error_Label.setVisible(True)
            self.ui.Error_Label.setText("Make sure it's divisible!")

    def reset(self) -> None:
        """
        Resets the UI elements to their initial state.
        """
        self.ui.spinBox.setVisible(False)
        self.ui.Error_Label.setVisible(False)
        self.ui.Per_Group_Label.setVisible(False)
        self.ui.Randomize_Button.setVisible(False)
        self.ui.Reset_Button.setVisible(False)
        self.ui.Name_Entry.setText('')
        self.ui.Age_Entry.setText('')
