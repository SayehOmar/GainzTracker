from turtle import right
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from Logic import WorkoutValidator, UserData  # Import from Logic.py
from PyQt5 import uic
from PyQt5.QtCore import QDate
import sys
from DatabaseConnection import DatabaseManager


class GainzTrackerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GainzTracker.ui", self)  # Load the UI
        self.validator = WorkoutValidator()  # Create instance of WorkoutValidator
        self.user_data = UserData()  # Create instance of UserData
        self.db_manager = DatabaseManager()  # Initialize the database manager
        self.ui.Date.setDate(
            QDate.currentDate()
        )  # Default the date to the current date

        self.ui.pushButton.clicked.connect(
            self.submit_data
        )  # Connect the submit button

    def submit_data(self):
        # Get the selected date, workout, creatine intake, and weight
        selected_date = self.ui.Date.date().toString(
            "yyyy-MM-dd"
        )  # Convert to string format
        selected_workouts = (
            self.ui.Workout.currentText()
        )  # Get selected workout from ComboBox
        creatine_intake = self.ui.Creatine.text()  # Get creatine intake from QLineEdit
        weight = self.ui.Weight.text()  # Get weight from QLineEdit

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
                "Please enter a valid weight (numeric value and above 40Kg).",
            )
            return

        # If validation passes, log the data
        self.user_data.log_workout(selected_date, selected_workouts)

        # Log the creatine intake
        if creatine_intake:
            self.user_data.log_creatine_intake(selected_date, float(creatine_intake))

        # Log the weight
        if weight:
            self.user_data.log_weight(selected_date, float(weight))

        # Display a summary of the day
        daily_summary = self.user_data.get_daily_summary(selected_date)
        self.show_daily_summary(daily_summary)
        # Insert data into PostgreSQL database
        self.db_manager.insert_data(
            selected_date, selected_workouts, float(creatine_intake), float(weight)
        )

        # Clear the fields after submission
        self.clear_fields()

    def show_daily_summary(self, summary):
        """Display the summary of the day in a message box."""
        summary_text = f"Date: {summary['date']}\n\n"

        summary_text += "Workouts:\n"
        for workout in summary["workouts"]:
            summary_text += f"- {workout}\n"

        summary_text += "\nCreatine Intake:\n"
        for intake in summary["creatine_intake"]:
            summary_text += f"- {intake}g\n"

        if summary["weight"] is not None:
            summary_text += f"\nWeight: {summary['weight']}Kg\n"
        else:
            summary_text += "\nWeight: Not recorded\n"

        QMessageBox.information(self, "Daily Summary", summary_text)

        QMessageBox.information(
            self, "Success", "Your data has been successfully saved !"
        )

    def clear_fields(self):
        """Clear the form fields."""
        self.ui.Date.setDate(QDate.currentDate())  # Reset the date to today
        self.ui.Workout.setCurrentIndex(0)  # Reset the ComboBox to the first item
        self.ui.Creatine.clear()  # Clear the creatine intake QLineEdit
        self.ui.Weight.clear()  # Clear the weight QLineEdit

    def closeEvent(self, event):
        """Close database connection on app exit."""
        self.db_manager.close()


# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = GainzTrackerApp()
    dialog.show()
    sys.exit(app.exec_())
