-- Create the players table
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_staff BOOLEAN DEFAULT FALSE
);

-- Create the saves table
CREATE TABLE saves (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID REFERENCES players(id) ON DELETE CASCADE,
    save_name TEXT NOT NULL,
    cookies BIGINT DEFAULT 0,
    last_updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create the items table
CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    cost INTEGER NOT NULL,
    effect JSONB NOT NULL
);

-- Create the inventory table
CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    save_id UUID REFERENCES saves(id) ON DELETE CASCADE,
    item_id UUID REFERENCES items(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1
);

-- Populate the items table
INSERT INTO items (name, cost, effect) VALUES
('Cursor', 10, '{"type": "multiplier", "value": 0.1}'),
('Robot', 1000, '{"type": "auto_clicker", "value": 1}'),
('Grandma', 100, '{"type": "auto_clicker", "value": 5}'),
('Factory', 5000, '{"type": "auto_clicker", "value": 25}'),
('Super Clicker', 10000, '{"type": "multiplier", "value": 1.0}');
