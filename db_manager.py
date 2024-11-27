import sqlite3
from datetime import datetime

DB_FILE = "pipeline_records.db"
SQL_FILE = "pipeline_schema.sql"

# Initialize the database
def initialize_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Read and execute schema from SQL file
    with open(SQL_FILE, "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)

    connection.commit()
    connection.close()
    print(f"Database initialized successfully from {SQL_FILE}")


# Insert into Inputs Table
def insert_input(buggy_code, language, mode):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO inputs (timestamp, buggy_code, language, mode)
        VALUES (?, ?, ?, ?)
    """, (timestamp, buggy_code, language, mode))
    input_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return input_id


# Insert into Generated Code Table
def insert_generated_code(input_id, model_name, dafny_code, generated_code):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO generated_code (input_id, timestamp, model_name, dafny_code, generated_code)
        VALUES (?, ?, ?, ?, ?)
    """, (input_id, timestamp, model_name, dafny_code, generated_code))
    generated_code_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return generated_code_id


# Insert into Evaluation Results Table
def insert_evaluation_results(input_id, generated_code_id, static_analysis_results, dynamic_analysis_results, rankme_score, formal_verification_results):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO evaluation_results (input_id, generated_code_id, timestamp, static_analysis_results, dynamic_analysis_results, rankme_score, formal_verification_results)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (input_id, generated_code_id, timestamp, static_analysis_results, dynamic_analysis_results, rankme_score, formal_verification_results))
    evaluation_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return evaluation_id


# Insert into Final Output Table
def insert_final_output(input_id, feedback_code, evaluation_summary, improvement_tips):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO final_output (input_id, timestamp, feedback_code, evaluation_summary, improvement_tips)
        VALUES (?, ?, ?, ?, ?)
    """, (input_id, timestamp, feedback_code, evaluation_summary, improvement_tips))
    final_output_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return final_output_id


# Delete Inputs Table Record (and cascade deletes)
def delete_input(input_id):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # Delete related records
    cursor.execute("DELETE FROM final_output WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM evaluation_results WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM generated_code WHERE input_id = ?", (input_id,))
    cursor.execute("DELETE FROM inputs WHERE id = ?", (input_id,))

    connection.commit()
    connection.close()
    print(f"Input {input_id} and all related records deleted successfully")


# Example Usage
if __name__ == "__main__":
    # Initialize database
    
    initialize_database()

    # Simulated pipeline operations
    input_id = insert_input("def buggy(): pass", "Python", "mode1")
    print(f"Inserted Input ID: {input_id}")

    primary_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def fixed(): return True")
    print(f"Inserted Primary Model Code ID: {primary_model_id}")

    primary_eval_id = insert_evaluation_results(input_id, primary_model_id, "No errors", "No runtime issues", 0.95, "Passed verification")
    print(f"Inserted Primary Model Evaluation ID: {primary_eval_id}")

    supplemental_model_id = insert_generated_code(input_id, "llama-3.2-3b-instruct", None, "def alternate(): return False")
    print(f"Inserted Supplemental Model Code ID: {supplemental_model_id}")

    supplemental_eval_id = insert_evaluation_results(input_id, supplemental_model_id, "Minor warnings", "No runtime issues", 0.90, "Passed verification with notes")
    print(f"Inserted Supplemental Model Evaluation ID: {supplemental_eval_id}")

    feedback_model_id = insert_generated_code(input_id, "qwen-coder-32b-instruct", None, "def improved(): return 'Done'")
    print(f"Inserted Feedback Model Code ID: {feedback_model_id}")

    feedback_eval_id = insert_evaluation_results(input_id, feedback_model_id, "Perfect", "No runtime issues", 1.0, "Passed all checks")
    print(f"Inserted Feedback Model Evaluation ID: {feedback_eval_id}")

    final_output_id = insert_final_output(input_id, "def final(): return 'Success'", "Well-optimized code", "Consider adding more documentation")
    print(f"Inserted Final Output ID: {final_output_id}")
    
    # Deletion example
    delete_input(1)
