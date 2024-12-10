import datetime


class WorkoutValidator:
    def validate_date(self, date_str):
        """Validates that the date is not from the future."""
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj > datetime.datetime.now():
                return False
            return True
        except ValueError:
            return False

    def validate_workout(self, workout):
        """Validates that a workout is selected."""
        return bool(workout)  # Ensure a workout is chosen

    def validate_creatine(self, creatine):
        """Validates that creatine is a numeric value."""
        try:
            value = float(creatine)
            return value >= 0  # Creatine should be a non-negative value
        except ValueError:
            return False

    def validate_weight(self, weight):
        """Validates that weight is a numeric value and above 40kg."""
        try:
            value = float(weight)
            return value >= 40
        except ValueError:
            return False


class UserData:
    def __init__(self):
        self.data = {}  # Initialize as an empty dictionary to store user data

    def log_workout(self, date, workout):
        # Ensure the date key exists
        if date not in self.data:
            self.data[date] = {
                "workouts": [],
                "creatine_intake": [],
                "weight": None,
            }  # Initialize all keys
        self.data[date]["workouts"].append(workout)

    def log_creatine_intake(self, date, intake):
        # Ensure the date key exists
        if date not in self.data:
            self.data[date] = {
                "workouts": [],
                "creatine_intake": [],
                "weight": None,
            }  # Initialize all keys
        self.data[date]["creatine_intake"].append(intake)

    def log_weight(self, date, weight):
        # Ensure the date key exists
        if date not in self.data:
            self.data[date] = {
                "workouts": [],
                "creatine_intake": [],
                "weight": None,
            }  # Initialize all keys
        self.data[date][
            "weight"
        ] = weight  # Assign the weight directly (overwrite any previous value)

    def get_daily_summary(self, date):
        # Return a summary including the date
        summary = self.data.get(
            date, {"workouts": [], "creatine_intake": [], "weight": None}
        )
        summary["date"] = date  # Add the 'date' key to the summary
        return summary
