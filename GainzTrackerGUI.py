from PyQt5.QtWidgets import QDialog, QMessageBox
from Logic import WorkoutValidator, UserData  # Import from Logic.py
from PyQt5 import uic
from PyQt5.QtCore import QDate


class GainzTrackerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GainzTracker.ui", self)  # Load the UI
        self.validator = WorkoutValidator()  # Create instance of WorkoutValidator
        self.user_data = UserData()  # Create instance of UserData

        self.ui.pushButton.clicked.connect(self.submit_data)

    def submit_data(self):
        # Get the selected date, workout, and creatine intake
        selected_date = self.ui.Date.date().toString(
            "dd-MM-yyyy"
        )  # Convert to string format
        selected_workouts = (
            self.ui.ComboBox.get_checked_items()
        )  # Replace with the correct method for getting checked items
        creatine_intake = self.ui.Creatine.text()
        weight = self.ui.Weight.text()

        # Validate the data
        if not self.validator.validate_date(selected_date):
            QMessageBox.warning(
                self,
                "Invalid Date",
                "Please select a valid date (not from the future).",
            )
            return

        if not self.validator.validate_workout(selected_workouts):
            QMessageBox.warning(
                self, "No Workout Selected", "Please choose at least one workout."
            )
            return

        if not self.validator.validate_creatine(creatine_intake):
            QMessageBox.warning(
                self,
                "Invalid Creatine Intake",
                "Please enter a valid creatine intake (numeric value).",
            )
            return

        if not self.validator.validate_weight(weight):
            QMessageBox.warning(
                self,
                "Invalid Weight",
                "Please enter a valid weight  (numeric value and above 40Kg ).",
            )
            return

        # If validation passes, log the data
        self.user_data.log_workout(selected_date, ", ".join(selected_workouts))

        # Log the creatine intake
        if creatine_intake:
            self.user_data.log_creatine_intake(selected_date, float(creatine_intake))

        # Display a summary of the day
        daily_summary = self.user_data.get_daily_summary(selected_date)
        self.show_daily_summary(daily_summary)

    def show_daily_summary(self, summary):
        """Display the summary of the day in a message box."""
        summary_text = f"Date: {summary['date']}\n\n"

        summary_text += "Workouts:\n"
        for workout in summary["workouts"]:
            summary_text += f"- {workout}\n"

        summary_text += "\nCreatine Intake:\n"
        for intake in summary["creatine_intake"]:
            summary_text += f"- {intake}g\n"

        QMessageBox.information(self, "Daily Summary", summary_text)
