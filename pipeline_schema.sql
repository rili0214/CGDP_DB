-- Create Inputs Table
CREATE TABLE inputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    buggy_code TEXT NOT NULL,
    language TEXT NOT NULL,
    mode TEXT NOT NULL
);

-- Create Generated Code Table
CREATE TABLE generated_code (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    model_name TEXT NOT NULL,
    dafny_code TEXT,
    generated_code TEXT NOT NULL,
    FOREIGN KEY(input_id) REFERENCES inputs(id)
);

-- Create Evaluation Results Table
CREATE TABLE evaluation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id INTEGER NOT NULL,
    generated_code_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    static_analysis_results TEXT,
    dynamic_analysis_results TEXT,
    rankme_score REAL,
    formal_verification_results TEXT,
    FOREIGN KEY(input_id) REFERENCES inputs(id),
    FOREIGN KEY(generated_code_id) REFERENCES generated_code(id)
);

-- Create Final Output Table
CREATE TABLE final_output (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    feedback_code TEXT NOT NULL,
    evaluation_summary TEXT,
    improvement_tips TEXT,
    FOREIGN KEY(input_id) REFERENCES inputs(id)
);
