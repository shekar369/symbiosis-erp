-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    date DATE NOT NULL,
    check_in TIME,
    check_out TIME,
    status VARCHAR(20) DEFAULT 'present',
    hours_worked INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create overtime table
CREATE TABLE IF NOT EXISTS overtime (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    date DATE NOT NULL,
    hours FLOAT NOT NULL,
    rate_multiplier FLOAT DEFAULT 1.5,
    amount FLOAT,
    approved_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create advances table
CREATE TABLE IF NOT EXISTS advances (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    amount FLOAT NOT NULL,
    date DATE NOT NULL,
    reason VARCHAR(255),
    approved_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'pending',
    recovery_amount FLOAT DEFAULT 0,
    deducted_amount FLOAT DEFAULT 0,
    remaining_amount FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create loans table
CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id),
    loan_type VARCHAR(100) NOT NULL,
    principal_amount FLOAT NOT NULL,
    interest_rate FLOAT DEFAULT 0,
    tenure_months INTEGER NOT NULL,
    emi_amount FLOAT NOT NULL,
    start_date DATE NOT NULL,
    paid_amount FLOAT DEFAULT 0,
    remaining_amount FLOAT,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    approved_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendance_uploads table
CREATE TABLE IF NOT EXISTS attendance_uploads (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES tenants(id),
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    uploaded_by INTEGER NOT NULL REFERENCES users(id),
    total_records INTEGER DEFAULT 0,
    successful_records INTEGER DEFAULT 0,
    failed_records INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance(employee_id, date);
CREATE INDEX IF NOT EXISTS idx_overtime_employee_date ON overtime(employee_id, date);
CREATE INDEX IF NOT EXISTS idx_advances_employee ON advances(employee_id);
CREATE INDEX IF NOT EXISTS idx_loans_employee ON loans(employee_id);
