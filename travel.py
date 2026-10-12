# ============================================================
# MINI AUTONOMOUS TRAVEL AGENT
# Class Activity 3
# ============================================================
#
# Concepts demonstrated:
# 1. Goal
# 2. LLM / Reasoning
# 3. Memory
# 4. Planning
# 5. Reasoning
# 6. Tools
# 7. Actions
# 8. Observations
# 9. Re-planning
# 10. Human Approval
#
# Deliverables:
# - Agent Architecture
# - Python Implementation
# - Tool Definitions
# - Memory Design
# - Agent Lifecycle
# - Successful Execution
# - Failure/Re-planning Example
# - Human-in-the-loop Safety Rule
# ============================================================


# ------------------------------------------------------------
# 1. MEMORY
# ------------------------------------------------------------

class Memory:

    def __init__(self):
        self.user_preferences = {
            "budget": 15000,
            "preferred_hotel": "3-star",
            "food": "vegetarian",
            "transport": "train"
        }

        self.previous_trips = []

        self.current_trip = {}


    def remember(self, key, value):
        self.current_trip[key] = value


    def get(self, key):
        return self.current_trip.get(key)


    def show_memory(self):

        print("\n========== MEMORY ==========")

        print("User Preferences:")
        for key, value in self.user_preferences.items():
            print(f"{key}: {value}")

        print("\nPrevious Trips:")
        if not self.previous_trips:
            print("No previous trips.")

        for trip in self.previous_trips:
            print(trip)

        print("============================")


# ------------------------------------------------------------
# 2. TRAVEL DATABASE
# ------------------------------------------------------------

class TravelDatabase:

    def __init__(self):

        self.trains = {
            "Bangalore-Goa": [
                {
                    "name": "Goa Express",
                    "time": "06:00 AM",
                    "price": 900,
                    "available": True
                },
                {
                    "name": "Karnataka Express",
                    "time": "09:30 AM",
                    "price": 1100,
                    "available": True
                }
            ]
        }

        self.hotels = {
            "Goa": [
                {
                    "name": "Sea View Hotel",
                    "type": "3-star",
                    "price": 2500,
                    "available": True
                },
                {
                    "name": "Beach Comfort",
                    "type": "3-star",
                    "price": 3000,
                    "available": True
                },
                {
                    "name": "Luxury Palace",
                    "type": "5-star",
                    "price": 6000,
                    "available": True
                }
            ]
        }

        self.places = {
            "Goa": [
                "Baga Beach",
                "Fort Aguada",
                "Basilica of Bom Jesus",
                "Dudhsagar Falls"
            ]
        }


# ------------------------------------------------------------
# 3. TOOLS
# ------------------------------------------------------------

class TravelTools:

    def __init__(self, database):

        self.database = database


    # TOOL 1 - Search Train

    def search_train(self, source, destination):

        print("\n[TOOL] Searching trains...")

        route = source + "-" + destination

        trains = self.database.trains.get(route, [])

        if not trains:
            print("[OBSERVATION] No trains found.")
            return None

        for train in trains:
            if train["available"]:
                print(
                    f"Train: {train['name']} | "
                    f"Time: {train['time']} | "
                    f"Price: ₹{train['price']}"
                )

        return trains[0]


    # TOOL 2 - Search Hotel

    def search_hotel(self, destination, hotel_type):

        print("\n[TOOL] Searching hotels...")

        hotels = self.database.hotels.get(destination, [])

        for hotel in hotels:

            if (
                hotel["type"] == hotel_type
                and hotel["available"]
            ):
                print(
                    f"Hotel: {hotel['name']} | "
                    f"Type: {hotel['type']} | "
                    f"Price: ₹{hotel['price']}"
                )

                return hotel

        print("[OBSERVATION] Requested hotel unavailable.")

        return None


    # TOOL 3 - Search Tourist Places

    def search_places(self, destination):

        print("\n[TOOL] Searching tourist places...")

        places = self.database.places.get(destination, [])

        for place in places:
            print(" -", place)

        return places


    # TOOL 4 - Book Train

    def book_train(self, train):

        print("\n[ACTION] Booking train...")

        if train is None:
            print("[OBSERVATION] Train booking failed.")
            return False

        if train["available"]:

            train["available"] = False

            print(
                f"[ACTION SUCCESS] {train['name']} booked successfully."
            )

            return True

        print("[OBSERVATION] Train is no longer available.")

        return False


    # TOOL 5 - Book Hotel

    def book_hotel(self, hotel):

        print("\n[ACTION] Booking hotel...")

        if hotel is None:

            print("[OBSERVATION] Hotel booking failed.")

            return False

        if hotel["available"]:

            hotel["available"] = False

            print(
                f"[ACTION SUCCESS] {hotel['name']} booked successfully."
            )

            return True

        print("[OBSERVATION] Hotel is no longer available.")

        return False


# ------------------------------------------------------------
# 4. LLM / REASONING COMPONENT
# ------------------------------------------------------------

class SimpleLLM:

    def understand_request(self, user_request):

        print("\n[LLM] Understanding user request...")

        request = user_request.lower()

        result = {
            "source": "Bangalore",
            "destination": "Goa",
            "budget": 15000,
            "days": 3
        }

        if "goa" in request:
            result["destination"] = "Goa"

        if "bangalore" in request:
            result["source"] = "Bangalore"

        print("[LLM] User goal understood.")

        return result


    def reason(self, message):

        print("\n[REASONING]", message)


# ------------------------------------------------------------
# 5. TRAVEL AGENT
# ------------------------------------------------------------

class TravelAgent:

    def __init__(self):

        self.memory = Memory()

        self.database = TravelDatabase()

        self.tools = TravelTools(self.database)

        self.llm = SimpleLLM()


    # --------------------------------------------------------
    # GOAL
    # --------------------------------------------------------

    def identify_goal(self, user_request):

        print("\n========================================")
        print("1. IDENTIFY GOAL")
        print("========================================")

        goal = self.llm.understand_request(user_request)

        self.memory.remember(
            "destination",
            goal["destination"]
        )

        self.memory.remember(
            "source",
            goal["source"]
        )

        self.memory.remember(
            "budget",
            goal["budget"]
        )

        self.memory.remember(
            "days",
            goal["days"]
        )

        return goal


    # --------------------------------------------------------
    # PLANNING
    # --------------------------------------------------------

    def create_plan(self, goal):

        print("\n========================================")
        print("2. PLANNING")
        print("========================================")

        plan = [
            "Search train",
            "Search hotel",
            "Search tourist places",
            "Check total cost",
            "Ask human approval",
            "Book train",
            "Book hotel",
            "Show final itinerary"
        ]

        for i, step in enumerate(plan, 1):

            print(f"{i}. {step}")

        return plan


    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    def reasoning(self, train, hotel, goal):

        print("\n========================================")
        print("3. REASONING")
        print("========================================")

        train_price = train["price"] if train else 0
        hotel_price = hotel["price"] if hotel else 0

        total_hotel = hotel_price * goal["days"]

        total = train_price + total_hotel

        print(f"Train cost: ₹{train_price}")

        print(
            f"Hotel cost: ₹{hotel_price} x "
            f"{goal['days']} days = ₹{total_hotel}"
        )

        print(f"Estimated total: ₹{total}")

        if total <= goal["budget"]:

            print("Reasoning result: Trip is within budget.")

            return total

        print("Reasoning result: Trip exceeds budget.")

        return total


    # --------------------------------------------------------
    # HUMAN APPROVAL
    # --------------------------------------------------------

    def human_approval(self, total):

        print("\n========================================")
        print("4. HUMAN-IN-THE-LOOP")
        print("========================================")

        print(f"Estimated booking amount: ₹{total}")

        print("\nSAFETY RULE:")
        print("The agent cannot make bookings without human approval.")

        while True:

            answer = input(
                "\nDo you approve the booking? (yes/no): "
            ).lower()

            if answer == "yes":

                print("[HUMAN APPROVAL] Approved.")

                return True

            elif answer == "no":

                print("[HUMAN APPROVAL] Booking rejected.")

                return False

            else:

                print("Please enter yes or no.")


    # --------------------------------------------------------
    # OBSERVATION
    # --------------------------------------------------------

    def observe(self, message):

        print("\n[OBSERVATION]", message)


    # --------------------------------------------------------
    # RE-PLANNING
    # --------------------------------------------------------

    def replan(self, failed_item):

        print("\n========================================")
        print("5. RE-PLANNING")
        print("========================================")

        print(f"Problem detected: {failed_item}")

        self.llm.reason(
            "The selected option failed. "
            "I will search for another available option."
        )

        print("New plan created.")

        return True


    # --------------------------------------------------------
    # MAIN AGENT LIFECYCLE
    # --------------------------------------------------------

    def run(self, user_request):

        print("\n")
        print("########################################")
        print("#       MINI AUTONOMOUS TRAVEL AGENT   #")
        print("########################################")

        # STEP 1 - Goal

        goal = self.identify_goal(user_request)


        # STEP 2 - Memory

        print("\n========================================")
        print("6. MEMORY")
        print("========================================")

        self.memory.show_memory()


        # STEP 3 - Planning

        plan = self.create_plan(goal)


        # STEP 4 - Search Train

        print("\n========================================")
        print("7. TOOL: TRAIN SEARCH")
        print("========================================")

        train = self.tools.search_train(
            goal["source"],
            goal["destination"]
        )

        if train is None:

            self.observe("Train search failed.")

            self.replan("No train available.")

            return


        # STEP 5 - Search Hotel

        print("\n========================================")
        print("8. TOOL: HOTEL SEARCH")
        print("========================================")

        hotel = self.tools.search_hotel(
            goal["destination"],
            self.memory.user_preferences["preferred_hotel"]
        )

        # ----------------------------------------------------
        # FAILURE + REPLANNING EXAMPLE
        # ----------------------------------------------------

        if hotel is None:

            self.observe(
                "Preferred hotel is unavailable."
            )

            self.replan(
                "Preferred hotel unavailable."
            )

            # Try another hotel

            print("\n[RE-PLANNING] Searching for another hotel...")

            hotels = self.database.hotels[goal["destination"]]

            hotel = None

            for h in hotels:

                if h["available"]:

                    hotel = h

                    print(
                        f"[NEW OPTION] {h['name']} selected."
                    )

                    break


        # STEP 6 - Tourist Places

        print("\n========================================")
        print("9. TOOL: TOURIST PLACE SEARCH")
        print("========================================")

        places = self.tools.search_places(
            goal["destination"]
        )


        # STEP 7 - Reasoning

        total = self.reasoning(
            train,
            hotel,
            goal
        )


        # STEP 8 - Budget checking

        if total > goal["budget"]:

            print("\n[OBSERVATION]")
            print("Trip exceeds the user's budget.")

            print("\n[RE-PLANNING]")
            print("Searching for a cheaper hotel...")

            hotels = self.database.hotels[
                goal["destination"]
            ]

            cheaper_hotel = None

            for h in hotels:

                if (
                    h["available"]
                    and h["price"] < hotel["price"]
                ):

                    cheaper_hotel = h
                    break

            if cheaper_hotel:

                hotel = cheaper_hotel

                total = self.reasoning(
                    train,
                    hotel,
                    goal
                )

            else:

                print(
                    "No cheaper hotel available."
                )

                return


        # STEP 9 - Human approval

        approved = self.human_approval(total)

        if not approved:

            print("\nAgent stopped safely.")

            print(
                "No booking was made because "
                "human approval was not provided."
            )

            return


        # STEP 10 - ACTION: BOOK TRAIN

        print("\n========================================")
        print("10. ACTION: BOOK TRAIN")
        print("========================================")

        train_success = self.tools.book_train(train)


        # STEP 11 - OBSERVATION

        if not train_success:

            self.observe(
                "Train booking failed."
            )

            self.replan(
                "Train became unavailable."
            )

            return


        # STEP 12 - ACTION: BOOK HOTEL

        print("\n========================================")
        print("11. ACTION: BOOK HOTEL")
        print("========================================")

        hotel_success = self.tools.book_hotel(hotel)


        if not hotel_success:

            self.observe(
                "Hotel booking failed."
            )

            self.replan(
                "Hotel became unavailable."
            )

            return


        # STEP 13 - SUCCESSFUL EXECUTION

        print("\n========================================")
        print("12. SUCCESSFUL EXECUTION")
        print("========================================")

        print("\nTravel plan completed successfully!")

        print("\n========== FINAL ITINERARY ==========")

        print(
            f"From: {goal['source']}"
        )

        print(
            f"To: {goal['destination']}"
        )

        print(
            f"Days: {goal['days']}"
        )

        print(
            f"Train: {train['name']}"
        )

        print(
            f"Train Time: {train['time']}"
        )

        print(
            f"Hotel: {hotel['name']}"
        )

        print(
            f"Hotel Type: {hotel['type']}"
        )

        print(
            f"Total Estimated Cost: ₹{total}"
        )

        print("\nTourist Places:")

        for place in places:

            print(" -", place)

        print("\n======================================")


        # Save trip to memory

        self.memory.previous_trips.append({
            "destination": goal["destination"],
            "train": train["name"],
            "hotel": hotel["name"],
            "cost": total
        })


        print("\nTrip saved to memory.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    agent = TravelAgent()

    user_request = input(
        "\nEnter your travel request: "
    )

    agent.run(user_request)

    print("\n")
    print("########################################")
    print("#          AGENT TASK COMPLETE         #")
    print("########################################")