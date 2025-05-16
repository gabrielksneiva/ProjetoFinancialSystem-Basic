-- initdb.sql

-- 1. Cria extensão para gerar UUIDs (se quiser usar UUIDs em vez de serial)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    is_active BOOLEAN DEFAULT TRUE,
);