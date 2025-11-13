-- Fix Loss of Pay leave balances
-- LOP should have 0 days allocation, not 365

-- First, let's see current LOP balances
SELECT lb.id, lt.name, lb.total_days, lb.used_days, lb.balance_days
FROM leave_balances lb
JOIN leave_types lt ON lb.leave_type_id = lt.id
WHERE lt.name = 'Loss of Pay';

-- Update LOP balances to 0
UPDATE leave_balances
SET total_days = 0, balance_days = 0
WHERE leave_type_id = (SELECT id FROM leave_types WHERE name = 'Loss of Pay');

-- Also update the leave type definition
UPDATE leave_types
SET days_per_year = 0
WHERE name = 'Loss of Pay';

-- Verify the changes
SELECT lb.id, lt.name, lb.total_days, lb.used_days, lb.balance_days
FROM leave_balances lb
JOIN leave_types lt ON lb.leave_type_id = lt.id
WHERE lt.name = 'Loss of Pay';
