from datetime import datetime


class WorkoutValidator:
    def __init__(self):
        pass

    def validate_date(self, selected_date):
        """Validate that the date is not from the future and is in a logical range."""
        try:
            date_obj = datetime.strptime(selected_date, "%d-%m-%Y")
            if date_obj > datetime.today():
                return False
            return True
        except ValueError:
            return False

    def validate_workout(self, selected_workouts):
        """at least one workout is selected."""
        return bool(selected_workouts)

    def validate_creatine(self, creatine_intake):
        """creatine intake is a valid number (integer or float)."""
        try:
            creatine = float(creatine_intake)
            return creatine > 0
        except ValueError:
            return False

    def validate_weight(self, weight):
        """weight is a valid number (integer or float) and contains no alphabetic characters."""
        try:
            weight_val = float(weight)
            return weight_val > 40
        except ValueError:
            return False


class UserData:
    def __init__(self):
        self.workout_data = {}
        self.creatine_data = {}

    def log_workout(self, date, workout):
        """Log workout data for a specific date."""
        if date not in self.workout_data:
            self.workout_data[date] = []
        self.workout_data[date].append(workout)

    def log_creatine_intake(self, date, creatine):
        """Log creatine intake data."""
        if date not in self.creatine_data:
            self.creatine_data[date] = []
        self.creatine_data[date].append(creatine)

    def get_daily_summary(self, date):
        """Get the summary of workouts and creatine intake for a specific date."""
        workouts = self.workout_data.get(date, [])
        creatine_intake = self.creatine_data.get(date, [])

        return {
            "date": date,
            "workouts": workouts,
            "creatine_intake": creatine_intake,
        }
