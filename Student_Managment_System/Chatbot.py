import re

class Chatbot:

    def __init__(self,db_instance):
        self.db_instance=db_instance

    def process_query(self,user_input):
        user_input_clean=user_input.strip().lower()

        if "how many" in user_input_clean or "count" in user_input_clean or "total" in user_input_clean:
            students=self.db_instance.fetch_all_students()
            return f"There are {len(students)} registered in the database"
        elif "all" in user_input_clean or "list" in user_input_clean or "show students" in user_input_clean:
            students=self.db_instance.fetch_all_students()
            if not students:
                return "No students found in database"
            response="Here are all the Students:\n"
            for s in students:
                response += f"- ID: {s[0]} | Name: {s[1]} | Age: {s[2]} | Grade: {s[3]}\n"
            return response
        elif "id" in user_input_clean or "find" in user_input_clean or "search" in user_input_clean:
            match=re.search(r'\b\d+\b',user_input_clean)
            if match:
                student_id=int(match.group())
                student=self.db_instance.fetch_students_by_id(student_id)
                if student:
                    return f"Student Found ----> ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}"
                else:
                    return f"No student found with ID {student_id}"
            else:
                return "Please provide a valid ID for your request (e.g., 'Find student 5')"
        else:
            return(
                "I'm not sure how to handle that request yet.\n"
                "Try asking:\n"
                "- 'Show all students'\n"
                "- 'How many students are there?'\n"
                "- 'Find student 3'"
            )